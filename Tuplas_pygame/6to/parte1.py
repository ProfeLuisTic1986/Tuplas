import pygame, sys
pygame.init()

CONFIG = (
    (480, 640),
    ((15,15,30),(230,230,200),(255,140,0),(255,255,255),(120,70,200)),
    ((40,30),(32,26)),
    (6, 4, 3, 7)
)
ANCHO_ALTO, COLORES, TAMAÑOS, VELOCIDADES = CONFIG
NOCHE, LUNA, NARANJA, BLANCO, MORADO = COLORES
TAM_CALABAZA, TAM_BRUJA = TAMAÑOS

pantalla = pygame.display.set_mode(ANCHO_ALTO)
reloj = pygame.time.Clock()

def dibujar_calabaza(pos):
    x, y = pos
    w, h = TAM_CALABAZA
    pygame.draw.ellipse(pantalla, NARANJA, (x, y, w, h))
    pygame.draw.rect(pantalla, (20, 120, 20), (x + w//2 - 4, y - 6, 8, 8))
    
    
pos_inicial = (ANCHO_ALTO[0]//2 - TAM_CALABAZA[0]//2, ANCHO_ALTO[1]//2 - TAM_CALABAZA[1]//2)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
    pantalla.fill(NOCHE)
    pygame.draw.circle(pantalla, LUNA, (ANCHO_ALTO[0]-70, 70), 40)
    dibujar_calabaza(pos_inicial)
    pygame.display.flip(); reloj.tick(60)