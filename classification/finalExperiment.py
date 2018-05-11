import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import matthews_corrcoef as mcc
import xgboost
le = preprocessing.LabelEncoder()

gains = pd.read_csv('./../data/matchagains.csv', low_memory=False)
wingains = pd.read_csv('./../data/matchwinagains.csv', low_memory=False)
wingains.set_index('id', inplace=True)
gains.set_index('id', inplace=True)
champ_advantage = wingains / gains

champions_data = pd.read_csv('./../data/champions.csv')
champions_data.set_index('name', inplace=True)
data = pd.read_csv('./../data/dataset.csv', low_memory=False)
roles_versus = {
    '0 - ADC': '1 - ADC',
    '0 - JUNGLE': '1 - JUNGLE',
    '0 - MID': '1 - MID',
    '0 - SUP': '1 - SUP',
    '0 - TOP': '1 - TOP',
    '1 - ADC': '0 - ADC',
    '1 - JUNGLE': '0 - JUNGLE',
    '1 - MID': '0 - MID',
    '1 - SUP': '0 - SUP',
    '1 - TOP': '0 - TOP',
}
roles_v = {
    '0 - ADC': '1 - ADC',
    '0 - JUNGLE': '1 - JUNGLE',
    '0 - MID': '1 - MID',
    '0 - SUP': '1 - SUP',
    '0 - TOP': '1 - TOP',
}
team0 = ['0 - ADC',    '0 - JUNGLE',    '0 - MID',    '0 - SUP',    '0 - TOP']
team1 = ['1 - ADC',    '1 - JUNGLE',    '1 - MID',    '1 - SUP',    '1 - TOP']
roles_names = ['Tank', 'Support', 'Mage', 'Assassin', 'Marksman']


def get_champ_id(champ_name):
    return champions_data.ix[champ_name, 'id']


def get_champ_type(champ_name):
    return champions_data.ix[champ_name, 'type1']


def get_team_composition(row, team):
    roles = {
        'Tank': 0,
        'Support': 0,
        'Mage': 0,
        'Assassin': 0,
        'Marksman': 0
    }
    for role in team:
        champ = row[role]
        champ_type = get_champ_type(champ)
        # print(champ_type)
        if champ_type in roles.keys():
            roles[champ_type] = 1
        elif champ_type == 'Fighter':
            roles['Tank'] = 1
    return sum(roles.values()) / len(roles)


def winrate(row):
        for key, value in roles_v.items():
            # print(row[key], get_champ_id(row[key]), '---', row[value], get_champ_id(row[value]))
            champ1_id = get_champ_id(row[key])
            champ2_id = get_champ_id(row[value])
            # print(champ_advantage.ix[champ1_id, str(champ2_id)])
            row[key + ' advantage'] = champ_advantage.ix[champ1_id, str(champ2_id)]

        row['T0 composition'] = get_team_composition(row, team0)
        row['T1 composition'] = get_team_composition(row, team1)
        return row


data['team'] = data['team'].apply(str)
data['role'] = data['team'] + ' - ' + data['position']
print(data['role'].unique())

# remove matchid with duplicate roles, e.g. 3 MID in same team, etc
remove_index = []
for i in (
        '0 - JUNGLE', '0 - SUP', '0 - ADC', '0 - TOP', '0 - MID', '1 - JUNGLE',
        '1 - TOP', '1 - MID', '1 - ADC', '1 - SUP'):
    df_remove = data[data['role'] == i].groupby('matchid').agg({'role': 'count'})
    remove_index.extend(df_remove[df_remove['role'] != 1].index.values)

# remove unclassified BOT, correct ones should be DUO_SUPPORT OR DUO_CARRY
remove_index.extend(data[data['position'] == 'BOT']['matchid'].unique())
remove_index = list(set(remove_index))

print('# matches in dataset before cleaning: {}'.format(data['matchid'].nunique()))
data = data[~data['matchid'].isin(remove_index)]
print('# matches in dataset after cleaning: {}'.format(data['matchid'].nunique()))


#

dataset_temp = data[
    ['id', 'matchid', 'player', 'name', 'position', 'role', 'win', 'kills', 'deaths', 'assists', 'turretkills',
     'totdmgtochamp', 'totheal', 'totminionskilled', 'goldspent', 'totdmgtaken', 'inhibkills', 'pinksbought',
     'wardsplaced', 'duration', 'platformid', 'seasonid', 'version', 'championid']]

dataset_fin = dataset_temp[['matchid', 'player', 'name', 'role', 'win']]
print('Before pivot', dataset_fin.head())
dataset_fin = dataset_fin.pivot(index='matchid', columns='role', values='name')
print('After pivot', dataset_fin.head())
dataset_fin = dataset_fin.reset_index()
dataset_fin = dataset_fin.merge(dataset_temp[dataset_temp['player'] == 1][['matchid', 'win']], left_on='matchid', right_on='matchid', how='left')
# dataset_fin = dataset_fin[dataset_fin.columns.difference(['matchid'])]
dataset_fin = dataset_fin.rename(columns={'win': 'T0 win'})

print(dataset_fin.head(10))

# remove missing data
print('Before drop missing data: {}'.format(len(dataset_fin)))
dataset_fin = dataset_fin.dropna()
print('After drop missing data: {}'.format(len(dataset_fin)))

rev = dataset_fin.rename(columns=roles_versus)
rev['T0 win'] = rev['T0 win'].apply(lambda x: 0 if x == 1 else 1)

dataset_fin = dataset_fin.append(rev, ignore_index=True)

print('After team reverse: {}'.format(len(dataset_fin)))
dataset_fin = dataset_fin[dataset_fin.columns.difference(['matchid'])]
print(dataset_fin.head(15))

dataset_fin = dataset_fin.apply(winrate, axis=1)
print(dataset_fin)

y = dataset_fin['T0 win']
X = dataset_fin[dataset_fin.columns.difference(['T0 win'])]


# label string to numeric
le_t = X.apply(le.fit)
X_t_1 = X.apply(le.fit_transform)

enc = preprocessing.OneHotEncoder()
enc_t = enc.fit(X_t_1)
X_t_2 = enc_t.transform(X_t_1)

X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X_t_1, y, random_state=0)
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(X_t_2, y, random_state=0)

print('Accuracy on dataset converted from label to integer category:')

logistic_regression = LogisticRegression(random_state=0)
clf_lr = logistic_regression.fit(X_train_1, y_train_1)
acc_lr = clf_lr.score(X_test_1, y_test_1)
lr_pred = logistic_regression.predict(X_test_1)
lr_mcc = mcc(y_test_1, lr_pred)
print('logistic regression accuracy: {}'.format(acc_lr))
print('logistic regression MCC: {}'.format(lr_mcc))

naive_bayes = BernoulliNB()
clf_bnb = naive_bayes.fit(X_train_1, y_train_1)
acc_bnb = clf_bnb.score(X_test_1, y_test_1)
nb_pred = naive_bayes.predict(X_test_1)
nb_mcc = mcc(y_test_1, nb_pred)
print('naive bayes accuracy: {}'.format(acc_bnb))
print('naive bayes MCC: {}'.format(nb_mcc))

gradient_boosting = xgboost.XGBClassifier()
clf_xb = gradient_boosting.fit(X_train_1, y_train_1)
acc_xb = clf_xb.score(X_test_1, y_test_1)
gb_pred = gradient_boosting.predict(X_test_1)
gb_mcc = mcc(y_test_1, gb_pred)
print('xgboost accuracy: {}'.format(acc_xb))
print('xgboost MCC: {}'.format(gb_mcc))

random_forest = RandomForestClassifier(n_estimators=10)
clf_rf = random_forest.fit(X_train_1, y_train_1)
acc_rf = clf_rf.score(X_test_1, y_test_1)
rf_pred = random_forest.predict(X_test_1)
rf_mcc = mcc(y_test_1, rf_pred)
print('Random forest : {}'.format(acc_rf))
print('Random forest MCC: {}'.format(rf_mcc))

print('\n')

# category with just 0 / 1, no magnitude meaning in category like above approach
print('Accuracy on dataset converted from label to binary category:')

logistic_regression = LogisticRegression(random_state=0)
clf_lr = logistic_regression.fit(X_train_2, y_train_2)
acc_lr = clf_lr.score(X_test_2, y_test_2)
lr_pred = logistic_regression.predict(X_test_2)
lr_mcc = mcc(y_test_1, lr_pred)
print('logistic regression accuracy: {}'.format(acc_lr))
print('logistic regression MCC: {}'.format(lr_mcc))

naive_bayes = BernoulliNB()
clf_bnb = naive_bayes.fit(X_train_2, y_train_2)
acc_bnb = clf_bnb.score(X_test_2, y_test_2)
nb_pred = naive_bayes.predict(X_test_2)
nb_mcc = mcc(y_test_1, nb_pred)
print('naive bayes accuracy: {}'.format(acc_bnb))
print('naive bayes MCC: {}'.format(nb_mcc))

gradient_boosting = xgboost.XGBClassifier()
clf_xb = gradient_boosting.fit(X_train_2, y_train_2)
acc_xb = clf_xb.score(X_test_2, y_test_2)
gb_pred = gradient_boosting.predict(X_test_2)
gb_mcc = mcc(y_test_1, gb_pred)
print('xgboost accuracy: {}'.format(acc_xb))
print('xgboost MCC: {}'.format(gb_mcc))

random_forest = RandomForestClassifier(n_estimators=10)
clf_rf = random_forest.fit(X_train_2, y_train_2)
acc_rf = clf_rf.score(X_test_2, y_test_2)
rf_pred = random_forest.predict(X_test_2)
rf_mcc = mcc(y_test_1, rf_pred)
print('Random forest : {}'.format(acc_rf))
print('Random forest MCC: {}'.format(rf_mcc))
