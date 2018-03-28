import pandas as pd

champions_data = pd.read_csv('./../data/champs.csv')
participants_data = pd.read_csv('./../data/participants.csv')
stats1_data = pd.read_csv('./../data/stats1.csv')
stats2_data = pd.read_csv('./../data/stats2.csv')
stats_data = pd.concat([stats1_data, stats2_data])
stats_data.to_csv('./../data/stats_merged.csv')

#load participants
participants_data2 = []
import csv 
with open("./../data/participants.csv", newline='') as part2:
    reader = csv.reader(part2, delimiter=',', quotechar = "\"")
    for row in reader:
        participants_data2.append(row)


#prepare column position
for row in participants_data2:
    if row[-2] != "role" and row[-2] !=  "NONE" and row[-2] != "SOLO":
        if row[-2] == "DUO_CARRY":
            row[-1] = "ADC"
        else:
            row[-1] = "SUP"
    del(row[-2])

#write to csv participants2.csv
import csv
with open('./../data/participants2.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for row in participants_data2:
        wr.writerow(row)
print("Upravene")

#import json champions
import json
with open('./../data/champions.json') as json_data:
    d = json.load(json_data)

#create tamp hashmap
data = d.get("data")
champions_types = {}
for k,v in data.items():
    temp_row = []    
    temp_row.append(v['tags'][0])
    if len(v['tags']) > 1:
        temp_row.append(v['tags'][1])
    else:
        temp_row.append("null")
    temp_row.append(v['partype'])   
    champions_types[int(v['key'])] = temp_row

#add types champions to champions
for index,row in champions_data.iterrows():
    champions_data.loc[index,'type1'] = champions_types[int(row['id'])][0]
    champions_data.loc[index,'type2'] = champions_types[int(row['id'])][1]
    champions_data.loc[index,'type3'] = champions_types[int(row['id'])][2]

champions_data.to_csv('./../data/champions.csv')

import json
with open('./../data/item.json') as json_data:
    d = json.load(json_data)
data = d.get("data")
    
item_types = {}
max_types = 0
#data_items = []
for k,v in data.items():
    temp_row = []
    for types in v['tags']:
        if len(v['tags']) > max_types:
            max_types = len(v['tags'])
        temp_row.append(types)   
    item_types[k] = temp_row

data_items =[['id','type1','type2','type3','type4','type5','type6','type7']]
for k,v in item_types.items():
    temp_list = []
    temp_list.append(k)
    for i in range(max_types):
        if len(v) > i:
            temp_list.append(v[i])
        else:
            temp_list.append("null")
    data_items.append(temp_list)

import csv
with open('./../data/typeitems.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for row in data_items:
        wr.writerow(row)
        
print(champions_data.describe(), len(champions_data))
print('***')
print(participants_data.describe(), len(participants_data))
print('***')
print(stats1_data.describe(), len(stats1_data))
print('***')
print(stats2_data.describe(), len(stats2_data))
print('***')
print(stats_data.describe(), len(stats_data))
print('***')


