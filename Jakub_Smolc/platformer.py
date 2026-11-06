"""
Plošinovka v Pygame – kostra pro maturitní projekt.

Spuštění:   pip install pygame   a pak   python platformer.py

Ovládání:   ← → nebo A D  = pohyb
            mezerník / ↑ / W = skok (čím déle držíš, tím výš skočíš)
            P = pauza,  ESC = zpět do menu
"""
import json
import math
import os
import sys

import pygame

# ---------------------------------------------------------------- NASTAVENÍ
TILE = 40                      # velikost jednoho políčka v pixelech
ROWS = 15                      # výška levelu v políčkách
WIDTH, HEIGHT = 960, ROWS * TILE
FPS = 60

GRAVITY = 2200                 # px/s^2
MOVE_SPEED = 300               # px/s
JUMP_SPEED = 780               # px/s
MAX_FALL = 1000                # maximální rychlost pádu
START_LIVES = 3

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")

SKY = (135, 206, 235)
DIRT = (121, 85, 58)
GRASS = (76, 175, 80)
PLAYER_COLOR = (52, 101, 214)
ENEMY_COLOR = (200, 50, 50)
COIN_COLOR = (255, 205, 40)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

# ------------------------------------------------------------------- LEVELY
# Legenda:  #  zem / platforma     P  start hráče     C  mince
#           E  nepřítel            ^  ostny           X  cíl (vlajka)
#           .  prázdno
# Stačí zapsat spodní řádky levelu, horní se doplní prázdnem.
# Nový level = přidej další seznam řetězců a zapiš ho do LEVELS.
LEVEL_1 = [
    "..............CC......CCC..........CC.......CCC.....",
    ".............####.................####..............",
    "..P.............E............E..........^........X..",
    "#########...##########...#########...#######...#####",
    "#########...##########...#########...#######...#####",
]

LEVEL_2 = [
    "...............CC.........CC.E..............CCC.............",
    "...............##.........#####..........#####..............",
    "...........##.......##......................................",
    "..P.............................E...........^..E..^....X....",
    "##########............###############...####################",
    "##########............###############...####################",
]
LEVELS = [LEVEL_1, LEVEL_2]


# ----------------------------------------------------------------- ULOŽENÍ
def load_highscore():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return int(json.load(f).get("highscore", 0))
    except (OSError, ValueError, AttributeError):
        return 0


def save_highscore(score):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"highscore": score}, f)
    except OSError:
        pass


# ------------------------------------------------------------------ HRÁČ
class Player:
    W, H = 28, 36

    def __init__(self, x, y):
        self.rect = pygame.Rect(x + (TILE - self.W) // 2, y + TILE - self.H, self.W, self.H)
        self.pos = pygame.Vector2(self.rect.topleft)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.coyote = 0.0          # krátce po odchodu z hrany jde ještě skočit
        self.jump_buffer = 0.0     # skok stisknutý těsně před dopadem se nezahodí
        self.facing = 1

    def update(self, dt, solids, level_width):
        keys = pygame.key.get_pressed()
        direction = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        jump_held = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]

        self.vel.x = direction * MOVE_SPEED
        if direction:
            self.facing = direction

        self.coyote = max(0.0, self.coyote - dt)
        self.jump_buffer = max(0.0, self.jump_buffer - dt)

        if self.jump_buffer > 0 and self.coyote > 0:
            self.vel.y = -JUMP_SPEED
            self.coyote = 0.0
            self.jump_buffer = 0.0

        # po puštění skoku padá hráč rychleji -> kratší skok
        gravity = GRAVITY * (2.5 if self.vel.y < 0 and not jump_held else 1)
        self.vel.y = min(self.vel.y + gravity * dt, MAX_FALL)

        nearby = [s for s in solids if self.rect.inflate(4 * TILE, 4 * TILE).colliderect(s)]

        # --- pohyb po ose X + kolize
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)
        for s in nearby:
            if self.rect.colliderect(s):
                if self.vel.x > 0:
                    self.rect.right = s.left
                elif self.vel.x < 0:
                    self.rect.left = s.right
                self.pos.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = 0
        if self.rect.right > level_width:
            self.rect.right = level_width
            self.pos.x = self.rect.x

        # --- pohyb po ose Y + kolize
        vy = self.vel.y
        self.pos.y += vy * dt
        self.rect.y = round(self.pos.y)
        self.on_ground = False
        for s in nearby:
            if self.rect.colliderect(s):
                if vy > 0:
                    self.rect.bottom = s.top
                    self.on_ground = True
                elif vy < 0:
                    self.rect.top = s.bottom
                self.vel.y = 0
                self.pos.y = self.rect.y
        if self.on_ground:
            self.coyote = 0.1

    def draw(self, surface, camera_x):
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, PLAYER_COLOR, r, border_radius=6)
        eye_x = r.centerx + 5 * self.facing
        pygame.draw.circle(surface, WHITE, (eye_x, r.y + 12), 5)
        pygame.draw.circle(surface, BLACK, (eye_x + self.facing, r.y + 12), 2)


# --------------------------------------------------------------- NEPŘÍTEL
class Enemy:
    SIZE = 32

    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 4, y + TILE - self.SIZE, self.SIZE, self.SIZE)
        self.x = float(self.rect.x)
        self.dir = -1
        self.speed = 80

    def update(self, dt, solids):
        self.x += self.dir * self.speed * dt
        self.rect.x = round(self.x)
        nearby = [s for s in solids if self.rect.inflate(2 * TILE, 2 * TILE).colliderect(s)]

        # narazil do zdi -> otoč se
        for s in nearby:
            if self.rect.colliderect(s):
                if self.dir > 0:
                    self.rect.right = s.left
                else:
                    self.rect.left = s.right
                self.x = self.rect.x
                self.dir *= -1
                break

        # došel na kraj platformy -> otoč se
        foot = (self.rect.right + 2 if self.dir > 0 else self.rect.left - 2, self.rect.bottom + 2)
        if not any(s.collidepoint(foot) for s in nearby):
            self.dir *= -1

    def draw(self, surface, camera_x):
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, ENEMY_COLOR, r, border_radius=8)
        for dx in (-7, 7):
            pygame.draw.circle(surface, WHITE, (r.centerx + dx, r.y + 11), 5)
            pygame.draw.circle(surface, BLACK, (r.centerx + dx + self.dir * 2, r.y + 11), 2)


# -------------------------------------------------------------------- HRA
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Plošinovka")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.big_font = pygame.font.Font(None, 96)
        self.state = "menu"            # menu / playing / paused / gameover / win
        self.highscore = load_highscore()
        self.time = 0.0
        self.score = 0
        self.lives = START_LIVES
        self.level_index = 0
        self.level_start_score = 0
        self.load_level(0)

    # ---------- načtení levelu z textu
    def load_level(self, index):
        rows = LEVELS[index]
        width = max(len(r) for r in rows)
        rows = [r.ljust(width, ".") for r in rows]
        rows = ["." * width] * (ROWS - len(rows)) + rows

        self.solids, self.coins, self.enemies, self.spikes = [], [], [], []
        self.tiles = set()
        self.exit_rect = None
        spawn = (TILE, TILE * (ROWS - 3))

        for ty, row in enumerate(rows):
            for tx, ch in enumerate(row):
                x, y = tx * TILE, ty * TILE
                if ch == "#":
                    self.solids.append(pygame.Rect(x, y, TILE, TILE))
                    self.tiles.add((tx, ty))
                elif ch == "C":
                    self.coins.append(pygame.Rect(x + 10, y + 10, 20, 20))
                elif ch == "E":
                    self.enemies.append(Enemy(x, y))
                elif ch == "^":
                    self.spikes.append(pygame.Rect(x + 6, y + TILE // 2, TILE - 12, TILE // 2))
                elif ch == "X":
                    self.exit_rect = pygame.Rect(x, y - TILE, TILE, 2 * TILE)
                elif ch == "P":
                    spawn = (x, y)

        self.level_width = width * TILE
        self.player = Player(*spawn)
        self.camera_x = 0

    def start_game(self):
        self.level_index = 0
        self.score = 0
        self.lives = START_LIVES
        self.level_start_score = 0
        self.load_level(0)
        self.state = "playing"

    def finish(self, state):
        if self.score > self.highscore:
            self.highscore = self.score
            save_highscore(self.highscore)
        self.state = state

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.finish("gameover")
        else:
            self.score = self.level_start_score
            self.load_level(self.level_index)

    def next_level(self):
        self.score += 100
        if self.level_index + 1 >= len(LEVELS):
            self.finish("win")
        else:
            self.level_index += 1
            self.level_start_score = self.score
            self.load_level(self.level_index)

    # ---------- logika
    def update_playing(self, dt):
        p = self.player
        p.update(dt, self.solids, self.level_width)

        for coin in self.coins[:]:
            if p.rect.colliderect(coin):
                self.coins.remove(coin)
                self.score += 10

        for enemy in self.enemies[:]:
            enemy.update(dt, self.solids)
            if p.rect.colliderect(enemy.rect):
                if p.vel.y > 0 and p.rect.bottom - enemy.rect.top < 20:
                    self.enemies.remove(enemy)       # skok na hlavu
                    self.score += 50
                    p.vel.y = -450
                else:
                    self.lose_life()
                    return

        if any(p.rect.colliderect(s) for s in self.spikes) or p.rect.top > HEIGHT + 50:
            self.lose_life()
            return

        if self.exit_rect and p.rect.colliderect(self.exit_rect):
            self.next_level()
            return

        target = p.rect.centerx - WIDTH // 2
        self.camera_x = max(0, min(target, self.level_width - WIDTH))

    # ---------- vykreslování
    def draw_text(self, text, font, color, center=None, topleft=None, shadow=True):
        img = font.render(text, True, color)
        rect = img.get_rect(center=center) if center else img.get_rect(topleft=topleft)
        if shadow:   # tmavý stín pod textem pro lepší čitelnost
            self.screen.blit(font.render(text, True, BLACK), rect.move(2, 2))
        self.screen.blit(img, rect)

    def draw_world(self):
        cam = self.camera_x
        self.screen.fill(SKY)

        # mraky (pomalejší pohyb = iluze hloubky)
        for i in range(8):
            cx = (i * 330 - cam * 0.3) % (WIDTH + 300) - 150
            cy = 70 + (i * 53) % 120
            for dx, dy, rad in ((0, 0, 28), (30, 8, 22), (-30, 8, 22)):
                pygame.draw.circle(self.screen, (245, 250, 255), (int(cx + dx), cy + dy), rad)

        for s in self.solids:
            if s.right < cam or s.left > cam + WIDTH:
                continue
            r = s.move(-cam, 0)
            pygame.draw.rect(self.screen, DIRT, r)
            if (s.x // TILE, s.y // TILE - 1) not in self.tiles:
                pygame.draw.rect(self.screen, GRASS, (r.x, r.y, TILE, 10))

        for sp in self.spikes:
            r = sp.move(-cam, 0)
            pygame.draw.polygon(self.screen, (170, 170, 180),
                                [(r.left - 6, r.bottom), (r.centerx, r.top), (r.right + 6, r.bottom)])

        for i, c in enumerate(self.coins):
            bob = math.sin(self.time * 4 + i) * 3
            pygame.draw.circle(self.screen, COIN_COLOR, (c.centerx - cam, int(c.centery + bob)), 10)
            pygame.draw.circle(self.screen, (200, 150, 0), (c.centerx - cam, int(c.centery + bob)), 10, 2)

        if self.exit_rect:
            r = self.exit_rect.move(-cam, 0)
            pygame.draw.line(self.screen, (90, 90, 90), (r.x + 10, r.y), (r.x + 10, r.bottom), 4)
            pygame.draw.polygon(self.screen, (230, 60, 60),
                                [(r.x + 12, r.y + 2), (r.x + 38, r.y + 14), (r.x + 12, r.y + 26)])

        for e in self.enemies:
            e.draw(self.screen, cam)
        self.player.draw(self.screen, cam)

        hud = (f"Skóre: {self.score}    Životy: {self.lives}    "
               f"Level: {self.level_index + 1}/{len(LEVELS)}    Rekord: {self.highscore}")
        self.draw_text(hud, self.font, WHITE, topleft=(15, 12))

    def draw_overlay(self, title, lines):
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 150))
        self.screen.blit(dim, (0, 0))
        self.draw_text(title, self.big_font, WHITE, center=(WIDTH // 2, HEIGHT // 2 - 90))
        for i, line in enumerate(lines):
            self.draw_text(line, self.font, WHITE, center=(WIDTH // 2, HEIGHT // 2 + i * 38))

    # ---------- hlavní smyčka
    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000, 1 / 30)   # omezení, aby hráč neprošel zdí při lagu
            self.time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type != pygame.KEYDOWN:
                    continue

                if self.state == "menu":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.quit()
                elif self.state == "playing":
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        self.player.jump_buffer = 0.12
                    elif event.key == pygame.K_p:
                        self.state = "paused"
                    elif event.key == pygame.K_ESCAPE:
                        self.finish("menu")
                elif self.state == "paused":
                    if event.key == pygame.K_p:
                        self.state = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        self.finish("menu")
                else:  # gameover / win
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        self.state = "menu"

            if self.state == "playing":
                self.update_playing(dt)

            if self.state == "menu":
                self.screen.fill(SKY)
                self.draw_text("PLOŠINOVKA", self.big_font, WHITE, center=(WIDTH // 2, 190))
                self.draw_text("ENTER – hrát", self.font, WHITE, center=(WIDTH // 2, 320))
                self.draw_text("ESC – konec", self.font, WHITE, center=(WIDTH // 2, 360))
                self.draw_text(f"Rekord: {self.highscore}", self.font, COIN_COLOR, center=(WIDTH // 2, 430))
            else:
                self.draw_world()
                if self.state == "paused":
                    self.draw_overlay("PAUZA", ["P – pokračovat", "ESC – menu"])
                elif self.state == "gameover":
                    self.draw_overlay("KONEC HRY", [f"Skóre: {self.score}", "ENTER – menu"])
                elif self.state == "win":
                    self.draw_overlay("VYHRÁL JSI!", [f"Skóre: {self.score}", "ENTER – menu"])

            pygame.display.flip()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
