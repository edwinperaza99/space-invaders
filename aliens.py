import pygame as pg
import sys
from pygame.sprite import Sprite
from vector import Vector
from random import randint
from lasers import Lasers
from timer import Timer
from sound import Sound


class Alien(Sprite):
    names = ["bunny", "pig", "stalk_eyes", "w_heart", "w_pigtails", "wild_tentacles"]
    points = [60, 80, 100, 200, 300, 500]
    images = [pg.image.load(f"images/aliens/alien_{name}.png") for name in names]
    explosion_images_100 = [
        pg.transform.scale(
            pg.image.load(f"images/explosion_100/explode_100_0{x}.png"), (80, 80)
        )
        for x in range(0, 5)
    ]
    # nameslen = len(names)
    # choices = [randint(0, nameslen) for _ in range(nameslen)]

    li = [x * x for x in range(1, 11)]

    def __init__(self, game, row, alien_no):
        super().__init__()
        self.game = game
        self.sound = game.sound
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.regtimer = Timer(
            Alien.images, start_index=randint(0, len(Alien.images) - 1), delta=20
        )
        self.explosiontimer = Timer(Alien.explosion_images_100, delta=3, looponce=True)
        self.timer = self.regtimer

        self.image = Alien.images[row % len(Alien.names)]
        self.alien_no = alien_no
        # self.image = Alien.images[randint(0, 5)]
        # self.image = Alien.images[Alien.choices[row % len(Alien.names)]]
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.isdying = False
        self.reallydead = False

    def laser_offscreen(self, rect):
        return rect.bottom > self.screen_rect.bottom

    def laser_start_rect(self):
        rect = self.rect
        rect.midbottom = self.rect.midbottom
        return rect.copy()

    def get_explosion_timer(self, points=60):
        explode_images = [
            pg.transform.scale(
                pg.image.load(f"images/explosion_{points}/explode_{points}_0{x}.png"),
                (80, 80),
            )
            for x in range(0, 5)
        ]
        timer = Timer(image_list=explode_images, start_index=0, delta=3, looponce=True)
        return timer

    def hit(self, points):
        self.isdying = True
        # change the timer here

        self.explosiontimer = self.get_explosion_timer(points)
        self.timer = self.explosiontimer
        # TODO: play explosion audio here
        self.sound.play_alien_explosion()

    def fire(self, lasers):
        # print(f'Alien {self.alien_no} firing laser')
        lasers.add(owner=self)
        self.sound.play_alien_laser()

    def check_edges(self):
        r = self.rect
        sr = self.screen_rect
        return r.right >= sr.right or r.left < 0

    def check_bottom(self):
        return self.rect.bottom >= self.screen_rect.bottom

    def update(self, v, delta_y):
        self.x += v.x
        self.rect.x = self.x
        self.rect.y += delta_y
        if self.explosiontimer.finished():
            self.kill()
        self.draw()

    def draw(self):
        self.image = self.timer.current_image()
        self.screen.blit(self.image, self.rect)


class Aliens:
    laser_image_files = [f"images/alien_laser/alien_laser_0{x}.png" for x in range(2)]
    laser_images = [
        pg.transform.scale(pg.image.load(x), (50, 50)) for x in laser_image_files
    ]

    def __init__(self, game):
        self.game = game
        self.sound = game.sound
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats
        self.sb = game.sb
        self.aliens_created = 0
        self.v = Vector(self.settings.alien_speed, 0)
        self.laser_timer = Timer(image_list=Aliens.laser_images, delta=10)
        self.lasers = Lasers(
            game=game,
            v=Vector(0, 1) * self.settings.laser_speed,
            timer=self.laser_timer,
            owner=self,
        )

        self.alien_group = pg.sprite.Group()
        self.ship = game.ship
        self.alien_firing_now = 0
        self.fire_every_counter = 0
        self.create_fleet()

    def create_alien(self, x, y, row, alien_no):
        alien = Alien(self.game, row, alien_no)
        alien.x = x
        alien.rect.x, alien.rect.y = x, y
        self.alien_group.add(alien)

    def empty(self):
        self.alien_group.empty()

    def reset(self):
        self.alien_group.empty()
        self.lasers.empty()
        self.create_fleet()

    def create_fleet(self):
        self.fire_every_counter = 1  # changed from 0 to 1 to prevent first fire
        alien = Alien(self.game, row=0, alien_no=-1)
        alien_width, alien_height = alien.rect.size

        # TODO: add alien height to leave margin at the top (added the 2*alien_height to y)
        x, y, row = alien_width, 3 * alien_height, 0
        self.aliens_created = 0
        margin_bottom = 3 * alien_height  # variable to change distance from bottom
        while y < (self.settings.screen_height - margin_bottom):
            while x < (self.settings.screen_width - 2 * alien_width):
                self.create_alien(x=x, y=y, row=row, alien_no=self.aliens_created)
                x += self.settings.alien_spacing * alien_width
                self.aliens_created += 1
            x = alien_width
            y += self.settings.alien_spacing * alien_height
            row += 1

    def check_edges(self):
        for alien in self.alien_group.sprites():
            if alien.check_edges():
                return True
        return False

    def check_bottom(self):
        for alien in self.alien_group.sprites():
            if alien.check_bottom():
                return True
        return False

    def update(self):
        delta_y = 0
        if self.check_edges():
            delta_y = self.settings.fleet_drop
            self.v.x *= -1

        if self.check_bottom():
            self.ship.hit()

        # ship lasers taking out aliens
        # TODO: ADD CODE HERE FROM MIN 34:15 LECTURE 9
        collisions = pg.sprite.groupcollide(
            self.alien_group, self.ship.lasers.lasergroup(), False, True
        )
        if len(collisions) > 0:
            for alien in collisions:
                # do not run collision again if alien is already drying
                if not alien.isdying:
                    # TODO: check if this is working
                    index = alien.timer.current_index()
                    points = Alien.points[index]
                    alien.hit(points)
                    self.stats.score += points
                    # self.stats.score += self.settings.alien_points
                    self.sb.prep_score()
                    self.sb.check_high_score()

        # laser-laser collisions
        collisions = pg.sprite.groupcollide(
            self.ship.lasers.lasergroup(), self.lasers.lasergroup(), True, True
        )

        for alien in self.alien_group.sprites():
            alien.update(self.v, delta_y)

        # must have aliens to fire at the ship
        if (
            self.alien_group
            and self.fire_every_counter % self.settings.aliens_fireevery == 0
        ):
            n = randint(0, len(self.alien_group) - 1)
            self.alien_group.sprites()[n].fire(lasers=self.lasers)
        self.fire_every_counter += 1

        # update the positions of all of the aliens' lasers (the ship updates its own lasers)
        self.lasers.update()

        # no more aliens -- time to re-create the fleet
        if not self.alien_group:
            self.lasers.empty()
            self.create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            # change song here for new level
            self.sound.play_music(self.sound.select_song())

        # aliens hitting the ship
        if pg.sprite.spritecollideany(self.ship, self.alien_group):
            self.ship.hit()

        # alien lasers taking out the ship
        if pg.sprite.spritecollideany(self.ship, self.lasers.lasergroup()):
            self.ship.hit()


if __name__ == "__main__":
    print("\nERROR: aliens.py is the wrong file! Run play from alien_invasions.py\n")
