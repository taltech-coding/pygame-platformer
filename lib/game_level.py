import pygame

from lib import ui, level_geometry
from lib.monster import Monster
from lib.player import Player
from lib.scene import Scene


class GameLevel(Scene):
    GAME_CAMERA_SIZE = 500, 250
    BACKGROUND_COLOR = pygame.Color(154, 147, 183)
    EXAMPLE_LEVEL = """
########################################################################
#######     ############################################################
####            ########################################################
#### F    M  #          ###    ##########              #################
################                                           #############
##################          #### ## ###     ### #  #           #########
####       ###########   #            #######         ##         #######
###             #######                 ###               ##      ######
###                ##                                        ##   ######
###        #                                                     #######
####       ##                                                     ######
#####  P ###########    ####  ##     #######   #####    #    ###########
######################        ####    ######    ####    #    ###########
######################SSSSSSSS##      #####     ####SSSS#SSSS###########
################################    #####       ########################
##################################             #########################
#####################################  M   #############################
########################################################################
"""

    def __init__(self, scene_switcher):  # level data as param
        super().__init__(scene_switcher)

        self.quit_button = ui.Button("Quit", on_pressed=self.quit_scene)  # TODO Update with the currrent screen size

        self.collision_layer = pygame.sprite.Group()  # Check if it needs to be self.
        self.sprites = pygame.sprite.Group()
        self.player = Player(self.collision_layer)

        self.game_camera = pygame.surface.Surface(GameLevel.GAME_CAMERA_SIZE)

        self.build_level_from_data()

        self.previous_frame_time = 0
        self.running = True
        self.clock = pygame.time.Clock()

    def update(self):
        # self.clock.tick(30)
        frame_time = pygame.time.get_ticks()
        delta = (frame_time - self.previous_frame_time) / 1000.0
        self.previous_frame_time = frame_time

        if delta > 0.1:
            delta = 0

        self.sprites.update(delta=delta, camera_offset=pygame.Vector2(0, 0))
        # self.clock.tick()

    def draw_game_world(self):
        pass

    def draw_ui(self, screen: pygame.Surface):
        pass

    def render(self, screen: pygame.Surface):
        camera_offset = self.player.position - (pygame.Vector2(self.game_camera.get_size()) - self.player.rect.size) / 2
        self.game_camera.fill(GameLevel.BACKGROUND_COLOR)

        for sprite in self.sprites:
            self.game_camera.blit(sprite.image, sprite.rect.center - camera_offset)

        screen.blit(pygame.transform.scale(self.game_camera, (screen.get_width(), screen.get_height())), (0, 0))

        text = ui.FONT.render(f"{self.clock.get_fps()} P: {self.player.position}, V:{self.player.velocity} ", True,
                              ui.BUTTON_TEXT_COLOR)
        screen.blit(text, (50, 0))

        if not self.player.alive():
            self.quit_button.render(screen, (screen.get_width() / 2, screen.get_height() / 2))  # not true center

    def build_level_from_data(self):
        draw_pos = pygame.Vector2(0, -1)

        def make_monster() -> Monster:
            return Monster(self.collision_layer, target=self.player, initial_position=scaled_position)

        for s in self.EXAMPLE_LEVEL:  # TODO use param
            scaled_position = map(lambda d: d * level_geometry.GRID_SIZE, (draw_pos.x, draw_pos.y))

            if s == "\n":
                draw_pos = pygame.Vector2(0, draw_pos.y + 1)
                continue

            if s == "#":
                self.collision_layer.add(level_geometry.CollisionBox(scaled_position))

            if s == "S":
                self.collision_layer.add(level_geometry.Spikes(scaled_position))

            if s == "F":
                self.collision_layer.add(level_geometry.FinishFlag(scaled_position))

            if s == "M":
                self.sprites.add(make_monster())

            if s == "P":
                self.player.position.x, self.player.position.y = scaled_position

            draw_pos.x += 1

        self.sprites.add(self.player)
        self.sprites.add(self.collision_layer)
