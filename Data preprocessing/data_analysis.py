import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

dataset = pd.read_csv('./../data/stats_merged.csv')

print(dataset.columns)


df_corr = dataset._get_numeric_data()
df_corr = df_corr.drop(['id', 'Unnamed: 0', 'totunitshealed', 'longesttimespentliving', 'visionscore', 'dmgselfmit', 'totheal', 'enemyjunglekills', 'pinksbought', 'totcctimedealt', 'totdmgdealt', 'truedmgdealt', 'pentakills', 'firstblood', 'quadrakills', 'triplekills', 'legendarykills', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'trinket', 'timecc'], axis=1)

mask = np.zeros_like(df_corr.corr(), dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
cmap = sns.diverging_palette(10, 150, as_cmap=True)

plt.figure(figsize=(90, 60))
correlations = df_corr.corr()
# sns.heatmap(correlations, cmap=cmap, annot=True, fmt = '.2f', mask = mask, square=True, linewidths=.5, center = 0)
# plt.title('Correlations - win vs factors (all games)')
# plt.show()
print(correlations[correlations >= 0.5].to_string())

