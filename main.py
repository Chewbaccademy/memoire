import reader.main as rd
import graph.main as g

if __name__ == "__main__":
    # Create a graph
    adjacence = g.Adjacency(rd.read_csv("test/1.reseau"))
    gr = g.Graph(adjacent=adjacence, name="Réseau Lillois")
    
    # Add properties to nodes
    node_properties = rd.read_json("test/1.noeuds")
    gr.set_nodes_properties(node_properties)
    gr.print_nodes_details()
    
    gr.puml_to_file("graphs_file/res1.puml")