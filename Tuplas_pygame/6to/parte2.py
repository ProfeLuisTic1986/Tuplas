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
VEL_JUGADOR, NUM_ENEMIGOS, VEL_MIN, VEL_MAX = VELOCIDADES

pantalla = pygame.display.set_mode(ANCHO_ALTO)
reloj = pygame.time.Clock()

def rect_tupla(pos, tam):
    # Devuelve (x, y, w, h) a partir de dos tuplas
    return (*pos, *tam)

jugador_pos = [ANCHO_ALTO[0]//2 - TAM_CALABAZA[0]//2, ANCHO_ALTO[1] - 80]

def dibujar_calabaza(pos):
    # Cuerpo
    pygame.draw.ellipse(pantalla, NARANJA, rect_tupla(pos, TAM_CALABAZA))
    # Rabito (tallo)
    x, y = pos; w, h = TAM_CALABAZA
    pygame.draw.rect(pantalla, (20, 120, 20), (x + w//2 - 4, y - 6, 8, 8))

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * VEL_JUGADOR
    dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * VEL_JUGADOR

    jugador_pos[0] += dx
    jugador_pos[1] += dy

    jugador_pos[0] = max(0, min(ANCHO_ALTO[0]-TAM_CALABAZA[0], jugador_pos[0]))
    jugador_pos[1] = max(0, min(ANCHO_ALTO[1]-TAM_CALABAZA[1], jugador_pos[1]))

    pantalla.fill(NOCHE)
    pygame.draw.circle(pantalla, LUNA, (ANCHO_ALTO[0]-70, 70), 40)
    dibujar_calabaza(jugador_pos)

    pygame.display.flip()
    reloj.tick(60)