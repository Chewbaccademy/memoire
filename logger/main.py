import pandas as pd

from graph.main import Edge
# from controller.controller import ControlledAgent

class Logger:
    def __init__(self):
        AGENTS_COLUMNS = ["Step", "Step Duration", "Name", "Emission By Kilometer (running)", "Emission By Minute (idle)", "Consumption", "Start", "End", "Position", "Has Arrived", "Distance Traveled"]
        EDGES_COLUMNS = ["Step", "Step Duration", "Name", "Length", "Lanes", "Occupied Length"]

        self.agents_data = pd.DataFrame(columns=AGENTS_COLUMNS)
        self.edges_data = pd.DataFrame(columns=EDGES_COLUMNS)


    def extract_data(self):
        self.agents_data.to_csv("results/agents_data.csv")
        self.edges_data.to_csv("results/edges_data.csv")


    def record_edge_state(self, edge:Edge, step:int, time_slice:float) -> None:
        properties = edge.get_properties()

        occupied_length = 0
        for vehicle in properties["vehicule_list"]:
            occupied_length += vehicle.length

        occupied_length /= properties["lanes"]

        row = {
            "Step": step,
            "Step Duration": time_slice,
            "Name": properties["name"],
            "Length": properties["length"],
            "Lanes": properties["lanes"],
            "Occupied Length": occupied_length
        }

        self.edges_data.loc[len(self.edges_data)] = row


    def record_agent_state(self, agent, step:int, time_slice:float) -> None:
        properties = agent.get_properties()

        row = {
            "Step": step,
            "Step Duration": time_slice,
            "Name": properties["name"],
            "Emission By Kilometer (running)": properties["emission"],
            "Emission By Minute (idle)": properties["emission_idle"],
            "Consumption": properties["consumption"],
            "Start": properties["depart"].name,
            "End": properties["arrivee"].name,
            "Position": properties["current_place"],
            "Has Arrived": properties["terminate"],
            "Distance Traveled": properties["distance_parcourue"]
        }

        self.agents_data.loc[len(self.agents_data)] = row