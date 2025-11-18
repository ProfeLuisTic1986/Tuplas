import pygame, random, sys
pygame.init()

# Perfiles de configuración en TUPLAS ANIDADAS: (ANCHO_ALTO, COLORES, TAMAÑOS, VELOCIDADES)
# COLORES: (NOCHE, LUNA, NARANJA, BLANCO, MORADO, SOMBRA)
# TAMAÑOS: (TAM_CALABAZA, TAM_BRUJA)
# VELOCIDADES: (VEL_JUGADOR, NUM_ENEMIGOS, VEL_MIN, VEL_MAX)
PERFILES = (
    ((480, 640), ((15,15,30),(230,230,200),(255,140,0),(255,255,255),(120,70,200),(60,0,70)), ((40,30),(32,26)), (5, 3, 2, 4)),
    ((480, 640), ((15,15,30),(230,230,200),(255,140,0),(255,255,255),(120,70,200),(60,0,70)), ((40,30),(32,26)), (6, 4, 3, 7)),
    ((480, 640), ((10,10,20),(220,220,180),(255,120,0),(245,245,255),(180,60,220),(80,0,90)), ((36,26),(30,24)), (7, 6, 5, 9)),
)

def get_config(i=1):
    return PERFILES[i]

# Carga inicial (Normal = índice 1)
ANCHO_ALTO, COLORES, TAMAÑOS, VELOCIDADES = get_config(1)
NOCHE, LUNA, NARANJA, BLANCO, MORADO, SOMBRA = COLORES
TAM_CALABAZA, TAM_BRUJA = TAMAÑOS
VEL_JUGADOR, NUM_ENEMIGOS, VEL_MIN, VEL_MAX = VELOCIDADES
NEGRO = (0, 0, 0)
MARRON = (120, 80, 40)

pantalla = pygame.display.set_mode(ANCHO_ALTO)
reloj = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

def rect_tupla(pos, tam):
    # Devuelve (x, y, w, h) a partir de dos tuplas
    return (*pos, *tam)

# Estado
jugador_pos = [ANCHO_ALTO[0]//2 - TAM_CALABAZA[0]//2, ANCHO_ALTO[1] - 80]
brujas = [[random.randint(0, ANCHO_ALTO[0]-TAM_BRUJA[0]), -TAM_BRUJA[1], random.randint(VEL_MIN, VEL_MAX)] for _ in range(NUM_ENEMIGOS)]
puntaje = 0
game_over = False

def dibujar_calabaza(pos):
    # Cuerpo
    pygame.draw.ellipse(pantalla, NARANJA, rect_tupla(pos, TAM_CALABAZA))
    # Rabito (tallo)
    x, y = pos; w, h = TAM_CALABAZA
    pygame.draw.rect(pantalla, (20, 120, 20), (x + w//2 - 4, y - 6, 8, 8))

def dibujar_bruja(pos):
    x, y = pos; w, h = TAM_BRUJA
    # cuerpo y gorro
    pygame.draw.ellipse(pantalla, SOMBRA, (x, y+6, w, h-6))
    pygame.draw.polygon(pantalla, SOMBRA, [(x+w//2, y-6), (x+w//2-10, y+8), (x+w//2+10, y+8)])
    pygame.draw.rect(pantalla, SOMBRA, (x+w//2-12, y+8, 24, 4))
    # escoba
    pygame.draw.line(pantalla, MARRON, (x-6, y+h-6), (x+w+10, y+h-3), 3)
    pygame.draw.polygon(pantalla, MARRON, [(x+w+10, y+h-3), (x+w+18, y+h-9), (x+w+18, y+h+3)])
    # ojos
    pygame.draw.circle(pantalla, MORADO, (x+w//2-4, y+12), 2)
    pygame.draw.circle(pantalla, MORADO, (x+w//2+4, y+12), 2)

def reiniciar():
    global brujas, puntaje, game_over, jugador_pos
    jugador_pos = [ANCHO_ALTO[0]//2 - TAM_CALABAZA[0]//2, ANCHO_ALTO[1] - 80]
    brujas = [[random.randint(0, ANCHO_ALTO[0]-TAM_BRUJA[0]), -TAM_BRUJA[1], random.randint(VEL_MIN, VEL_MAX)] for _ in range(NUM_ENEMIGOS)]
    puntaje = 0
    game_over = False
    return puntaje, game_over

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            # Cambiar perfil 1/2/3
            if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                idx = 0 if e.key == pygame.K_1 else 1 if e.key == pygame.K_2 else 2
                # Re-desempaquetar tuplas de configuración
                ANCHO_ALTO, COLORES, TAMAÑOS, VELOCIDADES = get_config(idx)
                NOCHE, LUNA, NARANJA, BLANCO, MORADO, SOMBRA = COLORES
                TAM_CALABAZA, TAM_BRUJA = TAMAÑOS
                VEL_JUGADOR, NUM_ENEMIGOS, VEL_MIN, VEL_MAX = VELOCIDADES
                pantalla = pygame.display.set_mode(ANCHO_ALTO)
                puntaje, game_over = reiniciar()
            # Reinicio cuando hay game over
            if game_over and e.key == pygame.K_r:
                puntaje, game_over = reiniciar()

    keys = pygame.key.get_pressed()
    if not game_over:
        # Movimiento jugador
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * VEL_JUGADOR
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * VEL_JUGADOR
        jugador_pos[0] += dx
        jugador_pos[1] += dy
        jugador_pos[0] = max(0, min(ANCHO_ALTO[0]-TAM_CALABAZA[0], jugador_pos[0]))
        jugador_pos[1] = max(0, min(ANCHO_ALTO[1]-TAM_CALABAZA[1], jugador_pos[1]))

        # Movimiento brujas
        for b in brujas:
            b[1] += b[2]
            if b[1] > ANCHO_ALTO[1]:
                b[0] = random.randint(0, ANCHO_ALTO[0]-TAM_BRUJA[0])
                b[1] = -TAM_BRUJA[1]
                b[2] = random.randint(VEL_MIN, VEL_MAX)
                puntaje += 1

            # Colisión
            if pygame.Rect(rect_tupla(jugador_pos, TAM_CALABAZA)).colliderect(pygame.Rect(b[0], b[1], *TAM_BRUJA)):
                game_over = True

    # Dibujo
    pantalla.fill(NOCHE)
    pygame.draw.circle(pantalla, LUNA, (ANCHO_ALTO[0]-70, 70), 40)
    dibujar_calabaza(jugador_pos)
    for b in brujas:
        dibujar_bruja((b[0], b[1]))

    # UI
    ayuda = "1=Fácil  2=Normal  3=Difícil"
    texto_top = f"{ayuda}    Puntos: {puntaje}" if not game_over else "¡Te atraparon! R = reiniciar"
    color_top = BLANCO if not game_over else (255, 120, 120)
    pantalla.blit(font.render(texto_top, True, color_top), (10, 10))

    pygame.display.flip()
    reloj.tick(60)