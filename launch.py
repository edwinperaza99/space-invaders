import sys, time
import pygame as pg
from button import Button


class LaunchScreen:
    def __init__(self, game):
        self.game = game
        self.sound = game.sound
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.play_button = Button(
            game=self.game, text="Play", pos=(450, 640), selected_color=(255, 7, 58)
        )
        self.high_score_button = Button(
            game=self.game,
            text="High Score",
            pos=(750, 640),
            selected_color=(9, 210, 255),
        )
        self.names = [
            "bunny",
            "pig",
            "stalk_eyes",
            "w_heart",
            "w_pigtails",
            "wild_tentacles",
        ]
        self.points = [10, 25, 50, 100, 250, 500]
        self.images = [
            pg.image.load(f"images/aliens/alien_{name}.png") for name in self.names
        ]

    def display_alien_info(self):
        max_image_width = max(image.get_width() for image in self.images)
        for i in range(len(self.names)):
            image = self.images[i]
            points = self.points[i]
            image_rect = image.get_rect()
            image_rect.x = (self.screen_rect.width - max_image_width) // 2.2
            image_rect.y = 200 + i * image_rect.height
            self.screen.blit(image, image_rect)

            font = pg.font.SysFont(None, 48)
            text = font.render(
                f"= {points}", True, (255, 255, 255), self.game.settings.bg_color
            )
            text_rect = text.get_rect()
            text_rect.left = image_rect.right + 20
            text_rect.centery = image_rect.centery
            self.screen.blit(text, text_rect)

    def display_title(self):
        title_space = pg.font.SysFont(None, 170).render(
            "SPACE", True, (255, 255, 255), self.game.settings.bg_color
        )
        title_space_rect = title_space.get_rect(center=(self.screen_rect.centerx, 70))

        title_invaders = pg.font.SysFont(None, 110).render(
            "INVADERS", True, (57, 255, 20), self.game.settings.bg_color
        )
        title_invaders_rect = title_invaders.get_rect(
            center=(self.screen_rect.centerx, title_space_rect.bottom + 20)
        )

        self.screen.blit(title_space, title_space_rect)
        self.screen.blit(title_invaders, title_invaders_rect)

    def check_events(self):
        for event in pg.event.get():
            type = event.type
            if type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif type == pg.MOUSEBUTTONDOWN:
                b = self.play_button
                c = self.high_score_button
                x, y = pg.mouse.get_pos()
                if b.rect.collidepoint(x, y):
                    b.press()
                elif c.rect.collidepoint(x, y):
                    c.click()
            elif type == pg.MOUSEMOTION:
                b = self.play_button
                c = self.high_score_button
                x, y = pg.mouse.get_pos()
                b.select(b.rect.collidepoint(x, y))
                c.select(c.rect.collidepoint(x, y))

    def draw(self):
        self.screen.fill(self.game.settings.bg_color)
        self.display_title()
        self.display_alien_info()
        self.play_button.draw()
        self.high_score_button.draw()
        pg.display.flip()

    def run(self):
        self.play_button.clicked = False
        self.play_button.show()
        self.high_score_button.clicked = False
        self.high_score_button.show()
        if not pg.mixer.music.get_busy():
            self.sound.play_music("sounds/space_invaders.wav")
        while not self.game.game_active:
            self.play_button.update()
            self.high_score_button.update()
            self.check_events()
            self.draw()
            if self.play_button.clicked:
                self.game.play()
                break
            elif self.high_score_button.clicked:
                self.game.show_high_scores_screen()  # Transition to high scores screen
                break


if __name__ == "__main__":
    print("\nERROR: launch.py is the wrong file! Run play from game.py\n")
