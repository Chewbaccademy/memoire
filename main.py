import reader.main as rd
import graph.main as g

if __name__ == "__main__":
    adjacencce = g.Adjacency(rd.read_csv("test/1.reseau"))
    gr = g.Graph(adjacent=adjacencce, name="Réseau Lillois")
    gr.puml_to_file("graphs_file/res1.puml")