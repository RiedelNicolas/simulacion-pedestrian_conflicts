import coordenada as cor
import numpy as np

#Funcion que define la velocidad inicial
def velocidad_inicial_peaton():
  p = np.random.random_sample()
  if p > 0 and p <= 0.273:
    return 2
  elif p > 0.273 and p <=0.793:
    return 3
  elif p > 0.793 and p <= 0.93:
    return 4
  elif p > 0.93 and p <= 0.978:
    return 5
  elif p > 0.978:
    return 6


class Peaton :
    def __init__(self, _posicion, _direccion):
        self.posicion = _posicion
        self.direccion = _direccion
        self.vel_base = velocidad_inicial_peaton()
        self.vel_turno = self.vel_base

    def calcular_velocidad_turno(self, modelo):
        if self.direccion == "d" :
            if self.posicion.x == (modelo.ancho-1) : return self.vel_base #Es imposible que tenga uno adelante.

            for i in range (self.posicion.x+1, modelo.ancho) :
                aux = cor.Coordenada(i, self.posicion.y);
                if (aux in modelo.peatones) : #El primero que encuentre es el que tengo mas cerca.
                    distancia = aux.distancia(self.posicion)
                    return min(self.vel_base, distancia-1) #Distancia-1 es la cantidad de espacios en el medio.

        if self.direccion == "i" :
            raise ValueError("Direccion izquierda aun no implementada")
            return 5;

        return self.vel_base #no tenia a nadie adelante.

    ## Logica de implementar su movimiento.
    def avanzar (self, modelo) :
        self.vel_turno = self.calcular_velocidad_turno(modelo);
        if not self.cambia_carril() :
            if (self.direccion == "d") : self.avanzar_derecha(modelo)
            if (self.direccion == "i") : self.avanzar_izquierda(modelo)
        return

    def avanzar_derecha(self, modelo):
        aux = cor.Coordenada(self.posicion.x + self.vel_turno, self.posicion.y)
        if aux.x >= modelo.ancho:
            modelo.cantidad_cruces += 1
            return  # llego a la meta, en el siguiente turno no esta en el mapa.
        else: #insertamos en el map secundario.
            if aux not in modelo.peatones_siguiente_turno :
                self.posicion = aux
                modelo.peatones_siguiente_turno[self.posicion] = self
            else: #La posicion ya estaba ocupada, me quedo quieto.
                modelo.peatones_siguiente_turno[self.posicion] = self

    def avanzar_izquierda(self, modelo) :
        aux = cor.Coordenada(self.posicion.x - self.vel_turno, self.posicion.y)
        if aux.x < 0:
            modelo.cantidad_cruces += 1
            return  # llego a la meta, en el siguiente turno no esta en el mapa.
        else: #insertamos en el map secundario.
            if aux not in modelo.peatones_siguiente_turno :
                self.posicion = aux
                modelo.peatones_siguiente_turno[self.posicion] = self
            else: #La posicion ya estaba ocupada, me quedo quieto.
                modelo.peatones_siguiente_turno[self.posicion] = self

    def cambia_carril(self): # Devuelve true si efectivamente debe cabiar de carril.
        return False
