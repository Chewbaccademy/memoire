import json
import random
import os

import reader.main as rd
import graph.main as g
import controller.controller as c

N = 20 # Configurations to generate
possible_limits = [30/3.6, 50/3.6, 70/3.6]
possible_signages = ["none", "lights"]
node_edges = {
    "Noeud1" : ["Noeud5-Noeud1", "Noeud2-Noeud1", "Noeud3-Noeud1"],
    "Noeud2" : ["Noeud1-Noeud2", "Noeud6-Noeud2", "Noeud7-Noeud2"],
    "Noeud3" : ["Noeud1-Noeud3", "Noeud10-Noeud3", "Noeud9-Noeud3"],
    "Noeud4" : ["Noeud6-Noeud4", "Noeud8-Noeud4", "Noeud3-Noeud4"],
    "Noeud5" : ["Noeud1-Noeud5", "Noeud10-Noeud5", "Noeud9-Noeud5", "Noeud7-Noeud5"],
    "Noeud6" : ["Noeud2-Noeud6", "Noeud4-Noeud6", "Noeud8-Noeud6", "Noeud9-Noeud6"],
    "Noeud7" : ["Noeud2-Noeud7", "Noeud5-Noeud7", "Noeud10-Noeud7"],
    "Noeud8" : ["Noeud4-Noeud8", "Noeud6-Noeud8", "Noeud9-Noeud8"],
    "Noeud9" : ["Noeud5-Noeud9", "Noeud6-Noeud9", "Noeud8-Noeud9", "Noeud10-Noeud9"],
    "Noeud10" : ["Noeud3-Noeud10", "Noeud5-Noeud10", "Noeud9-Noeud10"]
}

for i in range(N):
    print("\n\n\n\n=============== SIMULATION %i ================\n\n\n\n" % i)
    # Generate .aretesp file
    aretesp = dict()
    with open('test/1.reseau', 'r') as file:
        header = file.readline()
        nodes = header.replace('"', '').replace('\n', '').split(',')
        for l_i, line in enumerate(file):
            for c_i, value in enumerate(line.split(',')):
                if int(value) == 1:
                    edge_name = str(nodes[l_i]) + "-" + str(nodes[c_i])
                    aretesp[edge_name] = {'speed_limit': random.choice(possible_limits)}

    json_ = json.dumps(aretesp)
    with open("config/%i.aretesp" % i, "w") as f:
        f.write(json_)

    # Generate .noeuds file
    noeuds = dict()
    for node in node_edges:
        node_properties = dict()
        node_properties["edges"] = node_edges[node]
        node_properties["signage"] = random.choice(possible_signages)
        if len(node_properties["edges"]) != 4:
            node_properties["signage"] = "none"

        if node_properties["signage"] == "lights":
            node_properties["light_phases"] = [
                {
                    "edges": [node_properties["edges"][0], node_properties["edges"][2]],
                    "green_time": random.randint(10, 30),
                    "orange_time": random.randint(2,8),
                    "delay": random.randint(1, 5)
                },
                {
                    "edges": [node_properties["edges"][1], node_properties["edges"][3]],
                    "green_time": random.randint(10, 30),
                    "orange_time": random.randint(2,8),
                    "delay": random.randint(1, 5)
                }
            ]

        noeuds[node] = node_properties

    json_ = json.dumps(noeuds)
    with open("config/%i.noeuds" % i, "w") as f:
        f.write(json_)

    # Run the simulation
    adjacence = g.Adjacency(rd.read_csv("test/1.reseau"))
    gr = g.Graph(adjacent=adjacence, name="Réseau Lillois")
    gr.set_nodes_properties(noeuds)
    fixed_e_properties = rd.read_json("test/2.aretesf")
    gr.set_edges_properties(fixed_e_properties)
    gr.set_edges_properties(aretesp)    
    gr.puml_to_file("graphs_file/res1.puml")
    param_agents = rd.read_json("test/1.agents")
    rng = random.Random(param_agents["seed"])
    n = 1 # Id to make sure agents names are unique
    agents = []
    for agent_type in param_agents["agents"]:
        for k in range(agent_type["number"]):
            start_end = rng.sample(gr.nodes, 2)
            name = "Agent%i" % n
            n += 1
            agent = c.ControlledAgent(name, agent_type["length"], agent_type["vitesse_max"], gr, start_end[0], start_end[1], emission=agent_type["emission"], emission_idle=agent_type["emission_idle"], consumption=agent_type["consumption"])
            print(agent)
            agents.append(agent)

    engine = c.Engine(gr, agents)
    engine.display_state()
    engine.simulate(0.5)

    # Rename the result files
    os.rename("results/agents_data.csv", "results/%i_agents_data.csv" % i)
    os.rename("results/edges_data.csv", "results/%i_edges_data.csv" % i)