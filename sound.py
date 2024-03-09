import pygame as pg
from pygame import mixer
import time


class Sound:
    def __init__(self, game):
        self.game = game
        mixer.init()
        self.ship_laser = mixer.Sound("sounds/ship_laser.wav")
        self.alien_laser = mixer.Sound("sounds/alien_laser.wav")
        # self.explosion = mixer.Sound("sounds/explosion.wav")
        self.volume = 0.5
        self.set_volume(self.volume)
        self.set_effects_volume(ship=0.3, alien=0.05)

    def set_effects_volume(self, ship=0.3, alien=0.05):
        self.ship_laser.set_volume(ship)
        self.alien_laser.set_volume(alien)

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

    # def play_sound(self, soundname):
    #     mixer.Sound.play(soundname)

    def play_ship_laser(self):
        mixer.Sound.play(self.ship_laser)

    def play_alien_laser(self):
        mixer.Sound.play(self.alien_laser)

    # def play_bullet(self):
    #     mixer.Sound.play(self.bullet)

    # def play_explosion(self):
    #     mixer.Sound.play(self.explosion)

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
