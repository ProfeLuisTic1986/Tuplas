import pygame, sys
pygame.init()

ANCHO_ALTO = (480, 640)
NOCHE = (20, 20, 35)
LUNA = (230, 230, 200)
NARANJA = (255, 140, 0)
NEGRO = (0, 0, 0)
TAM_CALABAZA = (40, 30)

pantalla = pygame.display.set_mode(ANCHO_ALTO)
reloj = pygame.time.Clock()

def dibujar_calabaza(pos):
    pygame.draw.ellipse(pantalla, NARANJA, (pos[0], pos[1], TAM_CALABAZA[0], TAM_CALABAZA[1]))
    pygame.draw.rect(pantalla, (20,120,20), (pos[0]+TAM_CALABAZA[0]//2-4, pos[1]-6, 8, 8))

pos_inicial = (ANCHO_ALTO[0]//2 - TAM_CALABAZA[0]//2, ANCHO_ALTO[1]//2 - TAM_CALABAZA[1]//2)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
    pantalla.fill(NOCHE)
    pygame.draw.circle(pantalla, LUNA, (60, 60), 35)
    dibujar_calabaza(pos_inicial)
    pygame.display.flip(); reloj.tick(60)