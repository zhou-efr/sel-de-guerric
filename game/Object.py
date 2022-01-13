from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.widget import Widget

from game import DELTA_TIME
from game.Rect import GameRect


class Object(Widget):
    old_position: list
    position = ListProperty([50, 50])

    old_speed: list
    speed: list

    scale: list

    game_rect: GameRect
    game_rect_offset: list

    old_right_wall = False
    right_wall = False
    old_left_wall = False
    left_wall = False

    old_ground = False
    ground = False
    old_ceiling = False
    ceiling = False

    def __init__(self, **kwargs):
        super(Object, self).__init__(**kwargs)

    def update_physic(self):
        self.old_position = self.position
        self.old_speed = self.speed

        self.old_right_wall = self.right_wall
        self.old_left_wall = self.left_wall
        self.old_ground = self.ground
        self.old_ceiling = self.ceiling

        self.position = list(map(lambda x, y: x+y, self.position, list(map(lambda x: x*DELTA_TIME, self.speed))))

        # position y less than 0 then on ground
        if self.position[1] <= 5.0:
            self.position[1] = 5.0
            self.ground = True
            # print('on ground')
        else:
            self.ground = False

        self.game_rect.center = list(map(lambda x: self.position[x] + self.game_rect_offset[x],
                                     range(len(self.game_rect.center))))

        # TODO: render the object
