import pygame
import time
from random import randrange
import modelo as tp
import csv










pygame.init()


x = tp.Modelo()
x.avanzar_turno()
  








height = 10
width = 42
window = pygame.display.set_mode((1360 ,210)) #Mi monitor es chico, cambio un pco la reso
block_size = 20





turno = 0
myfont = pygame.font.SysFont("Comic Sans MS", 25)


autos_en_espera = x.autos_en_espera
cantidad_cruces = x.cantidad_cruces

cantidad_cruces_seg = x.cantidad_cruces

cruces_verde = x.cruces_verde


peaton_espera = x.peatones_en_espera
cantidad_conflictos = x.cantidad_conflictos
step = 0.5

while True:
    grid = x.generar_matriz()

    for fila in range(height):
        for columna in range(width):
            rect = pygame.Rect(columna*(block_size+1) + 120, fila*(block_size+1), block_size, block_size)
            pygame.draw.rect(window, (255,255,255), rect)
            if (grid[fila][columna] == 1):
                rect = pygame.Rect(columna*(block_size+1) + 120, fila*(block_size+1), block_size, block_size)
                pygame.draw.rect(window, (255,0,0), rect)
            if (grid[fila][columna] == 2):
                rect = pygame.Rect(columna*(block_size+1) + 120, fila*(block_size+1), block_size, block_size)
                pygame.draw.rect(window, (0,0,255), rect)
            


    
        
    
    
    
    
    
    grid_copy = [[],[],[],[],[],[], [], [], [], []]
    
    for fila in range(10):
        for columna in range(42):
            grid_copy[fila].append(0)
    for fila in range(10):
        for columna in range(42):
            if (grid[fila][columna] == 1):
                if (columna + 1 < 42):
                    grid_copy[fila][columna + 1] = 1
    
    x.avanzar_turno()



    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                step += 0.01
            if event.key == pygame.K_s  and step > 0.01:
                step -= 0.01

    #borro actual
    label_semasforo = myfont.render("verde", 1, (0,0,0))
    window.blit(label_semasforo, (20, 60))
    label_semasforo = myfont.render("rojo", 1, (0,0,0))
    window.blit(label_semasforo, (20, 60))
    if(x.semaforo.esta_verde()):
        label_semasforo = myfont.render("verde", 1, (0,255,0))
        window.blit(label_semasforo, (20, 60))
    else:
        label_semasforo = myfont.render("rojo", 1, (255,0,0))
        window.blit(label_semasforo, (20, 60))
    
    #borro actual
    label_turno = myfont.render("turno: "+str(turno), 1, (0,0,0))
    window.blit(label_turno, (20, 30))
    #actualizo turno
    turno +=1
    #dibujo nuevo turno
    label_turno = myfont.render("turno: "+str(turno), 1, (0,255,0))
    window.blit(label_turno, (20, 30))

    

    #borro actual
    label_peatones = myfont.render("peaton espera: "+str(peaton_espera), 1, (0,0,0))
    window.blit(label_peatones, (1100, 90))

    peaton_espera = x.peatones_en_espera

    #dibujo nuevo turno
    label_peatones = myfont.render("peaton espera: "+str(peaton_espera), 1, (0,255,0))
    window.blit(label_peatones, (1100, 90))
    
    


    #borro actual
    label_conflictos = myfont.render("conflictos: "+str(cantidad_conflictos), 1, (0,0,0))
    window.blit(label_conflictos, (1100, 120))

    cantidad_conflictos = x.cantidad_conflictos
    #dibujo nuevo turno
    label_conflictos = myfont.render("conflictos: "+str(cantidad_conflictos), 1, (0,255,0))
    window.blit(label_conflictos, (1100, 120))

    




    #borro actual
    label_autos = myfont.render("autos espera: "+str(autos_en_espera), 1, (0,0,0))
    window.blit(label_autos, (1100, 150))

    autos_en_espera = x.autos_en_espera
    #dibujo nuevo turno
    label_autos = myfont.render("autos espera: "+str(autos_en_espera), 1, (0,255,0))
    window.blit(label_autos, (1100, 150))



    #borro actual
    label_cruces = myfont.render("cantidad cruces: "+str(cantidad_cruces), 1, (0,0,0))
    window.blit(label_cruces, (1100, 60))

    cantidad_cruces = x.cantidad_cruces
    #dibujo nuevo turno
    label_cruces = myfont.render("cantidad cruces: "+str(cantidad_cruces), 1, (0,255,0))
    window.blit(label_cruces, (1100, 60))



    #borro actual
    label_cruces_por_seg = myfont.render("cantidad cruces/seg: "+str(round(cantidad_cruces_seg/turno, 1)), 1, (0,0,0))
    window.blit(label_cruces_por_seg, (1100, 5))

    cantidad_cruces_seg = x.cantidad_cruces
    #dibujo nuevo turno
    label_cruces_por_seg = myfont.render("cantidad cruces/seg: "+str(round(cantidad_cruces_seg/turno, 1)), 1, (0,255,0))
    window.blit(label_cruces_por_seg, (1100, 5))



    #borro actual
    label_cruces_verde = myfont.render("cruces verde: "+str(cruces_verde), 1, (0,0,0))
    window.blit(label_cruces_verde, (1100, 30))

    cruces_verde = x.cruces_verde
    #dibujo nuevo turno
    label_cruces_verde = myfont.render("cruces verde: "+str(cruces_verde), 1, (0,255,0))
    window.blit(label_cruces_verde, (1100, 30))








    grid = grid_copy
    pygame.display.update()
    time.sleep(step)
