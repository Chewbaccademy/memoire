from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import glob
import json

data = []

files = glob.glob('results/*_agents_data.json')

df = pd.DataFrame(columns=["time_by_distance", "time_wo_stop", "simulation_id"])

cpt = 0
for file in files:
    nom_simulation = "simulation_" + str(cpt+1)
    with open(file, 'r') as f:
        data = json.loads(f.read())
        for index, agent in enumerate([a for a in data if 'Agent' in a]):
            df.loc[cpt * 15 + index] = [data[agent]["time_by_distance"], data[agent]["time_wo_stop"], nom_simulation]
    cpt += 1
        
def mean(data:list):
    return sum(data)/len(data)

print(df.to_string())

# x = []
# y = []
# for simulation in data:
#     x += [simulation['simulation'][x]['time_by_distance'] for x in simulation['simulation'] if 'Agent' in x]
#     y += [simulation['simulation'][x]['time_wo_stop'] for x in simulation['simulation'] if 'Agent' in x]
# # print(refined_data)
    
# # x = [d['mean_time_by_distance'] for d in refined_data]
# # y = [d['mean_time_wo_stop'] for d in refined_data]

sns.scatterplot(data=df, x="time_by_distance", y="time_wo_stop", hue="simulation_id")
plt.show()
