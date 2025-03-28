import numpy as np
from numpy.typing import NDArray


class Palm:
    __slots__ = '__pos'
    __pos: NDArray[int]

    def __init__(self):
        self.__pos = np.zeros((5, 3), dtype=int)

    def update(self, pos: list) -> None:
        self.__pos[:] = np.array(pos, dtype=int)

    @property
    def v0(self) -> NDArray[int]:
        return self.__pos[0]

    @property
    def vi(self) -> NDArray[int]:
        return self.__pos[1]

    @property
    def vm(self) -> NDArray[int]:
        return self.__pos[2]

    @property
    def vr(self) -> NDArray[int]:
        return self.__pos[3]

    @property
    def vl(self) -> NDArray[int]:
        return self.__pos[3]

    def get_center(self) -> NDArray[int]:
        return np.mean(self.__pos, axis=0)




