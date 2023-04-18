import reader.main as rd
import graph.main as g
import controller.controller as c

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
    
    agents = [
        c.ControlledAgent("Voiture", 2.50, 41.6666666667, gr.get_node_by_name("Noeud1"), gr.get_node_by_name("Noeud9"), emission=2, emission_idle=2.1, consumption=1.2)
        , c.ControlledAgent("Camion", 6, 13.8888888889, gr.get_node_by_name("Noeud5"), gr.get_node_by_name("Noeud1"), emission=5, emission_idle=5.2, consumption=5.1)
    ]
    
    engine = c.Engine(gr, agents)
    engine.display_state()
    engine.simulate(0.5)
    
    