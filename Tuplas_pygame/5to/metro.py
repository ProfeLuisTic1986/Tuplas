import pygame, sys, math

# ----------------- Config -----------------
WIDTH, HEIGHT = 960, 540
SCALE = 3
FPS = 60

TILE = 32
GRAV = 0.45
MAX_FALL = 12
RUN_ACC = 0.6
RUN_DEC = 0.7
RUN_MAX = 4.0

JUMP_VEL = -9.5
COYOTE_FRAMES = 8          # frames para saltar tras dejar suelo
JUMP_BUFFER_FRAMES = 8     # frames para aceptar salto antes de tocar suelo
WALL_SLIDE_SPEED = 1.8
WALL_JUMP_VX = 6.0
WALL_JUMP_VY = -9.0
DASH_SPEED = 10.0
DASH_TIME = 10
DASH_COOLDOWN = 30
IFRAMES_HIT = 45

DEADZONE = pygame.Rect(WIDTH//2-80, HEIGHT//2-60, 160, 120)

# ----------------- Mapa (texto) -----------------
# X = bloque solido, E = enemigo, C = checkpoint, D = puerta/salida
LEVEL = [
"................................................",
"................................................",
".....................XXXX.......................",
".........................X......................",
"..............XXXX........X...............E.....",
"................................................",
".......XXXX.....................XXXX............",
"................................................",
"....C.................XXX..................D....",
"XXXXXXXXXXXXXXXXXXXXXX...XXXXXXXXXXXXXXXXXXXXXXXX",
]

def parse_level(lines):
    solids, enemies, checkpoints, doors = [], [], [], []
    for j, row in enumerate(lines):
        for i, ch in enumerate(row):
            x, y = i*TILE, j*TILE
            if ch == "X":
                solids.append(pygame.Rect(x,y,TILE,TILE))
            elif ch == "E":
                enemies.append(pygame.Rect(x,y,TILE,TILE))
            elif ch == "C":
                checkpoints.append(pygame.Rect(x,y,TILE,TILE))
            elif ch == "D":
                doors.append(pygame.Rect(x,y,TILE,TILE))
    return solids, enemies, checkpoints, doors

# ----------------- Util -----------------
def rect_collide_list(r, rects):
    hits = []
    for t in rects:
        if r.colliderect(t):
            hits.append(t)
    return hits

# ----------------- Entidades -----------------
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 28)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.coyote = 0
        self.jump_buffer = 0
        self.facing = 1
        self.can_double = True
        self.dashing = 0
        self.dash_cd = 0
        self.iframes = 0
        self.spawn = (x,y)

    def input(self, keys):
        ax = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ax -= RUN_ACC
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ax += RUN_ACC
            self.facing = 1

        # Aceleración / fricción
        self.vx += ax
        if ax == 0:
            # freno
            if abs(self.vx) < RUN_DEC:
                self.vx = 0
            else:
                self.vx -= RUN_DEC * math.copysign(1, self.vx)
        self.vx = max(-RUN_MAX, min(RUN_MAX, self.vx))

        # saltos: buffer
        if (keys[pygame.K_SPACE] or keys[pygame.K_z] or keys[pygame.K_k]):
            self.jump_buffer = JUMP_BUFFER_FRAMES

        # dash
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_j]) and self.dashing == 0 and self.dash_cd == 0:
            self.dashing = DASH_TIME
            self.dash_cd = DASH_COOLDOWN
            # impulso horizontal dominante; si no hay input, usa facing
            dirx = (-1 if (keys[pygame.K_LEFT] or keys[pygame.K_a]) else
                     1 if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) else self.facing)
            self.vx = dirx * DASH_SPEED
            self.vy = 0

    def apply_gravity(self):
        if self.dashing == 0:
            self.vy = min(self.vy + GRAV, MAX_FALL)

    def try_jump(self):
        # prioridad: coyote/ground -> salto normal
        if (self.coyote > 0 or self.on_ground) and self.jump_buffer > 0:
            self.vy = JUMP_VEL
            self.on_ground = False
            self.coyote = 0
            self.jump_buffer = 0
            self.can_double = True
            return True
        # doble salto
        if self.can_double and self.jump_buffer > 0:
            self.vy = JUMP_VEL
            self.can_double = False
            self.jump_buffer = 0
            return True
        return False

    def variable_jump(self, keys):
        # Soltar botón reduce altura (salto variable)
        if not (keys[pygame.K_SPACE] or keys[pygame.K_z] or keys[pygame.K_k]) and self.vy < -3:
            self.vy = -3

    def wall_interact(self, keys, solids):
        # slide en pared si empuja contra pared en aire
        left = self.rect.move(-1,0); right = self.rect.move(1,0)
        touching_left = rect_collide_list(left, solids)
        touching_right = rect_collide_list(right, solids)
        pushing_left = (keys[pygame.K_LEFT] or keys[pygame.K_a])
        pushing_right = (keys[pygame.K_RIGHT] or keys[pygame.K_d])

        if not self.on_ground and (touching_left and pushing_left or touching_right and pushing_right):
            if self.vy > WALL_SLIDE_SPEED:
                self.vy = WALL_SLIDE_SPEED

            # wall jump
            if self.jump_buffer > 0:
                dirx = 1 if touching_left else -1
                self.vx = dirx * WALL_JUMP_VX
                self.vy = WALL_JUMP_VY
                self.jump_buffer = 0
                self.can_double = True

    def move_and_collide(self, solids, keys):
        # Horizontal
        self.rect.x += int(round(self.vx))
        hits = rect_collide_list(self.rect, solids)
        for t in hits:
            if self.vx > 0:
                self.rect.right = t.left
            elif self.vx < 0:
                self.rect.left = t.right
            self.vx = 0

        # Vertical
        self.rect.y += int(round(self.vy))
        hits = rect_collide_list(self.rect, solids)
        self.on_ground = False
        for t in hits:
            if self.vy > 0:
                self.rect.bottom = t.top
                self.vy = 0
                self.on_ground = True
            elif self.vy < 0:
                self.rect.top = t.bottom
                self.vy = 0

        # timers
        self.coyote = COYOTE_FRAMES if self.on_ground else max(0, self.coyote-1)
        if self.jump_buffer > 0: self.jump_buffer -= 1
        if self.dashing > 0: self.dashing -= 1
        if self.dash_cd > 0: self.dash_cd -= 1
        if self.iframes > 0: self.iframes -= 1

        # pared
        self.wall_interact(keys, solids)

    def hurt(self, knock_dir):
        if self.iframes == 0:
            self.iframes = IFRAMES_HIT
            self.vx = 6*knock_dir
            self.vy = -6

    def update(self, keys, solids):
        self.input(keys)
        self.apply_gravity()
        self.try_jump()
        self.variable_jump(keys)
        self.move_and_collide(solids, keys)

    def draw(self, surf, camera):
        color = (255, 230, 80) if self.iframes % 6 < 3 else (255, 200, 40)
        pygame.draw.rect(surf, color, camera.to_screen(self.rect))

class EnemyPatrol:
    def __init__(self, rect, left= -48, right= 48, speed=1.2):
        self.origin = pygame.Vector2(rect.x, rect.y)
        self.rect = pygame.Rect(rect.x, rect.y, 20, 20)
        self.left = left; self.right = right
        self.speed = speed
        self.dir = 1

    def update(self, solids):
        self.rect.x += int(self.dir*self.speed)
        if self.rect.x > self.origin.x + self.right: self.dir = -1
        if self.rect.x < self.origin.x + self.left: self.dir = 1
        # simple colisión con sólidos: rebote
        for t in rect_collide_list(self.rect, solids):
            if self.dir > 0: self.rect.right = t.left; self.dir = -1
            else: self.rect.left = t.right; self.dir = 1

    def draw(self, surf, camera):
        pygame.draw.rect(surf, (200,60,60), camera.to_screen(self.rect))

# ----------------- Cámara -----------------
class Camera:
    def __init__(self, w, h):
        self.offset = pygame.Vector2(0,0)
        self.world_w = w; self.world_h = h

    def update(self, target_rect):
        # dead zone centrada
        screen_target = pygame.Rect(
            target_rect.x - self.offset.x,
            target_rect.y - self.offset.y,
            target_rect.width, target_rect.height
        )
        if screen_target.left < DEADZONE.left:
            self.offset.x -= DEADZONE.left - screen_target.left
        elif screen_target.right > DEADZONE.right:
            self.offset.x += screen_target.right - DEADZONE.right
        if screen_target.top < DEADZONE.top:
            self.offset.y -= DEADZONE.top - screen_target.top
        elif screen_target.bottom > DEADZONE.bottom:
            self.offset.y += screen_target.bottom - DEADZONE.bottom

        # límites mundo
        self.offset.x = max(0, min(self.offset.x, self.world_w - WIDTH))
        self.offset.y = max(0, min(self.offset.y, self.world_h - HEIGHT))

    def to_screen(self, rect):
        return pygame.Rect(rect.x - self.offset.x, rect.y - self.offset.y, rect.w, rect.h)

# ----------------- Juego -----------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Metroidvania Base - Pygame")
        self.clock = pygame.time.Clock()

        self.solids, enemy_rects, self.checkpoints, self.doors = parse_level(LEVEL)
        # tamaño mundo
        world_w = len(LEVEL[0]) * TILE
        world_h = len(LEVEL) * TILE
        self.camera = Camera(world_w, world_h)

        # jugador
        spawn = self.checkpoints[0] if self.checkpoints else pygame.Rect(64,64,32,32)
        self.player = Player(spawn.x, spawn.y - 8)
        self.respawn = (self.player.rect.x, self.player.rect.y)

        # enemigos
        self.enemies = [EnemyPatrol(r) for r in enemy_rects]

        # parallax (dos capas sencillas)
        self.bg1 = pygame.Surface((world_w, world_h)); self.bg1.fill((30,30,45))
        self.bg2 = pygame.Surface((world_w, world_h), pygame.SRCALPHA)
        for i in range(0, world_w, 160):
            pygame.draw.circle(self.bg2, (255,255,255,70), (i, 80), 2)

        self.font = pygame.font.SysFont("consolas", 16)

    def draw_tiles(self):
        for t in self.solids:
            pygame.draw.rect(self.screen, (90,110,140), self.camera.to_screen(t))
        for c in self.checkpoints:
            pygame.draw.rect(self.screen, (80,200,120), self.camera.to_screen(c))
        for d in self.doors:
            pygame.draw.rect(self.screen, (120,80,200), self.camera.to_screen(d))

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.solids)
        for e in self.enemies:
            e.update(self.solids)

        # daño por contacto
        for e in self.enemies:
            if self.player.rect.colliderect(e.rect):
                self.player.hurt(knock_dir=1 if self.player.rect.centerx < e.rect.centerx else -1)

        # checkpoints
        for c in self.checkpoints:
            if self.player.rect.colliderect(c):
                self.respawn = (c.x, c.y - 8)

        # puerta (reinicia nivel por ahora)
        for d in self.doors:
            if self.player.rect.colliderect(d):
                self.player.rect.topleft = self.respawn

        # caída al vacío
        if self.player.rect.top > len(LEVEL)*TILE + 200:
            self.player.rect.topleft = self.respawn
            self.player.vx = self.player.vy = 0
            self.player.iframes = 30

        self.camera.update(self.player.rect)

    def render(self):
        # parallax
        par1 = self.camera.offset * 0.3
        par2 = self.camera.offset * 0.6
        self.screen.blit(self.bg1, (-par1.x, -par1.y))
        self.screen.blit(self.bg2, (-par2.x, -par2.y))

        self.draw_tiles()
        for e in self.enemies: e.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        # UI
        txt = f"vx:{self.player.vx:.2f} vy:{self.player.vy:.2f} dash:{self.player.dash_cd} if:{self.player.iframes}"
        self.screen.blit(self.font.render(txt, True, (230,230,230)), (8,8))
        pygame.draw.rect(self.screen, (70,200,120), DEADZONE, 1)

    def run(self):
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()

            self.update()
            self.screen.fill((10,10,15))
            self.render()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()
