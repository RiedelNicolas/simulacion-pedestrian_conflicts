import modelo as tp
def main () :
    x = tp.Modelo() #Instanciamos
    #x.avanzar_turno()
    #x.imprimir()
    print ("Ingrese un caracter para comenzar")
    print ("Ingrese N para finalizar")
    leido = input("")

    #while leido != "N" or leido =="n" :

    """print("Simulando el turno",x.turno_actual)
    x.avanzar_turno()
    x.imprimir()
    leido = input("Desea simular otro turno? Y/N") """

    for i in range (0, 3600) :
        x.avanzar_turno()
        x.imprimir()
main()


