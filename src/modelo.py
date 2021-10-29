import coordenada as c
import peaton as p

class Modelo :
    def __init__(self, _alto=5,_ancho=21):
        self.alto = _alto*2 #Paso de metros a celdas.
        self.ancho = _ancho*2 #Paseo de metros a celdas.
        self.peatones = {}
        self.espera_peatones = 3


    def imprimir(self) :
        print()
        print(self.peatones)
        for y in range(0, self.alto):
            print()
            for x in range(0, self.ancho) :
                aux = c.Coordenada(x, y)
                if (aux in self.peatones) :
                    print("p",end="")
                else :
                    print("-",end="")
        print()

    #En un principio vamos a meter solo peatones por la derecha.
    def ingresar_en_espera(self) :

        self.peatones[c.Coordenada(0,0)] = p.Peaton(c.Coordenada(0,0),"d")
        self.peatones[c.Coordenada(0,1)] = p.Peaton(c.Coordenada(0,1),"d")
        self.peatones[c.Coordenada(0,3)] = p.Peaton(c.Coordenada(0,3),"d")
