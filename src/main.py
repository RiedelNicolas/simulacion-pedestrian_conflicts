import modelo as tp
import csv

def main () :
    f = open ("relacion-tiempo_verde-conflitos.csv", "w")
    writer = csv.writer(f)

    header = ["peatones_por_hora","conflictos"]
    writer.writerow(header)

    arribo_peatones = [100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000]

    print("Relacion entre conflictos peaton/vehiculo y arribo de peatones")
    print ("Arribo autos 0.07")
    for i in arribo_peatones :
        print("1)Personas por hora:",i)
        print("1) 0.07 arribo de vehiculos por segundo")
        x = tp.Modelo(5, 21, 40, i/3600, 0.07)
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