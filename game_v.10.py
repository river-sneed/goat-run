#!/usr/bin/env python3

import json
import pygame
import sys
import time

pygame.mixer.pre_init()
pygame.init()

# Window settings
TITLE = "Goat Run"
WIDTH = 1280
HEIGHT = 640
FPS = 60
GRID_SIZE = 64

# Options
music_on = True
sound_on = True


# Controls
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
JUMP = pygame.K_SPACE
MUSIC = pygame.K_m
SOUND = pygame.K_s

# Levels
levels = ["levels/world-1.json",
          "levels/world-2.json",
          "levels/world-4.json"]

# Colors
TRANSPARENT = (0, 0, 0, 0)
DARK_BLUE = (16, 86, 103)
WHITE = (255, 255, 255)

# Fonts
FONT_SM = pygame.font.Font("assets/fonts/hemi_head.ttf", 32)
FONT_MD = pygame.font.Font("assets/fonts/hemi_head.ttf", 64)
FONT_LG = pygame.font.Font("assets/fonts/hemi_head.ttf", 72)

# Helper functions
def load_image(file_path, width=GRID_SIZE, height=GRID_SIZE):
    img = pygame.image.load(file_path)
    img = pygame.transform.scale(img, (width, height))

    return img

def play_sound(sound, loops=0, maxtime=0, fade_ms=0):
    if sound_on:
        if maxtime == 0:
            sound.play(loops, maxtime, fade_ms)
        else:
            sound.play(loops, maxtime, fade_ms)
            
    elif sound_on == False:
        pass

def play_music():
    if music_on:
        pygame.mixer.music.play(-1)

    elif music_on == False:
        pass

def pause(state):
    if state:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
        
# Images
hero_walk1 = load_image("assets/goat/goat_walk1.png")
hero_walk2 = load_image("assets/goat/goat_walk2.png")
hero_jump = load_image("assets/goat/goat_jump.png")
hero_idle = load_image("assets/goat/goat_idle.png")
hero_bounce = load_image("assets/goat/goat_bounce.png")
hero_images = {"run": [hero_walk1, hero_walk2],
               "jump": hero_jump,
               "idle": hero_idle,
               "bounce": hero_bounce}

block_images = {"GTL": load_image("assets/goat_tiles/grass_top_left.png"),
                "GTM": load_image("assets/goat_tiles/grass_top_middle.png"),
                "GTR": load_image("assets/goat_tiles/grass_top_right.png"),
                "GFR": load_image("assets/goat_tiles/grass_float_right.png"),
                "GFL": load_image("assets/goat_tiles/grass_float_left.png"),
                "GTP": load_image("assets/goat_tiles/grass_top.png"),
                "GFC": load_image("assets/goat_tiles/grass_float_center.png"),
                "GL": load_image("assets/goat_tiles/grass_float_lone.png"),
                "GC": load_image("assets/goat_tiles/grass_center.png"),
                "SP": load_image("assets/goat_tiles/special.png"),
                "PT": load_image("assets/goat_tiles/pop_tart.png"),
                "RB": load_image("assets/goat_tiles/rock_bottom.png"),
                "RC": load_image("assets/goat_tiles/rock_center.png"),
                "SC": load_image("assets/goat_tiles/sand_center.png"),
                "STM": load_image("assets/goat_tiles/sand_top_middle.png"),
                "MTL": load_image("assets/goat_tiles/mars_top_left.png"),
                "MTM": load_image("assets/goat_tiles/mars_top_middle.png"),
                "MTR": load_image("assets/goat_tiles/mars_top_right.png"),
                "MFR": load_image("assets/goat_tiles/mars_float_right.png"),
                "MFL": load_image("assets/goat_tiles/mars_float_left.png"),
                "MTP": load_image("assets/goat_tiles/mars_top.png"),
                "MFC": load_image("assets/goat_tiles/mars_float_center.png"),
                "ML": load_image("assets/goat_tiles/mars_float_lone.png"),
                "MC": load_image("assets/goat_tiles/mars_center.png"),}

'''bear_images = {"norm_bear": load_image("assets/enemies/bear-1.png"),
               "sp_bear": load_image("assets/enemies/space_bear.png"),
               "uw_bear": load_image("assets/enemies/under_water_bear.png"),}'''

coin_img = load_image("assets/getables/hay.png")
lives_img = load_image("assets/goat/lives.png")
no_lives_img = load_image("assets/goat/no_lives.png")
heart_img = load_image("assets/getables/heart.png")
lives_progress_horn_0_img = load_image("assets/goat/lives_progress_horn_0.png", 100, 64)
lives_progress_horn_1_img = load_image("assets/goat/lives_progress_horn_1.png", 100, 64)
lives_progress_horn_2_img = load_image("assets/goat/lives_progress_horn_2.png", 100, 64)
lives_progress_horn_3_img = load_image("assets/goat/lives_progress_horn_3.png", 100, 64)
music_img = load_image("assets/sounds/music_img.png", 40, 40)
no_music_img = load_image("assets/sounds/no_music_img.png", 40, 40)
sound_img = load_image("assets/sounds/sound_img.png", 40, 40)
no_sound_img = load_image("assets/sounds/no_sound_img.png", 40, 40)
empty_heart_img = load_image("assets/getables/heart_empty.png")
oneup_img = load_image("assets/getables/first_aid.png")
flag_img = load_image("assets/getables/flag.png")
flagpole_img = load_image("assets/getables/flagpole.png")

splash_screen_img = load_image("assets/splash_screen.png", 1280, 640)

farmer_img1 = load_image("assets/enemies/farmer_1.png")
farmer_img2 = load_image("assets/enemies/farmer_2.png")
farmer_images = [farmer_img1, farmer_img2]

bear_img = load_image("assets/enemies/bear-1.png")
bear_images = [bear_img]

under_water_bear_img = load_image("assets/enemies/under_water_bear.png")
under_water_bear_images = [under_water_bear_img]


# Sounds
JUMP_SOUND = pygame.mixer.Sound("assets/sounds/jump.wav")
COIN_SOUND = pygame.mixer.Sound("assets/sounds/belch.ogg")
POWERUP_SOUND = pygame.mixer.Sound("assets/sounds/powerup.wav")
HURT_SOUND = pygame.mixer.Sound("assets/sounds/hurt_goat_bleat.ogg")
DIE_SOUND = pygame.mixer.Sound("assets/sounds/goat_bleat.ogg")
LEVELUP_SOUND = pygame.mixer.Sound("assets/sounds/level_up.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("assets/sounds/farts.ogg")
KILL_SOUND = pygame.mixer.Sound("assets/sounds/quick_fart.ogg")

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vy = 0
        self.vx = 0

    def apply_gravity(self, level):
        self.vy += level.gravity
        self.vy = min(self.vy, level.terminal_velocity)

class Block(Entity):

    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Character(Entity):

    def __init__(self, images):
        super().__init__(0, 0, images['idle'])

        self.image_idle_right = images['idle']
        self.image_idle_left = pygame.transform.flip(self.image_idle_right, 1, 0)
        self.images_run_right = images['run']
        self.images_run_left = [pygame.transform.flip(img, 1, 0) for img in self.images_run_right]
        self.image_jump_right = images['jump']
        self.image_jump_left = pygame.transform.flip(self.image_jump_right, 1, 0)
        self.image_bounce_right = images['bounce']
        self.image_bounce_left = pygame.transform.flip(self.image_bounce_right, 1, 0)
        

        self.running_images = self.images_run_right
        self.image_index = 0
        self.steps = 0

        self.speed = 7
        self.jump_power = 20
                

        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.on_ground = True
        self.bounce = False

        self.score = 0
        self.coin_count = 0
        self.lives = 3
        self.get_life = 0
        self.hearts = 3
        self.max_hearts = 3
        self.invincibility = 0

    def move_left(self):
        self.vx = -self.speed
        self.facing_right = False

    def move_right(self):
        self.vx = self.speed
        self.facing_right = True

    def stop(self):
        self.vx = 0

    def jump(self, level):
        blocks = level.blocks
        
        if level.free_jump == 1:
            self.vy = -1 * self.jump_power
            play_sound(JUMP_SOUND)

        else:
            self.rect.y += 1

            hit_list = pygame.sprite.spritecollide(self, blocks, False)

            if len(hit_list) > 0:
                self.vy = -1 * self.jump_power
                play_sound(JUMP_SOUND)

            self.rect.y -= 1

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level.width:
            self.rect.right = level.width

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.vx = 0

        self.on_ground = False
        self.rect.y += self.vy + 1
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
                self.on_ground = True
                self.bounce = False
            elif self.vy < 0:
                self.rect.top = (block.rect.bottom)
                self.vy = 0

    def process_coins(self, coins):
        hit_list = pygame.sprite.spritecollide(self, coins, True)

        for coin in hit_list:
            play_sound(COIN_SOUND)
            self.score += coin.value
            self.coin_count += 1

    def process_enemies(self, enemies):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)

        for h in hit_list:
            if len(hit_list) > 0 and self.invincibility == 0 and self.vy <= 0:
                play_sound(HURT_SOUND)
                self.hearts -= 1
                self.invincibility = int(0.75 * FPS)

            
            elif len(hit_list) > 0 and self.invincibility == 0 and self.vy >= 0 and (((h.rect.y) - (self.rect.y)) / 3) >= 15:
                pygame.sprite.Sprite.kill(h)
                self.vy  = 0
                self.vy -= 17                
                play_sound(KILL_SOUND)
                self.score += h.value
                self.bounce = True

            else:
                pass

            
    def process_powerups(self, powerups):
        hit_list = pygame.sprite.spritecollide(self, powerups, True)

        for p in hit_list:
            play_sound(POWERUP_SOUND)
            p.apply(self)

    def check_flag(self, level):
        hit_list = pygame.sprite.spritecollide(self, level.flag, False)

        if len(hit_list) > 0:
            level.completed = True
            play_sound(LEVELUP_SOUND)

    def set_image(self):
        if self.on_ground:
            if self.vx != 0:
                if self.facing_right:
                    self.running_images = self.images_run_right
                else:
                    self.running_images = self.images_run_left

                self.steps = (self.steps + 1) % self.speed # Works well with 2 images, try lower number if more frames are in animation

                if self.steps == 0:
                    self.image_index = (self.image_index + 1) % len(self.running_images)
                    self.image = self.running_images[self.image_index]
            else:
                if self.facing_right:
                    self.image = self.image_idle_right
                else:
                    self.image = self.image_idle_left
        else:
            if self.bounce == True:

                if self.facing_right:
                    self.image = self.image_bounce_right
                else:
                    self.image = self.image_bounce_left

            else:
                if self.facing_right:
                    self.image = self.image_jump_right
                else:
                    self.image = self.image_jump_left
                



    def die(self):
        self.lives -= 1

        if self.lives > 0:
            play_sound(DIE_SOUND)
        else:
            play_sound(GAMEOVER_SOUND)

    def respawn(self, level):
        self.rect.x = level.start_x
        self.rect.y = level.start_y
        self.hearts = self.max_hearts
        self.invincibility = 0
        self.facing_right = True

    def update(self, level):
        self.process_enemies(level.enemies)
        self.apply_gravity(level)
        self.move_and_process_blocks(level.blocks)
        self.check_world_boundaries(level)
        self.set_image()

        if self.hearts > 0:
            self.process_coins(level.coins)
            self.process_powerups(level.powerups)
            self.check_flag(level)

            if self.invincibility > 0:
                self.invincibility -= 1
        else:
            self.die()

class Coin(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 5

class Enemy(Entity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images_left = images
        self.images_right = [pygame.transform.flip(img, 1, 0) for img in images]
        self.current_images = self.images_left
        self.image_index = 0
        self.steps = 0

    def reverse(self):
        self.vx *= -1

        if self.vx < 0:
            self.current_images = self.images_left
        else:
            self.current_images = self.images_right

        self.image = self.current_images[self.image_index]

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > level.width:
            self.rect.right = level.width
            self.reverse()

    def move_and_process_blocks(self):
        pass

    def set_images(self):
        if self.steps == 0:
            self.image = self.current_images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.current_images)

        self.steps = (self.steps + 1) % 20 # Nothing significant about 20. It just seems to work okay.

    def is_near(self, hero):
        return abs(self.rect.x - hero.rect.x) < 2 * WIDTH



    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vx = self.start_vx
        self.vy = self.start_vy
        self.current_images = self.images_left
        self.image = self.current_images[0]
        self.steps = 0

class Bear(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.value = 15
        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy + 1
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

    def update(self, level, hero):
        if self.is_near(hero):
            self.apply_gravity(level)
            self.move_and_process_blocks(level.blocks)
            self.check_world_boundaries(level)
            self.set_images()

class Under_water_bear(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.value = 10
        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

        

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

    def update(self, level, hero):
        if self.is_near(hero):
            self.move_and_process_blocks(level.blocks)
            self.check_world_boundaries(level)
            self.set_images()


class Farmer(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.value = 15
        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        reverse = False

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy + 1
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        reverse = True

        for block in hit_list:
            if self.vy >= 0:
                self.rect.bottom = block.rect.top
                self.vy = 0

                if self.vx > 0 and self.rect.right <= block.rect.right:
                    reverse = False

                elif self.vx < 0 and self.rect.left >= block.rect.left:
                    reverse = False

            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

        if reverse:
            self.reverse()

    def update(self, level, hero):
        if self.is_near(hero):
            self.apply_gravity(level)
            self.move_and_process_blocks(level.blocks)
            self.check_world_boundaries(level)
            self.set_images()

class OneUp(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 20
        
    def apply(self, character):
        character.lives += 1

class Heart(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 10
        
    def apply(self, character):
        character.hearts += 1
        character.hearts = max(character.hearts, character.max_hearts)

class Flag(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 35
        
class Level():

    def __init__(self, file_path):
        self.starting_blocks = []
        self.starting_enemies = []
        self.starting_coins = []
        self.starting_powerups = []
        self.starting_flag = []

        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.flag = pygame.sprite.Group()

        self.active_sprites = pygame.sprite.Group()
        self.inactive_sprites = pygame.sprite.Group()

        with open(file_path, 'r') as f:
            data = f.read()

        map_data = json.loads(data)

        self.width = map_data['width'] * GRID_SIZE
        self.height = map_data['height'] * GRID_SIZE

        self.start_x = map_data['start'][0] * GRID_SIZE
        self.start_y = map_data['start'][1] * GRID_SIZE

        for item in map_data['blocks']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            img = block_images[item[2]]
            self.starting_blocks.append(Block(x, y, img))

        for item in map_data['bears']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Bear(x, y, bear_images))

        for item in map_data['under_water_bears']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Under_water_bear(x, y, under_water_bear_images))

        for item in map_data['farmers']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Farmer(x, y, farmer_images))

        for item in map_data['coins']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_coins.append(Coin(x, y, coin_img))

        for item in map_data['oneups']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(OneUp(x, y, oneup_img))

        for item in map_data['hearts']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Heart(x, y, heart_img))

        for i, item in enumerate(map_data['flag']):
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE

            if i == 0:
                img = flag_img
            else:
                img = flagpole_img

            self.starting_flag.append(Flag(x, y, img))

        self.background_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.scenery_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.inactive_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)

        if map_data['background-color'] != "":
            self.background_layer.fill(map_data['background-color'])

        if map_data['background-img'] != "":
            background_img = pygame.image.load(map_data['background-img'])

            if map_data['background-fill-y']:
                h = background_img.get_height()
                w = int(background_img.get_width() * HEIGHT / h)
                background_img = pygame.transform.scale(background_img, (w, HEIGHT))

            if "top" in map_data['background-position']:
                start_y = 0
            elif "bottom" in map_data['background-position']:
                start_y = self.height - background_img.get_height()

            if map_data['background-repeat-x']:
                for x in range(0, self.width, background_img.get_width()):
                    self.background_layer.blit(background_img, [x, start_y])
            else:
                self.background_layer.blit(background_img, [0, start_y])

        if map_data['scenery-img'] != "":
            scenery_img = pygame.image.load(map_data['scenery-img'])

            if map_data['scenery-fill-y']:
                h = scenery_img.get_height()
                w = int(scenery_img.get_width() * HEIGHT / h)
                scenery_img = pygame.transform.scale(scenery_img, (w, HEIGHT))

            if "top" in map_data['scenery-position']:
                start_y = 0
            elif "bottom" in map_data['scenery-position']:
                start_y = self.height - scenery_img.get_height()

            if map_data['scenery-repeat-x']:
                for x in range(0, self.width, scenery_img.get_width()):
                    self.scenery_layer.blit(scenery_img, [x, start_y])
            else:
                self.scenery_layer.blit(scenery_img, [0, start_y])

        pygame.mixer.music.load(map_data['music'])

        self.gravity = map_data['gravity']
        self.terminal_velocity = map_data['terminal-velocity']
        self.free_jump = map_data['free_jump']

        self.completed = False

        self.blocks.add(self.starting_blocks)
        self.enemies.add(self.starting_enemies)
        self.coins.add(self.starting_coins)
        self.powerups.add(self.starting_powerups)
        self.flag.add(self.starting_flag)

        self.active_sprites.add(self.coins, self.enemies, self.powerups)
        self.inactive_sprites.add(self.blocks, self.flag)

        self.inactive_sprites.draw(self.inactive_layer)

    def reset(self):
        self.enemies.add(self.starting_enemies)
        self.coins.add(self.starting_coins)
        self.powerups.add(self.starting_powerups)

        self.active_sprites.add(self.coins, self.enemies, self.powerups)

        for e in self.enemies:
            e.reset()

class Game():

    SPLASH = 0
    START = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETED = 4
    GAME_OVER = 5
    VICTORY = 6

    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.done = False

        self.reset()

    def start(self):
        self.level = Level(levels[self.current_level])
        self.level.reset()
        self.hero.respawn(self.level)

    def advance(self):
        self.current_level += 1
        self.start()
        self.stage = Game.START

    def reset(self):
        self.hero = Character(hero_images)
        self.current_level = 0
        self.start()
        self.stage = Game.SPLASH

    def display_splash(self, surface):
        line1 = FONT_LG.render(TITLE, 1, DARK_BLUE)
        line2 = FONT_SM.render("Press any key to start.", 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - line2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

        #surface.blit(splash_screen_img, [0, 0])

    def display_message(self, surface, primary_text, secondary_text):
        line1 = FONT_MD.render(primary_text, 1, WHITE)
        line2 = FONT_SM.render(secondary_text, 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - line2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

       

    def display_stats(self, surface):
        y = 0
        hearts_text = FONT_SM.render("Hearts: " + str(self.hero.hearts), 1, WHITE)
        lives_text = FONT_SM.render(" X " + str(self.hero.lives), 1, WHITE)
        score_text = FONT_SM.render("Score: " + str(self.hero.score), 1, WHITE)
        level_text = FONT_SM.render("Level: " + str(self.current_level + 1), 1, WHITE)
        coins_text = FONT_SM.render("Hay : " + str(self.hero.coin_count), 1, WHITE)

        surface.blit(score_text, (WIDTH - score_text.get_width() - 32, 32))
        surface.blit(coins_text, (WIDTH - coins_text.get_width() - 32, 100))
        #surface.blit(hearts_text, (32, 32))
        #surface.blit(lives_text, (32, 64))

        for x in range(self.hero.max_hearts):
            if x < self.hero.hearts:
                surface.blit(heart_img, [x * 64, y])

            else:
                surface.blit(empty_heart_img, [x * 64, y])

        if self.hero.hearts > self.hero.max_hearts:
            self.hero.get_life += 1
            self.hero.hearts = self.hero.max_hearts

        if self.hero.hearts < self.hero.max_hearts:
            self.hero.get_life = 0

        if self.hero.get_life == 0:
            surface.blit(lives_progress_horn_0_img, [x * 64 + 64, y])

        elif self.hero.get_life == 1:
            surface.blit(lives_progress_horn_1_img, [x * 64 + 64, y])

        elif self.hero.get_life == 2:
            surface.blit(lives_progress_horn_2_img, [x * 64 + 64, y])

        elif self.hero.get_life == 3:
            self.hero.lives + 1
            surface.blit(lives_progress_horn_3_img, [x * 64 + 64, y])
            self.hero.get_life = 0

        if self.hero.lives >= 1:
            surface.blit(lives_img, [1, 60])
            
        elif self.hero.lives < 1:
            surface.blit(no_lives_img, [1, 60])

        if music_on == True:
            surface.blit(music_img, (WIDTH - (music_img.get_width() + 32), 64))

        elif music_on == False:
            surface.blit(no_music_img, (WIDTH - (music_img.get_width() + 32), 64))

        if sound_on == True:
            surface.blit(sound_img, (WIDTH - (music_img.get_width() + sound_img.get_width() + 32), 64))

        elif sound_on == False:
            surface.blit(no_sound_img, (WIDTH - (music_img.get_width() + sound_img.get_width() + 32), 64))

            
        surface.blit(lives_text, (60, 80))
        surface.blit(level_text, (20, 130))
        
        
    def process_events(self):
        global sound_on, music_on
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            elif event.type == pygame.KEYDOWN:
                if self.stage == Game.SPLASH or self.stage == Game.START:
                    self.stage = Game.PLAYING
                    play_music()

                if event.key == MUSIC:
                    pause(music_on)
                    if music_on:
                        music_on = False
                    else:
                        music_on = True
                
                if event.key == SOUND:
                    sound_on = not sound_on


                elif self.stage == Game.PLAYING:
                    if event.key == JUMP:
                        self.hero.jump(self.level)

                elif self.stage == Game.PAUSED:
                    sound_on = False
                    pygame.mixer.music.stop()

                elif self.stage == Game.LEVEL_COMPLETED:
                    self.advance()

                elif self.stage == Game.VICTORY or self.stage == Game.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset()



        pressed = pygame.key.get_pressed()

        if self.stage == Game.PLAYING:
            if pressed[LEFT]:
                self.hero.move_left()
            elif pressed[RIGHT]:
                self.hero.move_right()
            else:
                self.hero.stop()

    def update(self):
        if self.stage == Game.PLAYING:
            self.hero.update(self.level)
            self.level.enemies.update(self.level, self.hero)

        if self.level.completed:
            if self.current_level < len(levels) - 1:
                self.stage = Game.LEVEL_COMPLETED
            else:
                self.stage = Game.VICTORY
            pygame.mixer.music.stop()

        elif self.hero.lives == 0:
            self.stage = Game.GAME_OVER
            pygame.mixer.music.stop()

        elif self.hero.hearts == 0:
            self.level.reset()
            self.hero.respawn(self.level)

    def calculate_offset(self):
        x = -1 * self.hero.rect.centerx + WIDTH / 2

        if self.hero.rect.centerx < WIDTH / 2:
            x = 0
        elif self.hero.rect.centerx > self.level.width - WIDTH / 2:
            x = -1 * self.level.width + WIDTH

        return x, 0

    def draw(self):
        offset_x, offset_y = self.calculate_offset()

        self.level.active_layer.fill(TRANSPARENT)
        self.level.active_sprites.draw(self.level.active_layer)

        if self.hero.invincibility % 3 < 2:
            self.level.active_layer.blit(self.hero.image, [self.hero.rect.x, self.hero.rect.y])

        self.window.blit(self.level.background_layer, [offset_x / 3, offset_y])
        self.window.blit(self.level.scenery_layer, [offset_x / 2, offset_y])
        self.window.blit(self.level.inactive_layer, [offset_x, offset_y])
        self.window.blit(self.level.active_layer, [offset_x, offset_y])

        self.display_stats(self.window)

        if self.stage == Game.SPLASH:
            self.display_splash(self.window)
        elif self.stage == Game.START:
            self.display_message(self.window, "Ready?!!!", "Press any key to start.")
        elif self.stage == Game.PAUSED:
            pass
        elif self.stage == Game.LEVEL_COMPLETED:
            self.display_message(self.window, "Level Complete", "Press any key to continue.")
        elif self.stage == Game.VICTORY:
            self.display_message(self.window, "You Win!", "Press 'R' to restart.")
        elif self.stage == Game.GAME_OVER:
            self.display_message(self.window, "Game Over", "Press 'R' to restart.")

        pygame.display.flip()

    def loop(self):
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.start()
    game.loop()
    pygame.quit()
    sys.exit()
