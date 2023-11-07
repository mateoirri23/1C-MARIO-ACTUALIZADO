import pygame, sys
from pygame.locals import *
from Class_Personaje import *
from Class_Enemigo import *
from configuraciones import *
from modo import *
from Class_Enemigo import *

def crear_plataforma(path, ancho, alto, x, y, es_visible):
    plataforma = {}
    
    if es_visible:
        plataforma["imagen"] = pygame.image.load(path)
    
        plataforma["imagen"] = pygame.transform.scale(plataforma["imagen"], (ancho,alto))
    else:
        plataforma["imagen"] = pygame.Surface((ancho, alto))
        
    plataforma["rectangulo"] = plataforma["imagen"].get_rect() 
    plataforma["rectangulo"].x = x
    plataforma["rectangulo"].y = y

    return plataforma

##############################INICIALIZACIONES##########################################

#############Pantalla##########
#ANCHO W - ALTO H
W,H = 1280,720
FPS = 18 #para desacelerar la pantalla

pygame.init()
RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((W,H)) # en pixeles

#Fondo
fondo = pygame.image.load(r"Corre\fondo.jpg").convert()#Acelera el juego y hace que consuma menos recursos
fondo = pygame.transform.scale(fondo, (W,H))

#PERSONAJE

diccionario = {}
diccionario["Quieto"] = personaje_quieto
diccionario["Derecha"] = personaje_corre
diccionario["Izquierda"] = personaje_camina_izquierda
diccionario["Salta"] = personaje_salta
diccionario["super"] = super_mario


mario = Personaje(diccionario, (70,60), 700,600,5)


#PLATAFORMAS

piso = crear_plataforma("",W,20,0,0,False)
piso["rectangulo"].top = mario.rectangulo_principal.bottom


plataforma_caño = crear_plataforma(r"Corre\Caño (2).png", 100,100,0,0,True)
plataforma_caño["rectangulo"].x = 850
plataforma_caño["rectangulo"].bottom = piso["rectangulo"].top

plataforma_invisible = crear_plataforma("",247,167,950,495,False)

plataformas = [piso, plataforma_caño,plataforma_invisible]

#ENEMIGO
diccionario_enemigo = {}
diccionario_enemigo["izquierda"] = enemigo_camina
diccionario_enemigo["aplasta"] = enemigo_aplasta
coopa = Enemigo(diccionario_enemigo)
coopa.rectangulo.bottom = piso["rectangulo"].top
        
d = {"aplastado": diccionario_enemigo["aplasta"]}
reescalar_imagenes(d,50,50)


# d = {diccionario_enemigo["aplasta"]}
# reescalar_imagenes(d,50,50)

lista_enemigos = Enemigo.crear_lista(piso)

# PREMIO
premio = crear_plataforma("",70,50,703,439,False)
flor = {}
flor["superficie"] = flor_fuego[0]
flor["superficie"] = pygame.transform.scale(flor["superficie"], (80,80))
flor["rectangulo"] = flor["superficie"].get_rect()
flor["rectangulo"].bottom = premio["rectangulo"].top
flor["descubierta"] = False
flor["tocada"] = False

while True:
    RELOJ.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit(0)
        # elif evento.type == pygame.MOUSEBUTTONDOWN:
        #     print(evento)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                cambiar_modo()
    keys = pygame.key.get_pressed()


    if(keys[pygame.K_RIGHT]):
        mario.que_hace = "Derecha"
    elif(keys[pygame.K_LEFT]):
        mario.que_hace = "Izquierda"
    elif(keys[pygame.K_SPACE]):
        mario.que_hace = "Salta"
    else:
        mario.que_hace = "Quieto"
        
    PANTALLA.blit(fondo,(0,0))
    PANTALLA.blit(plataforma_caño["imagen"], plataforma_caño["rectangulo"])
    
    # for enemigo in lista_enemigos:
    #     enemigo.actualizar(PANTALLA)
    # mario.colision_enemigo()
    
    # for enemigo in lista_enemigos:
    #     if enemigo.esta_muerto:
    #         del enemigo
    #         break
    
    mario.actualizar(PANTALLA, plataformas)
    #mario.verificar_colision_flor(flor)
    coopa.actualizar(PANTALLA) # ENEMIGO
    
    if get_mode() == True:
        pygame.draw.rect(PANTALLA,"green",mario.rectangulo_principal,3)
        for plataforma in plataformas:
            pygame.draw.rect(PANTALLA,"blue",plataforma["rectangulo"],3)
        pygame.draw.rect(PANTALLA,"red",plataforma_caño["rectangulo"],3)
        pygame.draw.rect(PANTALLA,"red",premio["rectangulo"],3) 
        #for enemigo in lista_enemigos:
             #pygame.draw.rect(PANTALLA,"orange",enemigo,3)

           

    
    pygame.display.update()