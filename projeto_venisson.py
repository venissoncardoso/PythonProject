import pgzrun
import random
from pygame import Rect
#teste
WIDTH = 1024
HEIGHT = 768
TILE_SIZE = 48

game_state = "menu"
sound_on = True
coins_collected = 0
total_coins = 3

click_sound = sounds.click
toggle_sound = sounds.toggle
step_sound = sounds.step
game_over_sound = sounds.game_over
coin_sound = sounds.coin

music.set_volume(0.3)
music.play("music")

game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

button_width = 250
button_height = 60
button_x = WIDTH // 2 - button_width // 2
first_button_y = int(HEIGHT * 0.4)
button_spacing = 30

start_button = Rect((button_x, first_button_y), (button_width, button_height))
sound_button = Rect((button_x, first_button_y + button_height + button_spacing), (button_width, button_height))
quit_button = Rect((button_x, first_button_y + 2 * (button_height + button_spacing)), (button_width, button_height))
hovered_button = None

class Hero:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 4
        self.state = "idle"
        self.frame = 0
        self.frame_timer = 0
        self.idle_frames = ["hero_idle_0", "hero_idle_1", "hero_idle_2", "hero_idle_3"]
        self.walk_frames = ["hero_walk_0", "hero_walk_1", "hero_walk_2", "hero_walk_3"]
        self.actor = Actor(self.idle_frames[0], (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2))

    def draw(self):
        self.actor.draw()

    def update(self):
        moving = False
        if self.x < self.target_x:
            self.x += self.speed
            moving = True
        elif self.x > self.target_x:
            self.x -= self.speed
            moving = True
        if self.y < self.target_y:
            self.y += self.speed
            moving = True
        elif self.y > self.target_y:
            self.y -= self.speed
            moving = True

        if self.x == self.target_x and self.y == self.target_y:
            self.grid_x = self.target_x // TILE_SIZE
            self.grid_y = self.target_y // TILE_SIZE

        self.state = "walk" if moving else "idle"
        self.actor.pos = (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)

        self.frame_timer += 1
        if self.frame_timer >= 8:
            self.frame_timer = 0
            self.frame = (self.frame + 1) % len(self.get_frames())
            self.actor.image = self.get_frames()[self.frame]

    def get_frames(self):
        return self.walk_frames if self.state == "walk" else self.idle_frames

    def move(self, dx, dy):
        if self.x != self.target_x or self.y != self.target_y:
            return
        new_x, new_y = self.grid_x + dx, self.grid_y + dy
        if (0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map)
                and game_map[new_y][new_x] == 0):
            self.grid_x, self.grid_y = new_x, new_y
            self.target_x = new_x * TILE_SIZE
            self.target_y = new_y * TILE_SIZE
            if sound_on:
                step_sound.play()

class Enemy:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 2
        self.pause_time = random.randint(20, 60)
        self.pause_timer = self.pause_time
        self.idle_frames = ["enemy_idle_0", "enemy_idle_1", "enemy_idle_2", "enemy_idle_3"]
        self.walk_frames = ["enemy_walk_0", "enemy_walk_1", "enemy_walk_2", "enemy_walk_3"]
        self.actor = Actor(self.idle_frames[0], (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2))
        self.frame = 0
        self.frame_timer = 0

    def draw(self):
        self.actor.draw()

    def update(self, hero, reserved_positions):
        if self.x < self.target_x:
            self.x += self.speed
        elif self.x > self.target_x:
            self.x -= self.speed
        if self.y < self.target_y:
            self.y += self.speed
        elif self.y > self.target_y:
            self.y -= self.speed
        if self.x == self.target_x and self.y == self.target_y:
            self.grid_x = self.target_x // TILE_SIZE
            self.grid_y = self.target_y // TILE_SIZE
        self.actor.pos = (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
        if self.pause_timer > 0:
            self.pause_timer -= 1
        elif self.x == self.target_x and self.y == self.target_y:
            if self.grid_x != hero.grid_x or self.grid_y != hero.grid_y:
                dx, dy = hero.grid_x - self.grid_x, hero.grid_y - self.grid_y
                directions = []
                if abs(dx) > 0:
                    directions.append((1 if dx > 0 else -1, 0))
                if abs(dy) > 0:
                    directions.append((0, 1 if dy > 0 else -1))
                random.shuffle(directions)
                for step_x, step_y in directions:
                    new_x, new_y = self.grid_x + step_x, self.grid_y + step_y
                    if (0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map)
                            and game_map[new_y][new_x] == 0
                            and (new_x, new_y) not in reserved_positions
                            and not self.has_enemy_at(new_x, new_y)
                            and not self.has_coin_at(new_x, new_y)):
                        reserved_positions.add((new_x, new_y))
                        self.grid_x, self.grid_y = new_x, new_y
                        self.target_x = new_x * TILE_SIZE
                        self.target_y = new_y * TILE_SIZE
                        break
                self.pause_timer = self.pause_time

        self.frame_timer += 1
        if self.frame_timer >= 8:
            self.frame_timer = 0
            self.frame = (self.frame + 1) % 4
            is_moving = self.x != self.target_x or self.y != self.target_y
            self.actor.image = self.walk_frames[self.frame] if is_moving else self.idle_frames[self.frame]

    def has_enemy_at(self, x, y):
        for enemy in enemies:
            if enemy != self and enemy.grid_x == x and enemy.grid_y == y:
                return True
        return False

    def has_coin_at(self, x, y):
        for coin in coins:
            if coin.grid_x == x and coin.grid_y == y and not coin.collected:
                return True
        return False

class Coin:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.collected = False
        self.frame = 0
        self.frame_timer = 0
        self.frames = ["coin_0", "coin_1", "coin_2", "coin_3"]
        self.actor = Actor(self.frames[0], (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2))
        self.float_offset = 0
        self.float_direction = 1

    def draw(self):
        if not self.collected:
            float_y = self.y + self.float_offset
            self.actor.pos = (self.x + TILE_SIZE // 2, float_y + TILE_SIZE // 2)
            self.actor.draw()

    def update(self):
        if not self.collected:
            self.frame_timer += 1
            if self.frame_timer >= 12:
                self.frame_timer = 0
                self.frame = (self.frame + 1) % len(self.frames)
                self.actor.image = self.frames[self.frame]

            self.float_offset += 0.3 * self.float_direction
            if abs(self.float_offset) > 3:
                self.float_direction *= -1

hero = Hero(1, 1)

def get_valid_enemy_positions():
    positions = []
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            if game_map[y][x] == 0 and (x, y) != (1, 1):
                positions.append((x, y))
    return random.sample(positions, 5)

def get_valid_coin_positions():
    positions = []
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            if game_map[y][x] == 0 and (x, y) != (1, 1):
                positions.append((x, y))
    return random.sample(positions, total_coins)

def spawn_enemies():
    positions = get_valid_enemy_positions()
    return [Enemy(x, y) for (x, y) in positions]

def spawn_coins():
    positions = get_valid_coin_positions()
    return [Coin(x, y) for (x, y) in positions]

enemies = spawn_enemies()
coins = spawn_coins()

def reset_game():
    global hero, enemies, coins, coins_collected
    hero = Hero(1, 1)
    enemies = spawn_enemies()
    coins = spawn_coins()
    coins_collected = 0

def game_over():
    global game_state
    if sound_on:
        game_over_sound.play()
    game_state = "game_over"

def victory():
    global game_state
    game_state = "victory"

collision_detected = False


def check_collision():
    global collision_detected
    if game_state == "game_over" or game_state == "victory":
        return False
    if hero.x != hero.target_x or hero.y != hero.target_y:
        collision_detected = False
        return False
    for enemy in enemies:
        if enemy.x != enemy.target_x or enemy.y != enemy.target_y:
            continue
        if hero.grid_x == enemy.grid_x and hero.grid_y == enemy.grid_y:
            if not collision_detected:
                collision_detected = True
                return True
    collision_detected = False
    return False

def check_coin_collection():
    global coins_collected
    for coin in coins:
        if not coin.collected and hero.grid_x == coin.grid_x and hero.grid_y == coin.grid_y:
            coin.collected = True
            coins_collected += 1
            if sound_on:
                coin_sound.play()
            if coins_collected >= total_coins:
                victory()
            return True
    return False

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu_background()
        draw_menu()
    elif game_state == "game":
        draw_game()
        screen.draw.text(f"Coins: {coins_collected}/{total_coins}", (10, 10), fontsize=36, color="yellow")
    elif game_state == "victory":
        draw_game()
        screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (0, 0, 0, 160))
        screen.draw.text("VICTORY!", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=72, color="gold")
        screen.draw.text(f"Coins Collected: {coins_collected}/{total_coins}", center=(WIDTH // 2, HEIGHT // 2 + 10),
                         fontsize=36, color="yellow")
        screen.draw.text("Press ENTER to continue", center=(WIDTH // 2, HEIGHT // 2 + 70), fontsize=24, color="white")
    elif game_state == "game_over":
        draw_game()
        screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (0, 0, 0, 160))
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=72, color="red")
        screen.draw.text(f"Coins: {coins_collected}/{total_coins}", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=36,
                         color="yellow")
        screen.draw.text("Press ENTER or Click Start", center=(WIDTH // 2, HEIGHT // 2 + 70), fontsize=24,
                         color="white")
def draw_game():
    for row in range(len(game_map)):
        for col in range(len(game_map[0])):
            tile = game_map[row][col]
            color = (60, 60, 60) if tile == 1 else (180, 180, 180)
            screen.draw.filled_rect(Rect((col * TILE_SIZE, row * TILE_SIZE), (TILE_SIZE, TILE_SIZE)), color)
    for coin in coins:
        coin.draw()
    hero.draw()
    for enemy in enemies:
        enemy.draw()


def update():
    global collision_detected
    if game_state == "game":
        hero.update()
        reserved_positions = set()
        for enemy in enemies:
            enemy.update(hero, reserved_positions)
        for coin in coins:
            coin.update()
        if check_collision():
            game_over()
            collision_detected = False
        check_coin_collection()
    if sound_on and not music.is_playing:
        music.play("music")
    elif not sound_on and music.is_playing:
        music.stop()

def draw_menu_background():
    for y in range(0, HEIGHT, 40):
        for x in range(0, WIDTH, 40):
            color = (230, 230, 250) if (x // 40 + y // 40) % 2 == 0 else (210, 210, 240)
            screen.draw.filled_rect(Rect((x, y), (40, 40)), color)
    screen.draw.text("ADVENTURES OF KODLAND", center=(WIDTH // 2, 100), fontsize=60, color=(20, 20, 60), shadow=(1, 1))


def draw_button(rect, text, hovered=False):
    color = (220, 220, 220) if hovered else (180, 180, 180)
    screen.draw.filled_rect(rect, color)
    screen.draw.rect(rect, (0, 0, 0))
    screen.draw.text(text, center=rect.center, fontsize=32, color=(0, 0, 0))

def draw_menu():
    draw_button(start_button, "Start Game", hovered_button == start_button)
    draw_button(sound_button, f"Sound: {'On' if sound_on else 'Off'}", hovered_button == sound_button)
    draw_button(quit_button, "Quit", hovered_button == quit_button)

def on_mouse_move(pos):
    global hovered_button
    hovered_button = None
    if start_button.collidepoint(pos):
        hovered_button = start_button
    elif sound_button.collidepoint(pos):
        hovered_button = sound_button
    elif quit_button.collidepoint(pos):
        hovered_button = quit_button

def on_mouse_down(pos):
    global game_state, sound_on, collision_detected
    if game_state == "menu":
        if start_button.collidepoint(pos):
            if sound_on: click_sound.play()
            reset_game()
            game_state = "game"
            collision_detected = False
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on: toggle_sound.play()
            music.set_volume(0.3 if sound_on else 0)
        elif quit_button.collidepoint(pos):
            if sound_on: click_sound.play()
            exit()
    elif game_state == "game_over" or game_state == "victory":
        reset_game()
        game_state = "menu"
        collision_detected = False

def on_key_down(key):
    global game_state, collision_detected
    if game_state == "game":
        if key == keys.ESCAPE:
            game_state = "menu"
            collision_detected = False
        elif key == keys.LEFT:
            hero.move(-1, 0)
        elif key == keys.RIGHT:
            hero.move(1, 0)
        elif key == keys.UP:
            hero.move(0, -1)
        elif key == keys.DOWN:
            hero.move(0, 1)
    elif (game_state == "game_over" or game_state == "victory") and key == keys.RETURN:
        reset_game()
        game_state = "menu"
        collision_detected = False

pgzrun.go()
