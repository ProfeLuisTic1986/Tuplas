import pygame, sys
pygame.init()

ANCHO_ALTO = (480, 640)
CENTRO = (ANCHO_ALTO[0]//2, ANCHO_ALTO[1]//2)
NOCHE = (18, 18, 32)
LUNA = (230, 230, 200)
NARANJA = (255, 140, 0)
HUESO = (235, 235, 235)
TAM_CALABAZA = (35, 25)

pantalla = pygame.display.set_mode(ANCHO_ALTO)
reloj = pygame.time.Clock()

def dibujar_calabaza(pos):
    x, y = pos
    w, h = TAM_CALABAZA
    # cuerpo
    pygame.draw.ellipse(pantalla, NARANJA, (x, y, w, h))
    # rabito (tallo)
    pygame.draw.rect(pantalla, (20, 120, 20), (x + w//2 - 3, y - 5, 6, 6))
    
pos_inicial = (CENTRO[0] - TAM_CALABAZA[0]//2, ANCHO_ALTO[1] - 100)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
    pantalla.fill(NOCHE)
    pygame.draw.circle(pantalla, LUNA, (ANCHO_ALTO[0]-70, 70), 40)
    dibujar_calabaza(pos_inicial)
    pygame.display.flip(); reloj.tick(60)