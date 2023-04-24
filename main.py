import reader.main as rd
import graph.main as g
import controller.controller as c

import random


if __name__ == "__main__":
    # Create a graph
    adjacence = g.Adjacency(rd.read_csv("test/1.reseau"))
    gr = g.Graph(adjacent=adjacence, name="Réseau Lillois")
    
    # Add properties to nodes
    node_properties = rd.read_json("test/1.noeuds")
    gr.set_nodes_properties(node_properties)
    #gr.print_nodes_details()

    # Add fixed properties to edges
    fixed_e_properties = rd.read_json("test/2.aretesf")
    gr.set_edges_properties(fixed_e_properties)

    # Add parameters to edges
    param_edges = rd.read_json("test/1.aretesp")
    gr.set_edges_properties(param_edges)
    #gr.print_edges_details()
    
    gr.puml_to_file("graphs_file/res1.puml")
    
    param_agents = rd.read_json("test/1.agents")
    random.seed(param_agents["seed"])
    n = 1 # Id to make sure agents names are unique
    agents = []
    for agent_type in param_agents["agents"]:
        for i in range(agent_type["number"]):
            start_end = random.sample(gr.nodes, 2)
            name = "Agent%i" % n
            n += 1
            agent = c.ControlledAgent(name, agent_type["length"], agent_type["vitesse_max"], start_end[0], start_end[1], emission=agent_type["emission"], emission_idle=agent_type["emission_idle"], consumption=agent_type["consumption"])
            print(agent)
            agents.append(agent)


    engine = c.Engine(gr, agents)
    engine.display_state()
    engine.simulate(0.5)
    
    