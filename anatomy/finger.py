import numpy as np
from numpy.typing import NDArray


class Finger:
    __slots__ = '__pos'
    __pos: NDArray[int]

    def __init__(self):
        self.__pos = np.zeros((4, 3), dtype=int)

    def update(self, pos: list[tuple[int]]) -> None:
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

    def get_2d_pos(self) -> NDArray[int]:
        return self.__pos[:, :2]
