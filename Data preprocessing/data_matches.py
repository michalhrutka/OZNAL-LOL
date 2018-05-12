import pandas as pd
import numpy as np
import csv

participants_data = pd.read_csv('./../data/participants2.csv')
champs_data = pd.read_csv('./../data/champs.csv')
stats1_data = pd.read_csv('./../data/stats1.csv')
stats2_data = pd.read_csv('./../data/stats2.csv')
stats_data = pd.concat([stats1_data, stats2_data])

champs_data = champs_data.drop(champs_data.columns[0], axis=1)
#create matrix
wins = pd.DataFrame(np.outer(champs_data, champs_data), champs_data.id, champs_data.id)
wins_on_lane = pd.DataFrame(np.outer(champs_data, champs_data), champs_data.id, champs_data.id)
wins_against = pd.DataFrame(np.outer(champs_data, champs_data), champs_data.id, champs_data.id)
wins[:] = 0
wins_on_lane[:] = 0
wins_against[:] = 0
#print(wins_on_lane)
#add results    
dataset = pd.merge(participants_data, stats_data, how='left', left_on='id', right_on='id',  suffixes=('', '_y'))
dataset = dataset.drop(dataset.columns[8:], axis=1)
matches = dataset.groupby(['matchid'])

for name, group in matches:
    poc = 0
    match = []
    for row,champion in group.iterrows():
        match.append(list(champion))
        poc += 1
        if poc == 10:
            #jedna strana
            wins.at[match[0][3],match[5][3]] +=1    
            wins.at[match[0][3],match[6][3]] +=1
            wins.at[match[0][3],match[7][3]] +=1
            wins.at[match[0][3],match[8][3]] +=1
            wins.at[match[0][3],match[9][3]] +=1
            wins.at[match[1][3],match[5][3]] +=1    
            wins.at[match[1][3],match[6][3]] +=1
            wins.at[match[1][3],match[7][3]] +=1
            wins.at[match[1][3],match[8][3]] +=1
            wins.at[match[1][3],match[9][3]] +=1
            wins.at[match[2][3],match[5][3]] +=1    
            wins.at[match[2][3],match[6][3]] +=1
            wins.at[match[2][3],match[7][3]] +=1
            wins.at[match[2][3],match[8][3]] +=1
            wins.at[match[2][3],match[9][3]] +=1
            wins.at[match[3][3],match[5][3]] +=1    
            wins.at[match[3][3],match[6][3]] +=1
            wins.at[match[3][3],match[7][3]] +=1
            wins.at[match[3][3],match[8][3]] +=1
            wins.at[match[3][3],match[9][3]] +=1
            wins.at[match[4][3],match[5][3]] +=1    
            wins.at[match[4][3],match[6][3]] +=1
            wins.at[match[4][3],match[7][3]] +=1
            wins.at[match[4][3],match[8][3]] +=1
            wins.at[match[4][3],match[9][3]] +=1
            #druha strana
            wins.at[match[5][3],match[0][3]] +=1    
            wins.at[match[5][3],match[1][3]] +=1
            wins.at[match[5][3],match[2][3]] +=1
            wins.at[match[5][3],match[3][3]] +=1
            wins.at[match[5][3],match[4][3]] +=1
            wins.at[match[6][3],match[0][3]] +=1    
            wins.at[match[6][3],match[1][3]] +=1
            wins.at[match[6][3],match[2][3]] +=1
            wins.at[match[6][3],match[3][3]] +=1
            wins.at[match[6][3],match[4][3]] +=1
            wins.at[match[7][3],match[0][3]] +=1    
            wins.at[match[7][3],match[1][3]] +=1
            wins.at[match[7][3],match[2][3]] +=1
            wins.at[match[7][3],match[3][3]] +=1
            wins.at[match[7][3],match[4][3]] +=1
            wins.at[match[8][3],match[0][3]] +=1    
            wins.at[match[8][3],match[1][3]] +=1
            wins.at[match[8][3],match[2][3]] +=1
            wins.at[match[8][3],match[3][3]] +=1
            wins.at[match[8][3],match[4][3]] +=1
            wins.at[match[9][3],match[0][3]] +=1    
            wins.at[match[9][3],match[1][3]] +=1
            wins.at[match[9][3],match[2][3]] +=1
            wins.at[match[9][3],match[3][3]] +=1
            wins.at[match[9][3],match[4][3]] +=1
            #zapis win
            if match[0][7] == 1:
                wins_on_lane.at[match[0][3],match[5][3]] +=1    
                wins_on_lane.at[match[0][3],match[6][3]] +=1
                wins_on_lane.at[match[0][3],match[7][3]] +=1
                wins_on_lane.at[match[0][3],match[8][3]] +=1
                wins_on_lane.at[match[0][3],match[9][3]] +=1
                wins_on_lane.at[match[1][3],match[5][3]] +=1    
                wins_on_lane.at[match[1][3],match[6][3]] +=1
                wins_on_lane.at[match[1][3],match[7][3]] +=1
                wins_on_lane.at[match[1][3],match[8][3]] +=1
                wins_on_lane.at[match[1][3],match[9][3]] +=1
                wins_on_lane.at[match[2][3],match[5][3]] +=1    
                wins_on_lane.at[match[2][3],match[6][3]] +=1
                wins_on_lane.at[match[2][3],match[7][3]] +=1
                wins_on_lane.at[match[2][3],match[8][3]] +=1
                wins_on_lane.at[match[2][3],match[9][3]] +=1
                wins_on_lane.at[match[3][3],match[5][3]] +=1    
                wins_on_lane.at[match[3][3],match[6][3]] +=1
                wins_on_lane.at[match[3][3],match[7][3]] +=1
                wins_on_lane.at[match[3][3],match[8][3]] +=1
                wins_on_lane.at[match[3][3],match[9][3]] +=1
                wins_on_lane.at[match[4][3],match[5][3]] +=1    
                wins_on_lane.at[match[4][3],match[6][3]] +=1
                wins_on_lane.at[match[4][3],match[7][3]] +=1
                wins_on_lane.at[match[4][3],match[8][3]] +=1
                wins_on_lane.at[match[4][3],match[9][3]] +=1
            else :
                wins_on_lane.at[match[5][3],match[0][3]] +=1    
                wins_on_lane.at[match[5][3],match[1][3]] +=1
                wins_on_lane.at[match[5][3],match[2][3]] +=1
                wins_on_lane.at[match[5][3],match[3][3]] +=1
                wins_on_lane.at[match[5][3],match[4][3]] +=1
                wins_on_lane.at[match[6][3],match[0][3]] +=1    
                wins_on_lane.at[match[6][3],match[1][3]] +=1
                wins_on_lane.at[match[6][3],match[2][3]] +=1
                wins_on_lane.at[match[6][3],match[3][3]] +=1
                wins_on_lane.at[match[6][3],match[4][3]] +=1
                wins_on_lane.at[match[7][3],match[0][3]] +=1    
                wins_on_lane.at[match[7][3],match[1][3]] +=1
                wins_on_lane.at[match[7][3],match[2][3]] +=1
                wins_on_lane.at[match[7][3],match[3][3]] +=1
                wins_on_lane.at[match[7][3],match[4][3]] +=1
                wins_on_lane.at[match[8][3],match[0][3]] +=1    
                wins_on_lane.at[match[8][3],match[1][3]] +=1
                wins_on_lane.at[match[8][3],match[2][3]] +=1
                wins_on_lane.at[match[8][3],match[3][3]] +=1
                wins_on_lane.at[match[8][3],match[4][3]] +=1
                wins_on_lane.at[match[9][3],match[0][3]] +=1    
                wins_on_lane.at[match[9][3],match[1][3]] +=1
                wins_on_lane.at[match[9][3],match[2][3]] +=1
                wins_on_lane.at[match[9][3],match[3][3]] +=1
                wins_on_lane.at[match[9][3],match[4][3]] +=1

 
#ulozenie matic
wins.to_csv('./../data/matchagains.csv')   
wins_on_lane.to_csv('./../data/matchwinagains.csv')
