from __future__ import annotations


class GameRect:
    half_size: list
    center : list

    def __init__(self, center: list, half_size: list):
        """
        initialize a rect object
        :param center: array giving the position of the center of the rect [x, y]
        :param half_size: array giving the half size of the rect [width, height]
        """
        self.half_size = half_size
        self.center = center

    def overlaps(self, other: GameRect) -> bool:
        """
        Indicate either another game rect overlaps with this one or not
        :param other: game rect to compare with
        :return: true if overlap, false otherwise
        """
        return not (abs(self.center[0] - other.center[0]) > self.half_size[0] + other.half_size[0]) and \
               not (abs(self.center[1] - other.center[1]) > self.half_size[1] + other.half_size[1])


if __name__ == '__main__':
    test_rect_1 = GameRect([1, 1], [2, 2])
    test_rect_2 = GameRect([5, 1], [2, 2])
    print(test_rect_1.overlaps(test_rect_2))
