from numpy.typing import NDArray

from chirality import Chirality
from anatomy.finger import Finger
from anatomy.palm import Palm
from anatomy.thumb import Thumb


class Hand:
    __slots__ = ('__active', '__chirality', '__palm', '__thumb', '__index', '__middle', '__ring', '__little')
    __active: bool
    __chirality: Chirality
    __palm: Palm
    __thumb: Thumb
    __index: Finger
    __middle: Finger
    __ring: Finger
    __little: Finger

    def __init__(self, chirality: Chirality):
        self.__active = False
        self.__chirality = chirality
        self.__palm = Palm()
        self.__thumb = Thumb()
        self.__index = Finger()
        self.__middle = Finger()
        self.__ring = Finger()
        self.__little = Finger()

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def index(self) -> Finger:
        return self.__index

    @property
    def middle(self) -> Finger:
        return self.__middle

    @property
    def ring(self) -> Finger:
        return self.__ring

    @property
    def little(self) -> Finger:
        return self.__little

    def get_fingers(self) -> set[Finger]:
        return {self.__thumb, self.__index, self.__middle, self.__ring, self.__little}

    def get_center(self) -> NDArray[int]:
        return self.__palm.get_center()

    def update(self, hand_data: dict | None) -> None:
        if hand_data is None:
            self.__active = False
            return
        self.__thumb.update(hand_data['lmList'][1:5])
        self.__index.update(hand_data['lmList'][5:9])
        self.__middle.update(hand_data['lmList'][9:13])
        self.__ring.update(hand_data['lmList'][13:17])
        self.__little.update(hand_data['lmList'][17:21])
        self.__palm.update([hand_data['lmList'][0], hand_data['lmList'][5], hand_data['lmList'][9],
                            hand_data['lmList'][13], hand_data['lmList'][17]])
        self.__active = True


