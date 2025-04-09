from collections import deque

import numpy as np
from numpy.typing import NDArray

from algebra import calc_distance


class Finger:
    __slots__ = ('__pos', '__last_tips')
    __pos: NDArray[int]
    __last_tips: deque[NDArray[int]]

    def __init__(self):
        self.__pos = np.zeros((4, 3), dtype=int)
        self.__last_tips = deque(maxlen=10)
        for i in range(10):
            self.__last_tips.append(np.zeros((3), dtype=int))

    def update(self, pos: list[tuple[int]]) -> None:
        self.__last_tips.append(pos[3])
        self.__pos[:] = np.array(pos, dtype=int)

    @property
    def v0(self) -> NDArray[int]:
        return self.__pos[0]

    @property
    def v1(self) -> NDArray[int]:
        return self.__pos[1]

    @property
    def v2(self) -> NDArray[int]:
        return self.__pos[2]

    @property
    def v3(self) -> NDArray[int]:
        return self.__pos[3]

    @property
    def tip(self) -> NDArray[int]:
        return self.__pos[3]

    @property
    def pos(self) -> NDArray[int]:
        return self.__pos

    @property
    def get_lasts(self) -> deque[int]:
        return self.__last_tips

    def get_2d_pos(self) -> NDArray[int]:
        return self.__pos[:, :2]

    def get_moved_distance(self) -> float:
        return calc_distance(self.tip, self.__last_tips[5])
