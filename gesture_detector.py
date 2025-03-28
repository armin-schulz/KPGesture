import math

from anatomy.finger import Finger
from anatomy.hand import Hand
from constants import DEG_IN_RAD
from util import calc_angles


class GestureDetector:
    __slots__ = ('__left_hand', '__right_hand', '__lower_straight', '__upper_straight')
    __left_hand: Hand
    __right_hand: Hand
    __lower_straight: float
    __upper_straight: float

    def __init__(self, left_hand: Hand, right_hand: Hand, straight_tolerance: int = 10):
        self.__left_hand = left_hand
        self.__right_hand = right_hand
        self.__lower_straight = - straight_tolerance * DEG_IN_RAD
        self.__upper_straight = straight_tolerance * DEG_IN_RAD

    def is_straight(self, finger: Finger) -> bool:
        return all(self.__lower_straight <= a <= self.__upper_straight for a in calc_angles(finger.pos))

    def get_active_fingers(self) -> set[Finger]:
        active_fingers = set()
        if self.__left_hand.active:
            active_fingers.update(self.__left_hand.get_fingers())
        if self.__right_hand.active:
            active_fingers.update(self.__right_hand.get_fingers())
        return active_fingers
