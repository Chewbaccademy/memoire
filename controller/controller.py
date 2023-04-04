from agent.agent import Agent
from graph.main import Node


class ControlledAgent(Agent):
    
    def __init__(self, name, **properties) -> None:
        super().__init__(name, **properties)