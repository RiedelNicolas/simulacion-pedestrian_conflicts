import copy
import random

import numpy as np

import coordenada as c
import peaton as p
import semaforo as s
import auto as at
class Modelo :
    def __init__(self, _alto=5,_ancho=21, _tiempo_verde = 40, _lambda_peatones = 0.2, _lambda_autos = 0.07):
        self.alto = _alto*2 #Paso de metros a celdas.
        self.ancho = _ancho*2 #Paseo de metros a celdas.
        self.peatones = {}
        self.autos = []
        self.peatones_siguiente_turno = {} #estructura auxiliar.
        self.peatones_en_espera = 0
        self.autos_en_espera = 0
        self.cantidad_cruces = 0
        self.cantidad_conflictos = 0
        self.peatones_generados = 0
        self.turno_actual = 0
        self.cruces_verde = 0
        self.arribos_peatones = np.random.poisson(_lambda_peatones, 60*60)
        self.arribos_autos = np.random.poisson(_lambda_autos, 60*60)
        self.semaforo = s.Semaforo(_tiempo_verde) #el tiempo de un ciclo debe ser 90

    def imprimir(self) :
        print("Cantidad generados",self.peatones_generados)
        print("Cantidad de cruces",self.cantidad_cruces)
        print("En pantalla deberia haber",self.peatones_generados - self.cantidad_cruces)
        print("Autos en espera :", self.autos_en_espera)
        print("Cantidad de conflictos :", self.cantidad_conflictos)
        for i in self.autos :
            if i.salio == True : continue
            print("Hay un auto en el carril : ",i.carril)

        print("Estamos en el turno ", self.turno_actual)
        if self.semaforo.esta_verde() :
            print("El semaforo esta verde")
        else :
            print("El semaforo esta rojo")
        for y in range(0, self.alto):
            print()
            for x in range(0, self.ancho) :
                aux = c.Coordenada(x, y)
                if aux in self.peatones :
                    if self.peatones[aux].direccion == "d" :
                        print("\U0001F468",end="")
                    else:
                        print("\U0001F467",end="")
                elif self.hay_auto(aux) :
                    print("\U0001F697",end="")
                else :
                    print("\U0001F332", end="")
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


    def ingresar_peatones_en_espera (self) :

        if ( self.peatones_en_espera == 0 ) : return
        if( self.semaforo.esta_rojo() ) : return #No tiene que entrar nadie.
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

    def carril_ocupado_autos (self, carril) :
        for i in self.autos:
            if i.carril == carril: return True
        return False

    def ingresar_autos_en_espera(self):
        if self.autos_en_espera == 0 or self.semaforo.esta_verde() : return
        carriles_libres = []
        for i in range (0,6) :
            if not self.carril_ocupado_autos(i) :
                carriles_libres.append(i)
        random.shuffle(carriles_libres)
        i = 0
        while i < self.autos_en_espera and i < len(carriles_libres) :
            self.autos.append(at.Auto(carriles_libres[i]))
            i+=1
        self.autos_en_espera -= i

    def hay_auto (self, coor) : #devuelve true si hay un auto en esa posicion
        for i in self.autos :
            if i.ocupa(coor) : return True
        return False

    def limpiar_autos(self):
        aux = []
        for i in self.autos :
            if not i.salio :
                aux.append(i)

        self.autos = aux

    def avanzar_turno (self) :
        self.peatones_en_espera += self.arribos_peatones [self.turno_actual]
        self.autos_en_espera += self.arribos_autos[self.turno_actual]
        self.peatones = copy.deepcopy(self.peatones_siguiente_turno)
        self.peatones_siguiente_turno = {}
        self.ingresar_peatones_en_espera()
        self.ingresar_autos_en_espera()
        for key, value in self.peatones.items():
            value.avanzar(self)
        for i in self.autos :
            i.avanzar(self)
        self.turno_actual +=1
        self.semaforo.avanzar();

    def generar_matriz(self) :
        grid = [[], [], [], [], [], []]
        for y in range(0, self.alto):
            for x in range(0, self.ancho) :
                aux = c.Coordenada(x, y)
                if aux in self.peatones :
                    if self.peatones[aux].direccion == "d" :
                        grid[y][x] = 1
                    else:
                        grid[y][x] = 1
                elif self.hay_auto(aux) :
                    grid[y][x] = 2
                else :
                    grid[y][x] = 0