import pandas as pd
pd.options.mode.chained_assignment = None

# read data
participants_data = pd.read_csv('./../data/participants2.csv')
stats_data = pd.read_csv('./../data/stats_merged.csv')
champions_data = pd.read_csv('./../data/champs.csv')
matches_data = pd.read_csv('./../data/matches.csv')

# Drop columns (Probably useless for now)
# stats_data.drop(['trinket', 'killingsprees', 'largestcrit', 'totheal', 'totunitshealed', 'dmgselfmit', 'dmgtoobj',
#                  'dmgtoturrets', 'visionscore', 'goldspent', 'pinksbought', 'wardsbought', 'wardsplaced',
#                  'wardskilled'], axis=1, inplace=True)


# Print column names
print(participants_data.columns)
print(champions_data.columns)

# Print first 5 data samples
print(participants_data.head(5).to_string())

#divide games by time
early_game = []
mid_game = []
late_game = []
print(matches_data.columns)
for i,record in matches_data.iterrows():
    if int(record['duration']) > 1000 and int(record['duration']) < 1200:
        early_game.append(record)
    elif int(record['duration']) >= 1200 and int(record['duration']) < 2400:
        mid_game.append(record)
    else:
        late_game.append(record)

# Add champion names into participants data
participants_data = pd.merge(left=participants_data, right=champions_data, how='left', left_on='championid',
                             right_on='id',  suffixes=('', '_y'))

# Drop redundant column created by merge
participants_data.drop(['id_y'], axis=1, inplace=True)
print(participants_data.head().to_string())

# Select desired columns from the stats dataset
# stats_data = stats_data[['id', 'win', 'champlvl', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']]

# Add stats data to participants
dataset = pd.merge(participants_data, stats_data, how='left', left_on='id', right_on='id',  suffixes=('', '_y'))

# Add matches data to dataset
dataset = pd.merge(dataset, matches_data, how='left', left_on='matchid', right_on='id',  suffixes=('', '_y'))

# Print statistics and first 5 rows
print(dataset.describe().to_string())
print(dataset.head().to_string())

# # Print unique values in each column
# for col in dataset.columns:
#     print(col, ':', dataset[col].unique(), '\n')

# One hot encoding of several columns
one_hot_encoded_champs = pd.get_dummies(dataset['name'], prefix='', prefix_sep='')
# one_hot_encoded_roles = pd.get_dummies(dataset['role'], prefix='', prefix_sep='')
one_hot_encoded_positions = pd.get_dummies(dataset['position'], prefix='', prefix_sep='')
one_hot_encoded_items = pd.get_dummies(dataset['item1'], prefix='', prefix_sep='')

dataset['version'][dataset['version'].str.startswith('7', na=False)] = 7
dataset['version'][dataset['version'].str.startswith('6', na=False)] = 6
dataset['version'][dataset['version'].str.startswith('5', na=False)] = 5
dataset['version'][dataset['version'].str.startswith('4', na=False)] = 4
print(dataset['version'].value_counts())

dataset['player'][dataset['player'] <= 5] = 0
dataset['player'][dataset['player'] > 5] = 1
print(dataset['player'].value_counts())

dataset.to_csv('./../data/dataset.csv')
