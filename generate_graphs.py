from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import glob
import json
import pandas as pd

data = []

files = glob.glob('results/*_agents_data.json')

df = pd.DataFrame(columns=["time_by_distance", "time_wo_stop", "simulation_id"])

cpt = 0
for file in files:
    nom_simulation = "simulation_" + str(cpt+1)
    with open(file, 'r') as f:
        #data_kilian = json.loads(f.read())
        data.append({"simulation": json.loads(f.read())})
        #for index, agent in enumerate([a for a in data_kilian if 'Agent' in a]):
         #   df.loc[cpt * 15 + index] = [data_kilian[agent]["time_by_distance"], data_kilian[agent]["time_wo_stop"], nom_simulation]
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

# sns.scatterplot(data=df, x="time_by_distance", y="time_wo_stop", hue="simulation_id")
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

print(x)
print(y)

sns.barplot(x=y, y=x, orient='h')
plt.xlabel("Vitesse (m/s)")
plt.title("Vitesse minimale des agents par simulation")
plt.show()