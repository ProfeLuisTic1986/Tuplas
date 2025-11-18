import pygame, random, sys
pygame.init()

ANCHO_ALTO = (480, 640)
NOCHE = (20, 20, 35)
LUNA = (230, 230, 200)
NARANJA = (255, 140, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
MORADO = (120, 70, 200)
TAM_CALABAZA = (40, 30)
TAM_MURCIELAGO = (30, 20)

pantalla = pygame.display.set_mode(ANCHO_ALTO)
reloj = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

jugador_pos = [ANCHO_ALTO[0]//2 - TAM_CALABAZA[0]//2, ANCHO_ALTO[1] - 80]
murcielagos = [[random.randint(0, ANCHO_ALTO[0]-TAM_MURCIELAGO[0]), -TAM_MURCIELAGO[1], 4] for _ in range(3)]
puntaje, game_over = 0, False

def dibujar_calabaza(pos):
    pygame.draw.ellipse(pantalla, NARANJA, (pos[0], pos[1], TAM_CALABAZA[0], TAM_CALABAZA[1]))
    pygame.draw.rect(pantalla, (20,120,20), (pos[0]+TAM_CALABAZA[0]//2-4, pos[1]-6, 8, 8))

def dibujar_murcielago(pos):
    x, y = pos; w, h = TAM_MURCIELAGO
    pygame.draw.ellipse(pantalla, NEGRO, (x, y, w, h))
    pygame.draw.polygon(pantalla, NEGRO, [(x, y+h//2),(x-10, y-5),(x-5, y+h)])
    pygame.draw.polygon(pantalla, NEGRO, [(x+w, y+h//2),(x+w+10, y-5),(x+w+5, y+h)])
    pygame.draw.circle(pantalla, MORADO, (x+w//2-4, y+h//2-4), 2)
    pygame.draw.circle(pantalla, MORADO, (x+w//2+4, y+h//2-4), 2)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN and game_over and e.key == pygame.K_r:
            jugador_pos[:] = [ANCHO_ALTO[0]//2 - TAM_CALABAZA[0]//2, ANCHO_ALTO[1] - 80]
            murcielagos[:] = [[random.randint(0, ANCHO_ALTO[0]-TAM_MURCIELAGO[0]), -TAM_MURCIELAGO[1], 4] for _ in range(3)]
            puntaje, game_over = 0, False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  jugador_pos[0] -= 5
        if keys[pygame.K_RIGHT]: jugador_pos[0] += 5
        jugador_pos[0] = max(0, min(ANCHO_ALTO[0]-TAM_CALABAZA[0], jugador_pos[0]))
        for m in murcielagos:
            m[1] += m[2]
            if m[1] > ANCHO_ALTO[1]:
                m[0] = random.randint(0, ANCHO_ALTO[0]-TAM_MURCIELAGO[0]); m[1] = -TAM_MURCIELAGO[1]; puntaje += 1
            if pygame.Rect(jugador_pos[0], jugador_pos[1], *TAM_CALABAZA).colliderect(pygame.Rect(m[0], m[1], *TAM_MURCIELAGO)):
                game_over = True

    pantalla.fill(NOCHE)
    pygame.draw.circle(pantalla, LUNA, (60, 60), 35)
    dibujar_calabaza(jugador_pos)
    for m in murcielagos: dibujar_murcielago((m[0], m[1]))
    txt = "¡Te atraparon! R=reintentar" if game_over else f"Puntos: {puntaje}"
    pantalla.blit(font.render(txt, True, BLANCO), (10, 10))
    pygame.display.flip(); reloj.tick(60)