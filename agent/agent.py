

class Agent:
    
    def __init__(self, name, **properties) -> None:
        self.name = name
        self.__dict__.update(properties)
        

    def get_properties(self):
        return self.__dict__.copy()