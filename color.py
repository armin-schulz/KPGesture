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
    ORANGE = ('orange', (255, 155, 0))
    YELLOW = ('yellow', (255, 255, 0))
    VIOLET = ('violet', (117, 57, 199))
    BROWN = ('brown', (236, 148, 12))
    GREY = ('grey', (164, 180, 178))
    TURQUOISE = ('turquoise', (0,128,128))

    def __init__(self, name: str, rgb: tuple[int, int, int]):
        self.__name = name
        self.__rgb = rgb

    @property
    def rgb(self) -> tuple[int, int, int,]:
        """
        cv uses bgr
        """
        return self.__rgb[::-1]

    @property
    def name(self) -> str:
        return self.__name

    @classmethod
    def values(cls) -> list['Color']:
        return list(cls.__members__.values())
