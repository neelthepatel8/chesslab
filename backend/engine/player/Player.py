class Player():
    def __init__(self):
        pass

    def opponent(self):
        pass
    
    def __eq__(self, value: object) -> bool:
        return type(self) == type(value)