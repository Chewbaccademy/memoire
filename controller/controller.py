from agent.agent import Agent
from graph.main import Node
from graph.main import Graph, Node, Edge
from logger.main import Logger
from time import sleep

class ControlledAgent(Agent):
    
    def __init__(self, name, length:float, vitesse_max:float, graph:Graph, depart:Node, arrivee:Node, **properties) -> None:
        super().__init__(name, length=length, vitesse_max=vitesse_max, depart=depart, arrivee=arrivee,  **properties)
        self.distance_parcourue_sur_arrete = 0
        self.distance_parcourue = 0
        self.current_place = depart
        self.path:list = None
        self.vitesse = 0
        self.memory = []
        self.terminate = False
        self.graph = graph
        self.time_slice = 1
        
    def __str__(self):
        return f"= {self.name} | L = {self.length}, vmax = {self.vitesse_max} | s {self.depart} --> {self.arrivee} d\n"
    
    def get_property(self, name:str):
        return self.__dict__[name]
    
    def go_to_edge(self, targeted_edge:Edge) -> bool:
        if targeted_edge.vehicule_list != [] and targeted_edge.vehicule_list[-1].distance_parcourue_sur_arrete - targeted_edge.vehicule_list[-1].length <= self.length:
            return False
        if sum([l.length for l in targeted_edge.vehicule_list]) + self.length <= targeted_edge.get_property("length") \
            and self.current_place == targeted_edge.source:
            self.current_place.current_agent = None
            targeted_edge.append_properties("vehicule_list", self)
            self.current_place = targeted_edge
            self.distance_parcourue += self.length
            self.distance_parcourue_sur_arrete = self.length
            self.memory.append({'distance': self.length})
            self.vitesse = min(self.vitesse_max, targeted_edge.get_property("speed_limit"))
            return True
            
        return False
    
    def priority_check(self, targeted_node:None) -> bool:
        if targeted_node.signage == None or targeted_node.signage == "none":
            current_index = targeted_node.edges.index(self.current_place.get_property("name"))
            priority_index = (current_index + 1 if current_index + 1 < len(targeted_node.edges) else 0)
            super_priority_index = (priority_index + 1 if priority_index + 1 < len(targeted_node.edges) else 0)
            priority_edge = self.graph.get_edge_by_name(targeted_node.edges[priority_index])
            super_priority_edge = self.graph.get_edge_by_name(targeted_node.edges[super_priority_index])
            if priority_edge.vehicule_list == []:
                return True
            if (priority_edge.vehicule_list[0].distance_parcourue_sur_arrete \
                                + (priority_edge.vehicule_list[0].vitesse \
                                * self.time_slice)) \
                                > priority_edge.get_property('length') \
                    and (super_priority_edge.vehicule_list == [] or (super_priority_edge.vehicule_list[0].distance_parcourue_sur_arrete \
                                + (super_priority_edge.vehicule_list[0].vitesse \
                                * self.time_slice)) \
                                <= super_priority_edge.get_property('length')):
                return False
            
            return True
                                
        elif targeted_node.signage == "lights":
            if not self.current_place.name in targeted_node.light_phases[targeted_node.get_property("current_phase")]["edges"]:
                print("feu rouge detecté, temps restant : %s" % (targeted_node.get_property("countdown")))
            return self.current_place.name in targeted_node.light_phases[targeted_node.get_property("current_phase")]["edges"]
        
        return False
                
            
        
    def go_to_node(self, targeted_node:Node) -> bool:
        if self.priority_check(targeted_node):
            if targeted_node.current_agent == None or targeted_node.current_agent.terminate:
                targeted_node.current_agent = self
                self.current_place.get_property("vehicule_list").pop(0)
                self.current_place = targeted_node
                if targeted_node == self.arrivee:
                    self.terminate = True
                    
                return True
    
        return False
    
    def generate_path(self, reseau:Graph, method) -> list:
        path = method(reseau, self.depart, self.arrivee)
        self.path = path
        return path
    
    def step(self, time_slice:float) -> bool:
        self.time_slice = time_slice
        
        if self.terminate == True:
            return True
    
        # set the end of simulation for agent who have reached their destination
        if self.current_place == self.arrivee:
            self.terminate = True
            return True
        

        print("%s | l: %s | current_place : %s | length_driven : %s | vitesse : %s" % (self.name,self.length, self.current_place, self.distance_parcourue_sur_arrete, self.vitesse))
        
        # travel to the next edge on the path
        if type(self.current_place) == Node:
            if self.current_place == self.arrivee:
                self.current_place.current_agent = None
                self.terminate = True
            res = self.go_to_edge(self.path[0])
            if res:
                self.path.pop(0)
            return res        
        
        distance_avancee = self.vitesse * time_slice
        
        # if reached the end of the edge
        if self.distance_parcourue_sur_arrete + distance_avancee > self.current_place.get_property("length") \
            and self.current_place.get_property("vehicule_list")[0] == self:
            self.memory.append({'distance': self.current_place.get_property("length") - self.distance_parcourue_sur_arrete})
            self.distance_parcourue += self.current_place.get_property("length") - self.distance_parcourue_sur_arrete
            res=self.go_to_node(self.current_place.target)
            return res
        

        # test if the vehicule is blocked by other cars
        index_vehicule = self.current_place.get_property("vehicule_list").index(self)
        block_point = self.current_place.get_property("length")
        for vehicule in self.current_place.get_property("vehicule_list")[:index_vehicule]:
            block_point -= vehicule.get_property("length")
            
        old_distance_parcourue_sur_arrete = self.distance_parcourue_sur_arrete
        self.distance_parcourue_sur_arrete = min(block_point, self.distance_parcourue_sur_arrete + distance_avancee)
        
        self.memory.append({'distance': self.distance_parcourue_sur_arrete - old_distance_parcourue_sur_arrete})
        self.distance_parcourue += self.distance_parcourue_sur_arrete - old_distance_parcourue_sur_arrete
        
        return True
        
        
        
    def display_path(self):
        p = "S o "
        for edge in self.path:
            p += str(edge) + " o "
        p += "D"
        return p
        
    
        
        
        
class Engine:
    
    def __init__(self, graph:Graph, agent_list:list[ControlledAgent]) -> None:
        self.graph = graph
        self.agent_list = agent_list
        self.logger = Logger()
        self.step = 0
        
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
        
    def simulate(self, time_slice:float) -> None:
        
        # generate all the paths for every agents
        for agent in self.agent_list:
            agent.generate_path(self.graph, dijkstra)
            print(agent.display_path())
        
        # launch the simulation
        while not self.__every_agent_is_terminated():
            
            # trafic lights management
            nodes_with_lights = [n for n in self.graph.nodes if n.signage == "lights"]
            for node in nodes_with_lights:
                if not "current_phase" in node.get_properties():
                    node.set_property("current_phase", 0)
                    node.set_property("color", "green")
                    node.set_property("countdown", node.light_phases[0]["green_time"] + time_slice)
                    
                node.set_property("countdown", node.countdown - time_slice)
                
                if node.countdown <= 0:
                    if node.get_property("color") == "green":
                        node.set_property("color", "orange")
                        node.set_property("countdown", node.light_phases[0]["orange_time"])
                    if node.get_property("color") == "orange" and "delay" in node.light_phases[0]:
                        node.set_property("color", "delay")
                        node.set_property("countdown", node.light_phases[0]["delay"])
                    else:
                        new_phase = (node.get_property("current_phase") + 1 if node.get_property("current_phase") + 1 < len(node.light_phases) else 0)
                        node.set_property("current_phase", new_phase)
                        node.set_property("color", "green")
                        node.set_property("countdown", node.light_phases[new_phase]["green_time"] + time_slice)
                
            
            for agent in self.agent_list:
                agent.step(time_slice=time_slice)
                self.logger.record_agent_state(agent, self.step, time_slice=time_slice)

            for edge in self.graph.edges:
                self.logger.record_edge_state(edge, self.step, time_slice=time_slice)
            
            self.step += 1
                
        for agent in self.agent_list:
            print(agent.memory)

        self.logger.extract_data()
        
            
    def __every_agent_is_terminated(self):
        for agent in self.agent_list:
            if agent.terminate == False:
                return False
        return True
        
        
def dijkstra(graph:Graph, source:Node, destination:Node):
    
    memory = {}
    for node in graph.nodes:
        memory[node.name] = {'source': None, 'distance': float('Inf'), 'edge_source': None}
    memory[source.name]['distance'] = 0
    
    while True:
        node_min = {'source': None, 'distance': float('Inf'), 'edge_source': None}
        node_min_name = ""
        for node in [n for n in graph.nodes if memory[n.name]['distance'] == float('Inf')]:
            tmp = {'source': None, 'distance': float('Inf'), 'edge_source': None}
            for edge in [e for e in graph.edges if e.target == node and memory[e.source.name]['distance'] != float('Inf')]:
                if float(edge.get_property('length') * edge.get_property('speed_limit')) < tmp["distance"]:
                    tmp = {'source': edge.source, 'distance': edge.get_property('length'), 'edge_source': edge}
                    
            if tmp['distance'] < node_min['distance']:
                node_min = tmp
                node_min_name = node.name
        
        memory[node_min_name] = node_min
        
        if node_min_name == destination.name:
            break
        
    path = []
    current_node = destination
    while current_node != source:
        path.append(memory[current_node.name]['edge_source'])
        current_node = memory[current_node.name]['source']
        
    path = list(reversed(path))
    
    return path
                
            
                
            
            