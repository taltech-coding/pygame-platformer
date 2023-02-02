import pygame

from lib import ui
from lib.game_level import GameLevel
from lib.scene import Scene


class MainMenu(Scene):
    BACKGROUND_COLOR = pygame.Color(64, 74, 104)

    def __init__(self, scene_switcher, game_title):
        super().__init__(scene_switcher)

        self.title = ui.FONT.render(game_title, True, ui.TEXT_COLOR)
        self.start_button = ui.Button("Start", on_pressed=lambda: scene_switcher(GameLevel(scene_switcher)))
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_scene)

    def render(self, screen: pygame.Surface):
        screen.fill(MainMenu.BACKGROUND_COLOR)
        screen.blit(self.title, ((screen.get_width() - self.title.get_width()) / 2, screen.get_height() * 0.2))

        self.quit_button.render(screen, (
            (screen.get_width() - self.quit_button.get_width()) / 2,
            screen.get_height() - self.quit_button.get_height() - 10))

        self.start_button.render(screen, (
            (screen.get_width() - self.start_button.get_width()) / 2,
            screen.get_height() - self.quit_button.get_height() - self.start_button.get_height() - 20))
