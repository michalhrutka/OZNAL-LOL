import pandas as pd

participants_data = pd.read_csv('./../data/participants.csv')
stats1_data = pd.read_csv('./../data/stats1.csv')
stats2_data = pd.read_csv('./../data/stats2.csv')
stats_data = pd.concat([stats1_data, stats2_data])
stats_data.to_csv('./../data/stats_merged.csv')

print(participants_data.describe(), len(participants_data))
print('***')
print(stats1_data.describe(), len(stats1_data))
print('***')
print(stats2_data.describe(), len(stats2_data))
print('***')
print(stats_data.describe(), len(stats_data))
print('***')

