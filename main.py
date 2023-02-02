import pygame

from lib import ui
from lib.main_menu import MainMenu
from lib.scene import Scene

INITIAL_SCREEN_SIZE = 1000, 500
GAME_TITLE = "Your game name here"

current_scene: Scene


def scene_switcher(new_scene: Scene):
    global current_scene
    current_scene = new_scene


def main():
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    screen = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
    ui.initialise_font()

    scene_switcher(MainMenu(scene_switcher, GAME_TITLE))

    while current_scene.is_running:
        current_scene.handle_events()
        current_scene.update()
        current_scene.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
