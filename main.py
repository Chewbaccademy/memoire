import reader.main as rd
import graph.main as g

if __name__ == "__main__":
    adjacencce = g.Adjacency(rd.read_csv("test/1.res"))
    n1 = g.Node("A")
    n2 = g.Node("B")
    n3 = g.Node("C")
    e1 = g.Edge(n1, n2)
    gr = g.Graph(adjacent=adjacencce, name="Réseau Lillois")
    with open("graphs_file/res1.puml", "w") as file:
        file.write(gr.generate_puml())