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

df = data[
    ['id', 'matchid', 'player', 'name', 'position', 'role', 'win', 'kills', 'deaths', 'assists', 'turretkills',
     'totdmgtochamp', 'totheal', 'totminionskilled', 'goldspent', 'totdmgtaken', 'inhibkills', 'pinksbought',
     'wardsplaced', 'duration', 'platformid', 'seasonid', 'version']]

df_3 = df[['matchid', 'player', 'name', 'role', 'win']]
print('Before pivot', df_3.head())
df_3 = df_3.pivot(index='matchid', columns='role', values='name')
print('After pivot', df_3.head())
df_3 = df_3.reset_index()
df_3 = df_3.merge(df[df['player'] == 1][['matchid', 'win']], left_on='matchid', right_on='matchid', how='left')
df_3 = df_3[df_3.columns.difference(['matchid'])]
df_3 = df_3.rename(columns={'win': 'T1 win'})

print(df_3.head(10))

# remove missing data
print('Before drop missing data: {}'.format(len(df_3)))
df_3 = df_3.dropna()
print('After drop missing data: {}'.format(len(df_3)))

y = df_3['T1 win']
X = df_3[df_3.columns.difference(['T1 win'])]

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
