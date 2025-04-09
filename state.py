from enum import Enum

from datetime import datetime, timedelta

from color import Color
from constants import IMAGE_WIDTH, STATE_COOLDOWN
from anatomy.finger import Finger


class Visual(Enum):
    __name: str

    LIVE = 'live'
    ADDED = 'added'
    SCHEMATIC = 'schematic'

    def __init__(self, name: str):
        self.__name = name


class Geometric(Enum):
    __name: str

    NONE = 'none'
    CENTER = 'center'
    STRAIGHT = 'straight'
    MOVING = 'moving'
    ALL = 'all'

    def __init__(self, name: str):
        self.__name = name


class StateManager:
    __slots__ = ('__current_visual', '__current_geometric', '__geometric_bounds', '__color', '__color_bounds',
                 '__free_at')
    __current_visual: Visual
    __current_geometric: Geometric
    __geometric_bounds: list[tuple[Geometric, int, int,]]
    __color: Color
    __color_bounds: list[tuple[Color, int, int,]]
    __free_at: datetime

    def __init__(self, visual: Visual, geometric: Geometric, colors: list[Color] = None, win_width: int = IMAGE_WIDTH):
        if colors is None:
            colors = list(Color.values())
        self.__color = colors[0]
        self.__current_visual = visual
        self.__current_geometric = geometric
        self.__free_at = datetime.now()
        min_y, max_y = int(0.1 * win_width), win_width - int(0.1 * win_width)
        geo_widths = int((max_y - min_y) / len(Geometric))
        color_widths = int((max_y - min_y) / len(colors))
        self.__geometric_bounds = list()
        self.__color_bounds = list()
        for i, g in enumerate(Geometric):
            self.__geometric_bounds.append((g, min_y + i * geo_widths, min_y + (i + 1) * geo_widths))
        for i, c in enumerate(colors):
            self.__color_bounds.append((c, min_y + i * color_widths, min_y + (i + 1) * color_widths))

    @property
    def visual_state(self) -> Visual:
        return self.__current_visual

    @property
    def geometric_state(self) -> Geometric:
        return self.__current_geometric

    @property
    def color(self) -> Color:
        return self.__color

    def determine_next_state(self, left: Finger, right: Finger) -> None:
        setable: bool = datetime.now() >= self.__free_at
        if not setable:
            return
        if left.tip[0] < 100 and right.tip[0] > (IMAGE_WIDTH - 100):
            match self.__current_visual:
                case Visual.LIVE:
                    self.__current_visual = Visual.ADDED
                case Visual.ADDED:
                    self.__current_visual = Visual.SCHEMATIC
                case Visual.SCHEMATIC:
                    self.__current_visual = Visual.LIVE
                case _:
                    pass
            self.__free_at = datetime.now() + timedelta(seconds=STATE_COOLDOWN)

        if left.tip[1] < 10:
            self.__set_geometric(left.tip[0])

        if right.tip[1] < 10:
            self.__set_color(right.tip[0])

    def __set_geometric(self, p: int) -> None:
        for g, l, r in self.__geometric_bounds:
            if l < p < r:
                self.__current_geometric = g
                return

    def __set_color(self, p: int) -> None:
        for c, l, r in self.__color_bounds:
            if l < p < r:
                self.__color = c
                return
