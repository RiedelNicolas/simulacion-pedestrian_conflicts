import modelo as tp
import csv

import modelo as tp
import csv

def main () :
    f = open ("relacion-arribo_autos-conflitos.csv", "w")
    writer = csv.writer(f)
    autos_por_hora = [0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.20 ]
    header = ["autos_por_hora", "conflictos"]
    writer.writerow(header)

    print("Relacion entre arribo de autos y cantidad de conflictos")
    for i in autos_por_hora :
        x = tp.Modelo(5, 21, 50, 0.4, i)
        for j in range(0,3600) :
            x.avanzar_turno()
        print("Se finalizo esta simulacion")
        print("Se obtuvo conflictos",x.cantidad_conflictos)
        writer.writerow([i,x.cantidad_conflictos])
main()

#x.avanzar_turno()
#x.imprimir()
#leido = input("Desea simular otro turno? Y/N")

# for i in range (0, 3600) :
# x.avanzar_turno()
# x.imprimir()