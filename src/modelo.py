import copy
import random

import numpy as np

import coordenada as c
import peaton as p

class Modelo :
    def __init__(self, _alto=5,_ancho=21):
        self.alto = _alto*2 #Paso de metros a celdas.
        self.ancho = _ancho*2 #Paseo de metros a celdas.
        self.peatones = {}
        self.peatones_siguiente_turno = {} #estructura auxiliar.
        self.peatones_en_espera = 0
        self.cantidad_cruces = 0
        self.peatones_generados = 0
        self.turno_actual = 0
        self.arribos_peatones = arribos = np.random.poisson(0.5, 60*60)

    def imprimir(self) :
        print("Cantidad generados",self.peatones_generados)
        print("Cantidad de cruces",self.cantidad_cruces)
        print("En pantalla deberia haber",self.peatones_generados - self.cantidad_cruces)
        for y in range(0, self.alto):
            print()
            for x in range(0, self.ancho) :
                aux = c.Coordenada(x, y)
                if aux in self.peatones :
                    if self.peatones[aux].direccion == "d" :
                        print("\U0001F468",end="")
                    else:
                        print("\U0001F467",end="")
                else :
                    print("\U0001F332",end="")
        print()

    #En un principio vamos a meter solo peatones por la derecha.
    def ingresar_peaton(self, posicion) :
        self.peatones_generados +=1;
        if ( posicion in self.peatones) :
            raise ValueError("intentaste ingresar un peaton en una posicion ocupada")
        if not ( posicion.x == 0 or posicion.x == (self.ancho-1) ) :
            raise ValueError("los peatones solo pueden ser ingresados en los bordes")
        if (posicion.x == 0):
            self.peatones[posicion] = p.Peaton(posicion, "d")
        elif (posicion.x == (self.ancho-1) ):
            self.peatones[posicion] = p.Peaton(posicion, "i")
        else :
            raise ValueError("Error desconocido ingresando peaton")


    def ingresar_en_espera (self) :
        if (self.peatones_en_espera == 0 ) : return

        lugares_disponibles = []

        for i in range (0, self.alto) :
            aux = c.Coordenada(0,i)
            if (aux not in self.peatones) : #si el lugar esta disponible
                lugares_disponibles.append(aux)

        for i in range (0, self.alto) :
            aux = c.Coordenada(self.ancho-1,i)
            if (aux not in self.peatones) : #si el lugar esta disponible
                lugares_disponibles.append(aux)

        random.shuffle(lugares_disponibles)
        i = 0
        while (i < self.peatones_en_espera and i < len(lugares_disponibles) ) :
             self.ingresar_peaton(lugares_disponibles[i]);
             i+=1

        self.peatones_en_espera -= i

    def avanzar_turno (self) :
        self.peatones_en_espera += self.arribos_peatones [self.turno_actual]
        self.peatones = copy.deepcopy(self.peatones_siguiente_turno)
        self.peatones_siguiente_turno = {}
        self.ingresar_en_espera()
        for key, value in self.peatones.items():
            value.avanzar(self)
        self.turno_actual +=1