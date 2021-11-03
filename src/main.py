import modelo as tp
import csv

def main () :
    x = tp.Modelo()
    x.avanzar_turno()
    x.imprimir()
    leido = input("Desea simular otro turno? Y/N")
    while (leido != "N") :
        x.avanzar_turno()
        x.imprimir()
        print(x.generar_matriz())
        leido = input("Desea simular otro turno? Y/N")

main()

