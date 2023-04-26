from matplotlib import pyplot as plt
import glob
import json

data = []

files = glob.glob('results/*_agents_data.json')

for file in files:
    with open(file, 'r') as f:
        data.append({"simulation": json.loads(f.read())})
        
def mean(data:list):
    return sum(data)/len(data)



x = []
y = []
for simulation in data:
    x += [simulation['simulation'][x]['time_by_distance'] for x in simulation['simulation'] if 'Agent' in x]
    y += [simulation['simulation'][x]['time_wo_stop'] for x in simulation['simulation'] if 'Agent' in x]
# print(refined_data)
    
# x = [d['mean_time_by_distance'] for d in refined_data]
# y = [d['mean_time_wo_stop'] for d in refined_data]

plt.scatter(x, y)
plt.show()

