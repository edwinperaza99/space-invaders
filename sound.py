import pygame as pg
from pygame import mixer
import time


class Sound:
    def __init__(self, game):
        self.game = game
        mixer.init()
        self.ship_laser = mixer.Sound("sounds/ship_laser.wav")
        self.alien_laser = mixer.Sound("sounds/alien_laser.wav")
        self.alien_explosion = mixer.Sound("sounds/alien_explosion.wav")
        self.ship_explosion = mixer.Sound("sounds/ship_explosion.wav")
        self.ufo_explosion = mixer.Sound("sounds/fire_force.wav")
        # self.explosion = mixer.Sound("sounds/explosion.wav")
        self.current_song = 0
        self.songs = ["sounds/Melody.wav", "sounds/koala.wav", "sounds/This_Groove.wav"]
        self.volume = 0.25
        self.set_volume(self.volume)
        self.set_effects_volume(
            ship=0.15,
            alien=0.05,
            alien_explosion=0.5,
            ship_explosion=0.25,
            ufo_explosion=0.5,
        )

    def reset(self):
        self.current_song = 0
        self.set_volume(self.volume)

    def select_song(self):
        if self.current_song == (len(self.songs) - 1):
            self.current_song = 0
        else:
            self.current_song += 1
        return self.songs[self.current_song]

    def set_effects_volume(
        self,
        ship=0.25,
        alien=0.04,
        alien_explosion=0.5,
        ship_explosion=0.25,
        ufo_explosion=0.5,
    ):
        self.ship_laser.set_volume(ship)
        self.alien_laser.set_volume(alien)
        self.alien_explosion.set_volume(alien_explosion)
        self.ship_explosion.set_volume(ship_explosion)
        self.ufo_explosion.set_volume(ufo_explosion)

    def set_volume(self, volume=0.3):
        mixer.music.set_volume(volume)

    def play_music(self, filename):
        self.stop_music()
        mixer.music.load(filename)
        mixer.music.play(-1)

    def play_once(self, filename):
        self.stop_music()
        mixer.music.load(filename)
        mixer.music.play(0)

    def pause_music(self):
        mixer.music.pause()

    def unpause_music(self):
        mixer.music.unpause()

    def stop_music(self):
        mixer.music.stop()

    def play_ship_laser(self):
        mixer.Sound.play(self.ship_laser)

    def play_alien_laser(self):
        mixer.Sound.play(self.alien_laser)

    def play_alien_explosion(self):
        mixer.Sound.play(self.alien_explosion)

    def play_ship_explosion(self):
        mixer.Sound.play(self.ship_explosion)

    def play_ufo_explosion(self):
        mixer.Sound.play(self.ufo_explosion)

    def play_game_over(self):
        self.stop_music()
        self.ship_laser.stop()
        self.alien_laser.stop()
        # sleep for last laser sound
        # time.sleep(2)
        self.set_volume(1)
        self.play_once("sounds/game_over.wav")
        # have to sleep for however long the last sound is...
        time.sleep(6)
        self.set_volume(self.volume)
        self.stop_music()
