import pandas as pd

class Adjacency:

    def __init__(self, model:pd.DataFrame):
        # the matrix must be a square matrix
        if len(model.columns) != len(model.index):
            raise ValueError("The adjacent matrix must be a square matrix")
        self.nodes = model.columns
        self.matrix = list(model.to_numpy())

    def __str__(self):
        max_l = max([len(str(x)) for x in self.nodes]) + 5
        header = (' ' * max_l)
        string = ''
        for index, node in enumerate(self.nodes):
            str_node = str(node)
            len_n = len(str_node) + 2
            header += (' ' * (max_l - len_n)) + '"' + str_node + '"'
            string += " " * (max_l - len_n) + '"' + str(node) + '"'
            for value in self.matrix[index]:
                str_value = str(value)
                string += (" " * (max_l - len(str_value))) + str_value + ""
            string = string + "\n"
        ret = header + "\n" + string
        return ret



class Node:

    def __init__(self, name, **kwargs):
        self.name = str(name)
        self.__dict__.update(kwargs)


    def set_properties(self, properties:dict):
        self.__dict__.update(properties)


    def get_properties(self) -> dict:
        return self.__dict__.copy()


    def __str__(self):
        return str(self.name)

    @staticmethod
    def generate_nodes_by_name(nodes:"list[str]") -> "list[Node]":
        ret = []
        for node_name in nodes:
            ret.append(Node(node_name))
        return ret

class Edge:

    def __init__(self, source:Node, target:Node, **kwargs):
        self.source = source
        self.target = target
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"{self.source} --> {self.target}"

class Graph:



    def __init__(self, nodes:"list[Node]"=None, edges:"list[Edge]"=None, adjacent:Adjacency=None, **kwargs):
        if adjacent != None:
            self.nodes = Node.generate_nodes_by_name(adjacent.nodes)
            self.edges = []
            for i in range(len(adjacent.matrix)):
                for j in range(len(adjacent.matrix[i])):
                    if adjacent.matrix[i][j] == 1:
                        e = Edge(source=self.get_node_by_name(adjacent.nodes[i]), target=self.get_node_by_name(adjacent.nodes[j]))
                        self.edges.append(e)

        if nodes != None:
            self.nodes = nodes
        if edges != None:
            for edge in edges:
                if edge.source not in self.nodes:
                    raise ValueError("Edges in the graph must link to 2 Nodes in the graph.\nError on edge : " + str(edge) + ", cannot find node " + str(edge.source))
                if edge.target not in self.nodes:
                    raise ValueError("Edges in the graph must link to 2 Nodes in the graph.\nError on edge : " + str(edge) + ", cannot find node " + str(edge.target))
            self.edges = edges
        self.__dict__.update(kwargs)
    
    def get_node_by_name(self, name:str):
        for node in self.nodes:
            if node.name == name:
                return node
            

    def set_nodes_properties(self, node_properties:dict):
        for node_name in node_properties:
            node = self.get_node_by_name(node_name)
            if node is None:
                raise ValueError("No node with name %s" % node_name)
            
            node.set_properties(node_properties[node_name])


    def generate_puml(self) -> str:
        string = "@startuml"
        if "name" in self.__dict__:
            string += " \"" + str(self.name) + "\""
        string += "\n"
        for e in self.edges:
            string += f"({e.source.name}) --> ({e.target.name})\n"
        string += "@enduml"
        return string

    def puml_to_file(self, filename):
        with open(filename, "w") as file:
            file.write(self.generate_puml())


    def print_nodes_details(self):
        for node in self.nodes:
            properties = node.get_properties()
            for property in properties:
                print(property, ":", properties[property])
                
            print("================\n\n")


    def __str__(self):
        string = "Nodes : [\"" + '\",\"'.join([str(x) for x in self.nodes]) + "\"]\n"
        string += f"Edges : {[str(x) for x in self.edges]}"
        return string



