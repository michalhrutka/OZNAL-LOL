import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
import xgboost
le = preprocessing.LabelEncoder()


data = pd.read_csv('./../data/dataset.csv', low_memory=False)

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
     'wardsplaced', 'duration', 'platformid', 'seasonid', 'version']]

dataset_fin = dataset_temp[['matchid', 'player', 'name', 'role', 'win']]
print('Before pivot', dataset_fin.head())
dataset_fin = dataset_fin.pivot(index='matchid', columns='role', values='name')
print('After pivot', dataset_fin.head())
dataset_fin = dataset_fin.reset_index()
dataset_fin = dataset_fin.merge(dataset_temp[dataset_temp['player'] == 1][['matchid', 'win']], left_on='matchid', right_on='matchid', how='left')
dataset_fin = dataset_fin[dataset_fin.columns.difference(['matchid'])]
dataset_fin = dataset_fin.rename(columns={'win': 'T1 win'})

print(dataset_fin.head(10))

# remove missing data
print('Before drop missing data: {}'.format(len(dataset_fin)))
dataset_fin = dataset_fin.dropna()
print('After drop missing data: {}'.format(len(dataset_fin)))

rev = dataset_fin.rename(columns={
    '0 - ADC': '1 - ADC',
    '0 - JUNGLE': '1 - JUNGLE',
    '0 - MID': '1 - MID',
    '0 - SUP': '1 - SUP',
    '0 - TOP': '1 - TOP',
    '1 - ADC': '0 - ADC',
    '1 - JUNGLE': '0 - JUNGLE',
    '1 - MID': '0 - MID',
    '1 - SUP': '0 - SUP',
    '1 - TOP': '0 - TOP'
})
rev['T1 win'] = rev['T1 win'].apply(lambda x: 0 if x == 1 else 1)

print(dataset_fin.tail(10))

dataset_fin = dataset_fin.append(rev, ignore_index=True)

print(dataset_fin.tail(10))
print('After team reverse: {}'.format(len(dataset_fin)))


y = dataset_fin['T1 win']
X = dataset_fin[dataset_fin.columns.difference(['T1 win'])]

# label string to numeric
le_t = X.apply(le.fit)
X_t_1 = X.apply(le.fit_transform)

enc = preprocessing.OneHotEncoder()
enc_t = enc.fit(X_t_1)
X_t_2 = enc_t.transform(X_t_1)

X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X_t_1, y, random_state=0)
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(X_t_2, y, random_state=0)

print('Accuracy on dataset converted from label to integer category:')

clf_lr = LogisticRegression(random_state=0).fit(X_train_1, y_train_1)
acc_lr = clf_lr.score(X_test_1, y_test_1)
print('logistic regression : {}'.format(acc_lr))

clf_bnb = BernoulliNB().fit(X_train_1, y_train_1)
acc_bnb = clf_bnb.score(X_test_1, y_test_1)
print('naive bayes : {}'.format(acc_bnb))

clf_xb = xgboost.XGBClassifier().fit(X_train_1, y_train_1)
acc_xb = clf_xb.score(X_test_1, y_test_1)
print('xgboost : {}'.format(acc_xb))

print('\n')

# category with just 0 / 1, no magnitude meaning in category like above approach
print('Accuracy on dataset converted from label to binary category:')

clf_lr = LogisticRegression(random_state=0).fit(X_train_2, y_train_2)
acc_lr = clf_lr.score(X_test_2, y_test_2)
print('logistic regression : {}'.format(acc_lr))

clf_bnb = BernoulliNB().fit(X_train_2, y_train_2)
acc_bnb = clf_bnb.score(X_test_2, y_test_2)
print('naive bayes : {}'.format(acc_bnb))

clf_xb = xgboost.XGBClassifier().fit(X_train_2, y_train_2)
acc_xb = clf_xb.score(X_test_2, y_test_2)
print('xgboost : {}'.format(acc_xb))
print()
