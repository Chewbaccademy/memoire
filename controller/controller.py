from agent.agent import Agent
from graph.main import Node
from graph.main import Graph, Node


class ControlledAgent(Agent):
    
    def __init__(self, name, longueur:float, vitesse_max:float, depart:Node, arrivee:Node, **properties) -> None:
        super().__init__(name, longueur=longueur, vitesse_max=vitesse_max, depart=depart, arrivee=arrivee,  **properties)
        self.distance_parcourue = 0
        
    def __str__(self):
        return f"= {self.name} | L = {self.longueur}, vmax = {self.vitesse_max} | s {self.depart} --> {self.arrivee} d\n"
        
        
class Engine:
    
    def __init__(self, graph:Graph, agent_list:list[ControlledAgent]) -> None:
        self.graph = graph
        self.agent_list = agent_list
        
        for agent in self.agent_list:
            depart_node:Node = agent.depart
            depart_node.append_properties("agent_list", agent)
            
    def display_state(self):
        print("AGENTS:")
        for agent in self.agent_list:
            print(str(agent))
        
        print("\n\n\n========================\nNODES:")
        self.graph.print_nodes_details()
        
        print("\n\n\n========================\nEDGES:")
        self.graph.print_nodes_details()