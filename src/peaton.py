import copy
import random

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
            if self.posicion.x == 0 : return self.vel_base #Es imposible que tenga uno adelante.

            for i in range (self.posicion.x-1, (0-1) , -1) : #Mi posicion obviamente no incluida
                aux = cor.Coordenada(i, self.posicion.y);
                if (aux in modelo.peatones) : #El primero que encuentre es el que tengo mas cerca.
                    distancia = aux.distancia(self.posicion)
                    return min(self.vel_base, distancia-1) #Distancia-1 es la cantidad de espacios en el medio.


        return self.vel_base #no tenia a nadie adelante.

    #En caso de que la posicion nueva se encuentre ocupada me quedo quieto.
    def mover_a (self, modelo, posicion_nueva) :
        if(posicion_nueva.x >= modelo.ancho or posicion_nueva.x < 0 or
            posicion_nueva.y<0 or posicion_nueva.y >= modelo.alto):
            raise ValueError("Se intento mover a una posicion invalida")

        aux = copy.deepcopy(self)
        if posicion_nueva not in modelo.peatones_siguiente_turno:
            aux.posicion = posicion_nueva
            modelo.peatones_siguiente_turno[aux.posicion] = aux
        else:  # La posicion ya estaba ocupada, me quedo quieto.
            modelo.peatones_siguiente_turno[aux.posicion] = aux


    ## Logica de implementar su movimiento.
    def avanzar (self, modelo) :
        self.vel_turno = self.calcular_velocidad_turno(modelo);
        if not self.cambia_carril(modelo) :
            if (self.direccion == "d") : self.avanzar_derecha(modelo)
            if (self.direccion == "i") : self.avanzar_izquierda(modelo)
        return

    def avanzar_derecha(self, modelo):
        aux = cor.Coordenada(self.posicion.x + self.vel_turno, self.posicion.y)
        if aux.x >= modelo.ancho:
            modelo.cantidad_cruces += 1
            return  # llego a la meta, en el siguiente turno no esta en el mapa.
        else: #insertamos en el map secundario.
            self.mover_a(modelo, aux)

    def avanzar_izquierda(self, modelo) :
        aux = cor.Coordenada(self.posicion.x - self.vel_turno, self.posicion.y)
        if aux.x < 0:
            modelo.cantidad_cruces += 1
            return  # llego a la meta, en el siguiente turno no esta en el mapa.
        else: #insertamos en el map secundario.
            self.mover_a(modelo, aux)

    def arriba_disponible (self, modelo) :
        arriba = cor.Coordenada(self.posicion.x,
                                self.posicion.y - 1)
        if(arriba.y < 0 ) : return False
        if (arriba in modelo.peatones): return False
        return True

    def abajo_disponible (self, modelo) :
        abajo = cor.Coordenada(self.posicion.x,
                                self.posicion.y + 1)
        if(abajo.y >= modelo.alto ) : return False
        if (abajo in modelo.peatones): return False
        return True

    def cambia_carril(self, modelo): # Devuelve true si efectivamente debe cabiar de carril. Efectua el cambio de carril.

        if self.vel_turno != 0 : return False #No esta bloquedo.

        puede_arriba = False
        puede_abajo = False
        #Evaluo si se le permite cambiar arriba.
        if self.arriba_disponible(modelo): #Si la posicion de arriba esta vacia o es valida.
            fila = []# Buscamos toda la fila superior (Menos con el que recorremos)
            for i in range(0, modelo.ancho) :
                aux = cor.Coordenada (i, self.posicion.y-1)
                if (aux in modelo.peatones and aux != self.posicion ) :  fila.append(aux)

            min_distancia = 100 # un maximo absurdo, mi idea es buscar con el que tengo minima distancia.
            min_coor = fila[0] #cargo una cualquiera, se va a sobrescribir.
            for i in fila :
              if( i.distancia(cor.Coordenada(self.posicion.x, self.posicion.y-1)) < min_distancia ):
                  min_distancia = i.distancia(cor.Coordenada(self.posicion.x, self.posicion.y-1))
                  min_coor = i
            if  (min_distancia-1) > self.vel_base :
                if (modelo.peatones[min_coor].vel_base < self.vel_base) :
                    puede_arriba = True

        #Evaluo si se le permite cambiar a abajo :
        if self.abajo_disponible(modelo): #Si la posicion de abajo esta vacia o es valida.
            fila = []# Buscamos toda la fila superior (Menos con el que recorremos)
            for i in range(0, modelo.ancho) :
                aux = cor.Coordenada (i, self.posicion.y+1)
                if (aux in modelo.peatones and aux != self.posicion ) :  fila.append(aux)

            min_distancia = 100 # un maximo absurdo, mi idea es buscar con el que tengo minima distancia.
            min_coor = cor.Coordenada(0,0) #cargo una cualquiera, se va a sobrescribir.
            for i in fila :
              if( i.distancia(cor.Coordenada(self.posicion.x, self.posicion.y+1)) < min_distancia ):
                  min_distancia = i.distancia(cor.Coordenada(self.posicion.x, self.posicion.y+1))
                  min_coor = i
            if  (min_distancia-1) > self.vel_base :
                if (modelo.peatones[min_coor].vel_base < self.vel_base) :
                    puede_abajo = True

        if puede_arriba and puede_abajo :
            if random.random() > 0.5 : #Mueve arriba
                aux = cor.Coordenada(self.posicion.x, self.posicion.y -1)
                self.mover_a(modelo, aux)
            else : #mueve abajo
                aux = cor.Coordenada(self.posicion.x, self.posicion.y + 1)
                self.mover_a(modelo, aux)
            return True
        if puede_arriba :
            aux = cor.Coordenada(self.posicion.x, self.posicion.y - 1)
            self.mover_a(modelo, aux)
            return True
        if puede_abajo :
            aux = cor.Coordenada(self.posicion.x, self.posicion.y + 1)
            self.mover_a(modelo, aux)
            return True
        return False #no entro a ninguna condicion, no hace cambio de carril.