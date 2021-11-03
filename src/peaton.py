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
            posicion_nueva.y < 0 or posicion_nueva.y >= modelo.alto):
            raise ValueError("Se intento mover a una posicion invalida")

        aux = copy.deepcopy(self)

        if posicion_nueva in modelo.peatones_siguiente_turno:
            modelo.peatones_siguiente_turno[aux.posicion] = aux  #me quedo quieto, la posicion ya estaba ocupada
            return
        if modelo.hay_auto(posicion_nueva):
            modelo.peatones_siguiente_turno[aux.posicion] = aux  #Habia un auto, entonces me quedo quieto
            modelo.cantidad_conflictos += 1
            return

        #si llego aca es porque me tengo que mover
        aux.posicion = posicion_nueva
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
            if modelo.semaforo.esta_verde()  :
                modelo.cruces_verde +=1
            return  # llego a la meta, en el siguiente turno no esta en el mapa.
        else: #insertamos en el map secundario.
            self.mover_a(modelo, aux)

    def avanzar_izquierda(self, modelo) :
        aux = cor.Coordenada(self.posicion.x - self.vel_turno, self.posicion.y)
        if aux.x < 0:
            modelo.cantidad_cruces += 1
            if modelo.semaforo.esta_verde()  :
                modelo.cruces_verde +=1
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

    def puede_cambiar_arriba(self, modelo): #devuelve true si se puede cambiar de carril arriba
        if not self.arriba_disponible(modelo) : return False
        fila = []  # Buscamos toda la fila superior
        for i in range(0, modelo.ancho):
            aux = cor.Coordenada(i, self.posicion.y - 1)
            if aux in modelo.peatones :  fila.append(aux)

        if( len (fila) == 0 ) : return True # La fila de arriba esta vacia, puedo cambiar.

        min_distancia = 100  # un maximo absurdo, mi idea es buscar con el que tengo minima distancia.
        min_coor = fila[0]  # cargo una cualquiera, se va a sobrescribir.
        for i in fila:
            if i.distancia(cor.Coordenada(self.posicion.x, self.posicion.y - 1)) < min_distancia :
                min_distancia = i.distancia(cor.Coordenada(self.posicion.x, self.posicion.y - 1))
                min_coor = i
        if (min_distancia - 1) > self.vel_base:
            if (modelo.peatones[min_coor].vel_base < self.vel_base):
                return True
        return False #no puede cambiar...


    def puede_cambiar_abajo(self, modelo): #devuelve true si se puede cambiar de carril arriba
        #Evaluo si se le permite cambiar a abajo :
        if not self.abajo_disponible(modelo): return False
        fila = []# Buscamos toda la fila inferior
        for i in range(0, modelo.ancho) :
            aux = cor.Coordenada (i, self.posicion.y+1)
            if (aux in modelo.peatones ) :  fila.append(aux)

        if( len (fila) == 0 ) : return True # La fila de abajo esta vacia, puedo cambiar.

        min_distancia = 100 # un maximo absurdo, mi idea es buscar con el que tengo minima distancia.
        min_coor = cor.Coordenada(0,0) #cargo una cualquiera, se va a sobrescribir.
        for i in fila :
          if( i.distancia(cor.Coordenada(self.posicion.x, self.posicion.y+1)) < min_distancia ):
              min_distancia = i.distancia(cor.Coordenada(self.posicion.x, self.posicion.y+1))
              min_coor = i
        if  (min_distancia-1) > self.vel_base :
            if (modelo.peatones[min_coor].vel_base < self.vel_base) :
                return True
        return False #No se cumplio ninguna condicion


    def cambia_carril(self, modelo): # Devuelve true si efectivamente debe cabiar de carril. Efectua el cambio de carril.

        if self.vel_turno != 0 : return False #No esta bloquedo.

        puede_arriba = self.puede_cambiar_arriba(modelo)
        puede_abajo = self.puede_cambiar_abajo(modelo)

        if puede_arriba and puede_abajo :
            if random.random() > 0.5 : #Tiro una moneda
                aux = cor.Coordenada(self.posicion.x, self.posicion.y -1) #mueve arriba
                self.mover_a(modelo, aux)
            else : #mueve abajo
                aux = cor.Coordenada(self.posicion.x, self.posicion.y + 1)
                self.mover_a(modelo, aux)
            return True
        if puede_arriba : # En este caso solo puede arriba
            aux = cor.Coordenada(self.posicion.x, self.posicion.y - 1)
            self.mover_a(modelo, aux)
            return True
        if puede_abajo :
            aux = cor.Coordenada(self.posicion.x, self.posicion.y + 1)
            self.mover_a(modelo, aux)
            return True
        return False #no entro a ninguna condicion, no hace cambio de carril.