import pygame, random, sys
pygame.init()

ANCHO_ALTO = (480, 640)
CENTRO = (ANCHO_ALTO[0]//2, ANCHO_ALTO[1]//2)
NOCHE = (18, 18, 32)
LUNA = (230, 230, 200)
NARANJA = (255, 140, 0)
HUESO = (235, 235, 235)
BLANCO = (255, 255, 255)
TAM_CALABAZA = (35, 25)
TAM_ESQUELETO = (26, 34)

pantalla = pygame.display.set_mode(ANCHO_ALTO)
reloj = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

jugador_pos = [CENTRO[0] - TAM_CALABAZA[0]//2, ANCHO_ALTO[1] - 100]
esqueletos = [[random.randint(0, ANCHO_ALTO[0]-TAM_ESQUELETO[0]), -TAM_ESQUELETO[1], random.randint(3, 6)] for _ in range(4)]
puntaje, game_over = 0, False

def dibujar_calabaza(pos):
    x, y = pos
    w, h = TAM_CALABAZA
    # cuerpo
    pygame.draw.ellipse(pantalla, NARANJA, (x, y, w, h))
    # rabito (tallo)
    pygame.draw.rect(pantalla, (20, 120, 20), (x + w//2 - 3, y - 5, 6, 6))

def dibujar_esqueleto(pos):
    x, y = pos; w, h = TAM_ESQUELETO
    pygame.draw.circle(pantalla, HUESO, (x+w//2, y+8), 8)
    pygame.draw.rect(pantalla, HUESO, (x+w//2-2, y+16, 4, h-16))
    for rib in (20, 24, 28): pygame.draw.line(pantalla, HUESO, (x+6, y+rib), (x+w-6, y+rib), 2)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN and game_over and e.key == pygame.K_r:
            jugador_pos[:] = [CENTRO[0] - TAM_CALABAZA[0]//2, ANCHO_ALTO[1] - 100]
            esqueletos[:] = [[random.randint(0, ANCHO_ALTO[0]-TAM_ESQUELETO[0]), -TAM_ESQUELETO[1], random.randint(3,6)] for _ in range(4)]
            puntaje, game_over = 0, False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  jugador_pos[0] -= 6
        if keys[pygame.K_RIGHT]: jugador_pos[0] += 6
        if keys[pygame.K_UP]:    jugador_pos[1] -= 6
        if keys[pygame.K_DOWN]:  jugador_pos[1] += 6
        jugador_pos[0] = max(0, min(ANCHO_ALTO[0]-TAM_CALABAZA[0], jugador_pos[0]))
        jugador_pos[1] = max(0, min(ANCHO_ALTO[1]-TAM_CALABAZA[1], jugador_pos[1]))
        for s in esqueletos:
            s[1] += s[2]
            if s[1] > ANCHO_ALTO[1]:
                s[0] = random.randint(0, ANCHO_ALTO[0]-TAM_ESQUELETO[0]); s[1] = -TAM_ESQUELETO[1]; puntaje += 1
            if pygame.Rect(jugador_pos[0], jugador_pos[1], *TAM_CALABAZA).colliderect(pygame.Rect(s[0], s[1], *TAM_ESQUELETO)):
                game_over = True

    pantalla.fill(NOCHE)
    pygame.draw.circle(pantalla, LUNA, (ANCHO_ALTO[0]-70, 70), 40)
    for s in esqueletos: dibujar_esqueleto((s[0], s[1]))
    dibujar_calabaza(jugador_pos)
    txt = "¡Te atraparon! R=reintentar" if game_over else f"Puntos: {puntaje}"
    pantalla.blit(font.render(txt, True, BLANCO), (10, 10))
    pygame.display.flip(); reloj.tick(60)