from matplotlib import pyplot as plt
import glob
import json
import pandas as pd

data = []

files = glob.glob('results/*_agents_data.json')

for file in files:
    with open(file, 'r') as f:
        data.append({"simulation": json.loads(f.read())})
        
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

x = []
y = []
for simulation in data:
    x += ["Simulation %i" % (len(x)+1)]
    total_emission = 0
    for info in simulation['simulation']:
        if 'Agent' in info:
            total_emission += simulation['simulation'][info]["total_emission"]
    y.append(total_emission)

print(x)
print(y)

plt.barh(x, y)
plt.xlabel("emission de CO2")
plt.title("Emission totale par simulation")
plt.show()