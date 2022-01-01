from game import DELTA_TIME
from game.Rect import GameRect


class Object:
    old_position: list
    position: list

    old_speed: list
    speed: list

    scale: list

    game_rect: GameRect
    game_rect_offset: list

    old_right_wall: bool
    right_wall: bool
    old_left_wall: bool
    left_wall: bool

    old_ground: bool
    ground: bool
    old_ceiling: bool
    ceiling: bool

    def update_physic(self):
        self.old_position = self.position
        self.old_speed = self.speed

        self.old_right_wall = self.right_wall
        self.old_left_wall = self.left_wall
        self.old_ground = self.ground
        self.old_ceiling = self.ceiling

        self.position = [map(lambda x: x*DELTA_TIME, self.speed)]

        # position y less than 0 then on ground
        if self.position[1] < 0.0:
            self.position[1] = 0.0
            self.ground = True
        else:
            self.ground = False

        self.game_rect.center = [map(lambda x: self.position[x] + self.game_rect_offset[x],
                                     range(len(self.game_rect.center)))]

        # TODO: render the object
