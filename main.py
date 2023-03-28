import reader.main as rd
import graph.main as g

if __name__ == "__main__":
    # Create a graph
    adjacence = g.Adjacency(rd.read_csv("test/1.reseau"))
    gr = g.Graph(adjacent=adjacence, name="Réseau Lillois")
    
    # Add properties to nodes
    node_properties = rd.read_json("test/1.noeuds")
    gr.set_nodes_properties(node_properties)
    #gr.print_nodes_details()

    # Add fixed properties to edges
    fixed_e_properties = rd.read_json("test/1.aretesf")
    gr.set_edges_properties(fixed_e_properties)

    # Add parameters to edges
    param_edges = rd.read_json("test/1.aretesp")
    gr.set_edges_properties(param_edges)
    gr.print_edges_details()
    
    gr.puml_to_file("graphs_file/res1.puml")