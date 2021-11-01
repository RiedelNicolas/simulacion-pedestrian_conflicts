class Semaforo :
    def __init__(self, _verde):
        self.verde = _verde
        self.contador = 0

    def avanzar(self) :
        self.contador +=1

    def esta_verde(self) : #devuelve true o false
        aux = self.contador%90 #un poquito de aritmetica modular.
        if aux < self.verde : return True
        return False

    def esta_rojo(self) : #devuelve true o false
        return not self.esta_verde()