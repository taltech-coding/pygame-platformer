import pygame

from typing import Callable

TEXT_COLOR = pygame.Color(154, 147, 183)

BUTTON_TEXT_COLOR = COLOR = pygame.Color(64, 74, 104)
BUTTON_COLOR = pygame.Color(103, 143, 203)
BUTTON_HOVER_COLOR = pygame.Color(139, 225, 224)
BUTTON_PADDING = 15

FONT: pygame.font.Font


def initialise_font():
    global FONT
    FONT = pygame.font.Font("assets/font/SourceSansPro-Regular.ttf", 25)


class Button(pygame.Surface):

    def __init__(self, button_text: str, on_pressed: Callable):
        self.text = button_text
        self.on_pressed = on_pressed
        self.font_surface = FONT.render(button_text, True, BUTTON_TEXT_COLOR)
        self.is_down = False

        button_size = self.font_surface.get_rect().inflate(BUTTON_PADDING, BUTTON_PADDING).size
        super().__init__(button_size)

    def render(self, screen: pygame.Surface, position):
        is_mouse_pressed = pygame.mouse.get_pressed(3)[0]
        button_color = BUTTON_HOVER_COLOR if self.is_down else BUTTON_COLOR

        detection_rect = pygame.draw.rect(screen, button_color, pygame.Rect(position, self.get_size()))
        screen.blit(self.font_surface, (position[0] + BUTTON_PADDING / 2, position[1] + BUTTON_PADDING / 2))

        if self.is_down and not is_mouse_pressed:
            self.on_pressed()

        self.is_down = is_mouse_pressed and detection_rect.collidepoint(pygame.mouse.get_pos())
