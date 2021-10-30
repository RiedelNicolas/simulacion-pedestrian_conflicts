class Coordenada :
    def __init__(self, _x = 0, _y= 0) :
        self.x = _x
        self.y = _y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def distancia(self, other) :
        return  abs(self.x - other.x) + abs(self.y - other.y)