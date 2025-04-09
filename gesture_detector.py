from anatomy.finger import Finger
from anatomy.hand import Hand
from color import Color
from constants import DEG_IN_RAD
from algebra import calc_angles, calc_distance


class GestureDetector:
    __slots__ = ('__left_hand', '__right_hand', '__lower_straight', '__upper_straight', '__move_lower', '__color')
    __left_hand: Hand
    __right_hand: Hand
    __lower_straight: float
    __upper_straight: float
    __move_lower: int
    __color: Color

    def __init__(self, left_hand: Hand, right_hand: Hand, color: Color, straight_tolerance: int = 10, move_lower: int = 25):
        self.__left_hand = left_hand
        self.__right_hand = right_hand
        self.__lower_straight = - straight_tolerance * DEG_IN_RAD
        self.__upper_straight = straight_tolerance * DEG_IN_RAD
        self.__move_lower = move_lower
        self.__color = color

    def set_color(self, color: Color) -> None:
        self.__color = color

    @property
    def color(self) -> Color:
        return self.__color

    def is_straight(self, finger: Finger) -> bool:
        return all(self.__lower_straight <= a <= self.__upper_straight for a in calc_angles(finger.pos))

    def tip_moves(self, finger: Finger) -> bool:
        return finger.get_moved_distance() > self.__move_lower

    def get_active_fingers(self) -> set[Finger]:
        active_fingers = set()
        if self.__left_hand.active:
            active_fingers.update(self.__left_hand.get_fingers())
        if self.__right_hand.active:
            active_fingers.update(self.__right_hand.get_fingers())
        return active_fingers

    def snaps(self, hand: Hand) -> bool:
        return (self.tip_moves(hand.thumb) and self.tip_moves(hand.middle) and
                calc_distance(hand.thumb.tip, hand.middle.tip) < 30)


