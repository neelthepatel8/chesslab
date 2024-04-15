class Player():
    def __init__(self):
        self.color = None

    def opponent(self):
        return Player()
    
    def __eq__(self, value: object) -> bool:
        return type(self) == type(value)
    
    def __str__(self):
        return "none"