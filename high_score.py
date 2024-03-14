import sys, time
import pygame as pg
from button import Button


class HighScoreScreen:
    def __init__(self, game):
        self.game = game
        self.sound = game.sound
        # TODO: probably play song here
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.play_button = Button(
            game=self.game, text="Play", pos=(450, 640), selected_color=(255, 7, 58)
        )
        self.back_button = Button(
            game=self.game,
            text="Back",
            pos=(750, 640),
            selected_color=(9, 210, 255),
        )
        self.high_score = game.stats.high_score

    def display_title(self):
        title_space = pg.font.SysFont(None, 170).render(
            "SPACE", True, (255, 255, 255), self.game.settings.bg_color
        )
        title_space_rect = title_space.get_rect(center=(self.screen_rect.centerx, 70))

        title_invaders = pg.font.SysFont(None, 110).render(
            "INVADERS", True, (57, 255, 20), self.game.settings.bg_color
        )
        title_invaders_rect = title_invaders.get_rect(
            center=(self.screen_rect.centerx, title_space_rect.bottom + 15)
        )

        self.screen.blit(title_space, title_space_rect)
        self.screen.blit(title_invaders, title_invaders_rect)

    def display_high_score(self):
        highest_score_text = pg.font.SysFont(None, 170).render(
            "SPACE", True, (255, 255, 255), self.game.settings.bg_color
        )
        highest_score_text_rect = highest_score_text.get_rect(
            center=(self.screen_rect.centerx, 270)
        )

        top_score = str(self.high_score)
        actual_score_text = pg.font.SysFont(None, 110).render(
            top_score, True, (57, 255, 20), self.game.settings.bg_color
        )
        actual_score_text_rect = actual_score_text.get_rect(
            center=(self.screen_rect.centerx, highest_score_text_rect.bottom + 15)
        )

        self.screen.blit(highest_score_text, highest_score_text_rect)
        self.screen.blit(actual_score_text, actual_score_text_rect)

    def check_events(self):
        for event in pg.event.get():
            type = event.type
            if type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif type == pg.MOUSEBUTTONDOWN:
                b = self.play_button
                c = self.back_button
                x, y = pg.mouse.get_pos()
                if b.rect.collidepoint(x, y):
                    b.press()
                elif c.rect.collidepoint(x, y):
                    c.press()
            elif type == pg.MOUSEMOTION:
                b = self.play_button
                c = self.back_button
                x, y = pg.mouse.get_pos()
                b.select(b.rect.collidepoint(x, y))
                c.select(c.rect.collidepoint(x, y))

    def draw(self):
        self.screen.fill(self.game.settings.bg_color)
        self.display_title()
        self.display_alien_info()
        self.play_button.draw()
        self.back_button.draw()
        pg.display.flip()

    def run(self):
        self.play_button.clicked = False
        self.play_button.show()
        self.back_button.clicked = False
        self.back_button.show()
        self.sound.play_music("sounds/Melody.wav")
        while not self.game.game_active:
            self.play_button.update()
            self.back_button.update()
            self.check_events()
            self.draw()
            if self.play_button.clicked:
                self.game.play()
                break
            # elif self.back_button.pressed:
            # self.game.show_high_scores()
            # break
            # self.game.clock.tick(self.game.settings.fps)
