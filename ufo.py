import pygame as pg
from pygame.sprite import Sprite
from random import randint
from timer import Timer


class Ufo(Sprite):
    images = [pg.image.load(f"images/ufo/ufo_{x}.png") for x in range(2)]
    explosion_images_500 = [
        pg.transform.scale(
            pg.image.load(f"images/explosion_500/explode_500_0{x}.png"), (80, 80)
        )
        for x in range(5)
    ]

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.sound = game.sound
        self.settings = game.settings
        self.timer = Timer(Ufo.images, delta=6)
        self.explosiontimer = Timer(Ufo.explosion_images_500, delta=3, looponce=True)
        self.spawn_time = randint(5000, 10000)  # 5 to 10 seconds in milliseconds
        self.spawn_timer = (
            pg.time.get_ticks()
        )  # Initialize spawn timer with current tick
        self.active = False  # Initially, the UFO isn't active
        self.initialize()
        self.ship = game.ship

    def initialize(self):
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()
        self.isdying = False

    def update(self):
        current_time = pg.time.get_ticks()

        # Increment spawn timer and check if it's time to spawn the UFO
        if not self.active and (current_time - self.spawn_timer) >= self.spawn_time:
            print("Spawning UFO")
            self.timer = Timer(Ufo.images, delta=6)
            self.spawn()

        # Update UFO behavior when active
        if self.active:
            if not self.isdying:
                self.rect.x += self.speed
                if self.rect.right < 0 or self.rect.left > self.screen_rect.right:
                    print("Resetting UFO - moved off screen")
                    self.reset()
                if pg.sprite.collide_rect(self, self.game.ship):
                    self.game.ship.hit()
                    # self.reset()
            else:
                # Handle UFO explosion
                if self.timer.finished():
                    print("Resetting UFO - explosion finished")
                    self.reset()

            # Collision detection with ship's lasers
            if not self.isdying:
                if pg.sprite.spritecollide(
                    self, self.game.ship.lasers.lasergroup(), True
                ):
                    print("UFO hit")
                    self.hit()

            # Draw the UFO if it's active
            self.draw()

    def spawn(self):
        # Randomize starting side (left or right) and position at the top of the screen
        if randint(0, 1):
            self.rect.x = -self.rect.width
            self.speed = randint(2, 8)
        else:
            self.rect.x = self.screen_rect.right
            self.speed = -randint(2, 8)
        # self.rect.y = randint(0, self.screen_rect.height // 4)
        self.rect.y = 40

        self.active = True
        self.sound.play_music("sounds/stallord-2.wav")
        self.sound.set_volume(0.5)
        self.spawn_timer = pg.time.get_ticks()  # Reset spawn timer

    def reset(self):
        self.sound.set_volume(0.25)
        self.sound.play_music(self.sound.songs[self.sound.current_song])
        print("Resetting UFO properties")
        # Reset UFO state and prepare for next spawn
        self.active = False
        self.isdying = False
        self.initialize()  # Reinitialize UFO properties
        self.spawn_time = randint(5000, 10000)
        self.spawn_timer = pg.time.get_ticks()

    def hit(self):
        # Handle UFO hit logic
        print("UFO hit function")
        if not self.isdying:
            print("UFO is dying - changed timer and played sound")
            self.isdying = True
            self.timer = Timer(Ufo.explosion_images_500, delta=3, looponce=True)
            self.sound.play_ufo_explosion()
            self.game.stats.score += 500  # Update score
            self.game.sb.prep_score()  # Update the scoreboard

    def draw(self):
        if self.active:
            self.image = self.timer.current_image()
            self.screen.blit(self.image, self.rect)
