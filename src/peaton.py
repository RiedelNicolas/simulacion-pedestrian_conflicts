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