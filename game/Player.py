from copy import deepcopy
from enum import Enum

from kivy.lang import Builder

from game import GRAVITY, DELTA_TIME, MAX_FALLING_SPEED, MIN_JUMP_SPEED, PLAYER_HALF_SIZE, WALK_SPEED, JUMP_SPEED
from game.Object import Object
from game.Rect import GameRect

Builder.load_file('./game/Player.kv')


class KeyInput(Enum):
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    JUMP = 3
    COUNT = 4


class PlayerState(Enum):
    STAND = 1
    WALK = 2
    JUMP = 3
    GRAB_EDGE = 4


class Player(Object):
    inputs: list
    old_inputs: list

    old_state = PlayerState.STAND
    current_state = PlayerState.STAND

    jump_speed: float  # 410 px/s
    walk_speed: float

    def released(self, key: KeyInput):
        return not (self.inputs[key.value] and self.old_inputs[key.value])

    def pressed(self, key: KeyInput):
        return self.inputs[key.value] and self.old_inputs[key.value]

    def key_state(self, key: KeyInput):
        return self.inputs[key.value]

    def update_inputs(self):
        self.old_inputs = deepcopy(self.inputs)

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)

    def update(self):
        if self.current_state == PlayerState.STAND:
            self.speed = [0.0, 0.0]
            # TODO: animation

            # if the player isn't on ground then the player is jumping (actually falling, but it's the same)
            if not self.ground:
                self.current_state = PlayerState.JUMP
            else:
                # since the player go either to right or left, he walks (if both inputs are pressed then he doesn't
                # move)
                if self.key_state(KeyInput.LEFT) != self.key_state(KeyInput.RIGHT):
                    self.current_state = PlayerState.WALK
                # jumping
                elif self.key_state(KeyInput.JUMP):
                    self.speed[1] = self.jump_speed
                    self.current_state = PlayerState.JUMP
        elif self.current_state == PlayerState.WALK:
            # TODO: animation
            if self.key_state(KeyInput.LEFT) == self.key_state(KeyInput.RIGHT):
                self.speed = [0.0, 0.0]
                self.current_state = PlayerState.STAND
            else:
                if self.key_state(KeyInput.LEFT):
                    self.speed[0] = 0.0 if self.left_wall else -self.walk_speed
                    self.scale[0] = -abs(self.scale[0])
                elif self.key_state(KeyInput.RIGHT):
                    self.speed[0] = 0.0 if self.right_wall else self.walk_speed
                    self.scale[0] = abs(self.scale[0])

                if self.key_state(KeyInput.JUMP) and self.ground:
                    self.speed[1] = self.jump_speed
                    # sound effect for jump
                    self.current_state = PlayerState.JUMP
        elif self.current_state == PlayerState.JUMP:
            # TODO: animation

            self.speed[1] += GRAVITY * DELTA_TIME
            self.speed[1] = max(self.speed[1], MAX_FALLING_SPEED)

            if not(self.key_state(KeyInput.JUMP)) and self.speed[1] > 0.0:
                self.speed[1] = min(self.speed[1], MIN_JUMP_SPEED)
            elif self.key_state(KeyInput.LEFT) == self.key_state(KeyInput.RIGHT):
                self.speed[0] = 0.0
            elif self.key_state(KeyInput.LEFT):
                self.speed[0] = 0.0 if self.left_wall else -self.walk_speed
                self.scale[0] = -abs(self.scale[0])
            elif self.key_state(KeyInput.RIGHT):
                self.speed[0] = 0.0 if self.right_wall else self.walk_speed
                self.scale[0] = abs(self.scale[0])

            if self.ground:
                if self.key_state(KeyInput.LEFT) == self.key_state(KeyInput.RIGHT):
                    self.current_state = PlayerState.STAND
                    self.speed = [0, 0]
                    # sfx
                else:
                    self.current_state = PlayerState.WALK
                    self.speed[1] = 0
                    # sfx
        elif self.current_state == PlayerState.GRAB_EDGE:
            pass

        self.update_physic()

        if ((self.ground and not self.old_ground) or (self.ceiling and not self.old_ceiling) or
                (self.left_wall and not self.old_left_wall) or (self.right_wall and not self.old_right_wall)):
            # sound effect for landing
            pass

        self.update_inputs()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.old_inputs = [False, False, False, False, False]

        self.inputs = [False, False, False, False, False]
        self.position = [0, 0]

        self.walk_speed = WALK_SPEED
        self.jump_speed = JUMP_SPEED

        self.game_rect = GameRect(self.position, deepcopy(PLAYER_HALF_SIZE))
        self.game_rect_offset = [0, self.game_rect.half_size[1]]

        self.scale = [1, 1]
