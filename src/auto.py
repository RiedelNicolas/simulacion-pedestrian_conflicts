import coordenada as cor

class Auto :
    def __init__(self, _carril) :
        self.posiciones = []
        self.carril = _carril
        self.tope_izq = _carril*7 + 1
        self.tope_der = _carril *7 + 5
        self.velocidad = 10 #Cuadraditos por segundo
        self.salio = False

    def peatones_adelante(self, modelo) :
        # El borde del auto arranca en (carril*7 +1) y termina en (carril*7 +5)
        if  len(self.posiciones) == 0  and self.salio == False :
            for i in range ( self.tope_izq, self.tope_der+1 ):
                for j in range (0, 10) :
                    aux = cor.Coordenada (i,j)
                    if aux in modelo.peatones_siguiente_turno : #Hay un peaton en esa posicion.
                        modelo.cantidad_conflictos +=1
                        return True
        return False

    def avanzar (self, modelo) :
        if self.peatones_adelante(modelo) : return  #No se puede avanzar
        if  len(self.posiciones) == 0  and self.salio == False: #Primer movimiento.
            for i in range (self.tope_izq, self.tope_der+1) :
                for j in range ( 4, 10) :
                    self.posiciones.append( cor.Coordenada(i,j) )
        else :
            self.posiciones = [] #Se fue del carril.
            self.salio = True
            self.carril = -1 #Se fue

    def ocupa(self, coordenada) : #devuelve true si el auto esta ocupado esa coordenada
        for i in self.posiciones :
            if i == coordenada : return True
        return False
