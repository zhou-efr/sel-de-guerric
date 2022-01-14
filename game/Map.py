from enum import Enum

from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget

from game import TILE_SIZE
from game.Player import Player


class TileType(Enum):
    EMPTY = 0
    BLOCK = 1
    ONE_WAY = 2
    COUNT = 3


OBSTACLES = [TileType.BLOCK]
GROUNDS = [TileType.BLOCK, TileType.ONE_WAY]
EMPTY = [TileType.EMPTY]
ONE_WAYS = [TileType.ONE_WAY]

SPRITES = ['', './file/image/Sprites/BLOCK/001.png', '']


class Map(Widget):
    _position = [0, 0]
    player = ObjectProperty(None)

    # Size in block
    height: int
    width: int

    def __init__(self, filename=None, **kwargs):
        super().__init__(**kwargs)
        self.file = filename
        self.loaded = False
        try:
            with open(filename, 'r') as m:
                self.raw = m.read()
        except (FileNotFoundError, FileExistsError) as error:
            print(error)
            return

        try:
            self.save = eval(self.raw)
        except (SyntaxError, NameError) as error:
            print(error)
            return

        temp = self.save['map'].split('\n')
        self._tiles = []
        self._tilesSprite = []
        for i in range(len(temp[0])):
            self._tiles.append([])
            self._tilesSprite.append([])
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if temp[i][j] in self.save['translation'].keys():
                    self._tiles[j].append(self.save['translation'][temp[i][j]])
                    self._tilesSprite[j].append(SPRITES[self.save['translation'][temp[i][j]].value])
                else:
                    self._tiles[j].append(TileType.EMPTY)
                    self._tilesSprite[j].append(SPRITES[TileType.EMPTY.value])

        with self.canvas:
            for i in range(len(self._tilesSprite)):
                for j in range(len(self._tilesSprite[i])):
                    Rectangle(size=[TILE_SIZE, TILE_SIZE],
                              pos=[i*TILE_SIZE+self._position[0], j*TILE_SIZE+self._position[1]],
                              source=self._tilesSprite[i][j])

        self.loaded = True

    # TODO: move in (given an entry index)
    def move_in(self, entry_id):
        self.player = Player(position=self.get_tile_position_at_index(self.save['entry'][entry_id]))
        self.add_widget(self.player)

    def get_tile_index_at_point(self, point):
        """
        return the index of the tile at the given position
        :param point: position
        :return: tile index
        """
        x = int((point[0] - self._position[0] + TILE_SIZE)/TILE_SIZE)
        y = int((point[1] - self._position[1] + TILE_SIZE) / TILE_SIZE)
        return x, y

    def get_tile_index_at_x(self, x):
        """
        return the index of the tile at the given position
        :param x: x value
        :return: tile x index
        """
        return int((x - self._position[0] + TILE_SIZE)/TILE_SIZE)

    def get_tile_index_at_y(self, y):
        """
        return the index of the tile at the given position
        :param y: y value
        :return: tile y index
        """
        return int((y - self._position[1] + TILE_SIZE)/TILE_SIZE)

    def get_tile_position_at_index(self, tile_index):
        x = tile_index[0]*TILE_SIZE + self._position[0]
        y = tile_index[1] * TILE_SIZE + self._position[1]
        return x, y

    def get_tile(self, x: int, y: int):
        if self.height < x or 0 > x or self.width < y or 0 > y:
            return TileType.BLOCK

        return self._tiles[x][y]

    def is_obstacle(self, x: int, y: int):
        return self.get_tile(x, y) in OBSTACLES

    def is_ground(self, x: int, y: int):
        return self.get_tile(x, y) in GROUNDS

    def is_empty(self, x: int, y: int):
        return self.get_tile(x, y) in EMPTY

    def is_one_way(self, x: int, y: int):
        return self.get_tile(x, y) in ONE_WAYS

    def update(self):
        if self.player is not None:
            self.player.update()
