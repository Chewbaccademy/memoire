import pandas as pd

from graph.main import Edge
from controller.controller import ControlledAgent

class Logger:
    def __init__(self):
        AGENTS_COLUMNS = ["Step", "Name", "Emission", "Start", "End", "Has Arrived", "Roadtime", "Distance"]
        EDGES_COLUMNS = ["Step", "Name", "Total Length", "Lanes", "Occupied Length"]

        self.agents_data = pd.DataFrame(columns=AGENTS_COLUMNS)
        self.edges_data = pd.DataFrame(columns=EDGES_COLUMNS)


    def extract_data(self):
        self.agents_data.to_csv("../results/agents_data.csv")
        self.edges_data.to_csv("../results/edges_data.csv")


    def record_edge_state(self, edge:Edge, step) -> None:
        properties = edge.get_properties()

        occupied_length = 0
        for vehicle in properties["vehicule_list"]:
            occupied_length += vehicle.longueur

        occupied_length /= properties["Lanes"]

        row = {
            "Step": step,
            "Name": properties["name"],
            "Length": properties["Length"],
            "Lanes": properties["Lanes"],
            "Occupied Length": occupied_length
        }

        self.edges_data.loc[len(self.edges_data)] = row


    def record_agent_state(self, agent:ControlledAgent, step) -> None:
        properties = agent.get_properties()

        row = {
            "Step": step,
            "Name": properties["name"],
            "Emission": properties["emission"],
            "Start": properties["depart"].name,
            "End": properties["arrivee"].name,
            "Has Arrived": properties["terminate"],
            "Distance Traveled": properties["distance_parcourue"]
        }

        self.edges_data.loc[len(self.edges_data)] = row