from enum import Enum


class Color(Enum):
    __slots__ = ('__name', '__rgb')
    __name: str
    __rgb: tuple[int, int, int,]

    BLACK = ('black', (0, 0, 0))
    WHITE = ('white', (255, 255, 255))
    RED = ('red', (255, 0, 0))
    BLUE = ('blue', (0, 0, 255))
    GREEN = ('green', (0, 255, 0))
    ORANGE = ('orange', (236, 148, 12))

    def __init__(self, name: str, rgb: tuple[int, int, int]):
        self.__name = name
        self.__rgb = rgb

    @property
    def rgb(self) -> tuple[int, int, int,]:
        """
        cv uses bgr
        """
        return self.__rgb[::-1]
        #return (self.__rgb[2], self.__rgb[1], self.__rgb[0])

    @property
    def name(self) -> str:
        return self.__name
