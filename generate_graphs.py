from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import glob
import json
import pandas as pd
import numpy as np

data = []

files = glob.glob('results/*_agents_data.json')

df = pd.DataFrame(columns=["time_by_distance", "time_wo_stop", "simulation_id"])
raw = ""
cpt = 0
for file in files:
    nom_simulation = "simulation_" + str(cpt+1)
    with open(file, 'r') as f:
        raw = f.read()
        data_kilian = json.loads(raw)
        data.append({"simulation": json.loads(raw)})
        for index, agent in enumerate([a for a in data_kilian if 'Agent' in a]):
            df.loc[cpt * 60 + index] = [data_kilian[agent]["time_by_distance"], (data_kilian[agent]["time_by_distance"] - data_kilian[agent]["time_wo_stop"]) / data_kilian[agent]["time_wo_stop"], nom_simulation]
    cpt += 1
        
def mean(data:list):
    return sum(data)/len(data)

def sort_func(x):
    return int(str(x).split('_')[1])

dataf = df.groupby("simulation_id").mean()
print(dataf)

x = dataf["time_by_distance"]
y = dataf["time_wo_stop"]


# x = []
# y = []
# for simulation in data:
#     x += [simulation['simulation'][x]['time_by_distance'] for x in simulation['simulation'] if 'Agent' in x]
#     y += [simulation['simulation'][x]['time_wo_stop'] for x in simulation['simulation'] if 'Agent' in x]
# # print(refined_data)
    
# # x = [d['mean_time_by_distance'] for d in refined_data]
# # y = [d['mean_time_wo_stop'] for d in refined_data]

sns.scatterplot(data=df, x="time_by_distance", y="time_wo_stop", hue="simulation_id")
plt.plot([0.1, 1.15], [0, 10], color='red', linestyle='-', linewidth=2)
plt.show()

df["best_way"] = df["time_by_distance"] == df["time_wo_stop"]

df2 = pd.DataFrame(index=df["simulation_id"].unique())
df2["agent_best"] = df[df["best_way"] == 1].groupby("simulation_id").count()["best_way"]
df2["agent_not_best"] = df[df["best_way"] == 0].groupby("simulation_id").count()["best_way"]
print(df2)

d = {"agent_did_best": df2["agent_best"], "pct_agent_did_best": (df2["agent_best"] / (df2["agent_best"] + df2["agent_not_best"]) * 100)}
dataf = pd.DataFrame(d)
dataf.to_csv("results/stats_agent_did_best.csv")
# print(dataf)

c = {
    "agent_did_best": df2["agent_best"],
    "agent_did_not_best": df2["agent_not_best"]
}

x = tuple(df2.index)

fig, ax = plt.subplots()
bottom = np.zeros(20)

for i, row in c.items():
    p = ax.bar(x, np.array(row), 0.5, label=i, bottom=bottom)
    bottom += row

ax.set_title("Nombre d'agents ayant réalisé le temps attendu par simulation")
plt.xticks(rotation = 45)

# plt.show()

plt.rcParams["figure.figsize"] = (9,5)

# def mean(data:list):
#     return sum(data)/len(data)



# x = []
# y = []
# for simulation in data:
#     x += [simulation['simulation'][x]['time_by_distance'] for x in simulation['simulation'] if 'Agent' in x]
#     y += [simulation['simulation'][x]['time_wo_stop'] for x in simulation['simulation'] if 'Agent' in x]
# # print(refined_data)
    
# # x = [d['mean_time_by_distance'] for d in refined_data]
# # y = [d['mean_time_wo_stop'] for d in refined_data]

# plt.scatter(x, y)
# plt.show()


# Emission

# x = []
# y = []
# for simulation in data:
#     x += ["Simulation %i" % (len(x)+1)]
#     total_emission = 0
#     for info in simulation['simulation']:
#         if 'Agent' in info:
#             total_emission += simulation['simulation'][info]["total_emission"]
#     y.append(total_emission)

# print(x)
# print(y)

# #plt.barh(x, y)
# sns.barplot(x=y, y=x, orient='h')
# plt.xlabel("emission de CO2 (u.a.)")
# plt.title("Emission totale par simulation")
# plt.show()


# # Consumption

# x = []
# y = []
# for simulation in data:
#     x += ["Simulation %i" % (len(x)+1)]
#     total_consumption = 0
#     nb_agents = 0
#     for info in simulation['simulation']:
#         if 'Agent' in info:
#             nb_agents += 1
#             total_consumption += simulation['simulation'][info]["total_consumption"]
#     y.append(total_consumption/nb_agents)

# print(x)
# print(y)

# #plt.barh(x, y)
# sns.barplot(x=y, y=x, orient='h')
# plt.xlabel("Coût (u.a.)")
# plt.title("Coût moyen de la consommation énergétique par agent par simulation")
# plt.show()


# # Travel time


# x = []
# y = []
# for simulation in data:
#     x += [simulation['simulation'][x]['total_time'] for x in simulation['simulation'] if 'Agent' in x]
#     y += [simulation['simulation'][x]['total_distance'] for x in simulation['simulation'] if 'Agent' in x]

# plt.xlabel("Temps (s)")
# plt.ylabel("Distance (m)")
# plt.title("Distance en fonction du temps par agent")
# sns.scatterplot(x=x, y=y)
# plt.show()


# x = []
# y = []
# for simulation in data:
#     x += ["Simulation %i" % (len(x)+1)]
#     total_speed = 0
#     nb_agents = 0
#     for info in simulation['simulation']:
#         if 'Agent' in info:
#             nb_agents += 1
#             total_speed += simulation['simulation'][info]["total_distance"] / simulation['simulation'][info]["total_time"]
#     y.append(total_speed/nb_agents)

# print(x)
# print(y)

# sns.barplot(x=y, y=x, orient='h')
# plt.xlabel("Vitesse (m/s)")
# plt.title("Vitesse moyenne des agents par simulation")
# plt.show()


x = []
y = []
for simulation in data:
    x += ["Simulation %i" % (len(x)+1)]
    min_speed = 999
    for info in simulation['simulation']:
        if 'Agent' in info:
            speed = simulation['simulation'][info]["total_distance"] / simulation['simulation'][info]["total_time"]
            if min_speed > speed:
                min_speed = speed
    y.append(min_speed)

plt.barh(x, y)
plt.xlabel("Vitesse (m/s)")
plt.title("Vitesse moyenne des agents par simulation")
# plt.show()
print(x)
print(y)

sns.barplot(x=y, y=x, orient='h')
plt.xlabel("Vitesse (m/s)")
plt.title("Vitesse minimale des agents par simulation")
plt.show()
