from enum import Enum

from datetime import datetime, timedelta
from constants import IMAGE_WIDTH, STATE_COOLDOWN
from anatomy.finger import Finger


class Visual(Enum):
    __name: str

    LIVE = 'live'
    ADDED = 'added'
    SCHEMATIC = 'schematic'

    def __init__(self, name: str):
        self.__name = name


class StateManager:
    __slots__ = ('__current', '__free_at')
    __current: Visual
    __free_at: datetime

    def __init__(self, state: Visual):
        self.__current = state
        self.__free_at = datetime.now()

    @property
    def state(self) -> Visual:
        return self.__current

    def determine_next_state(self, left: Finger, right: Finger) -> None:
        setable: bool = datetime.now() >= self.__free_at
        if not setable:
            return
        if left.tip[0] < 100 and right.tip[0] > (IMAGE_WIDTH - 100):
            match self.__current:
                case Visual.LIVE:
                    self.__current = Visual.ADDED
                case Visual.ADDED:
                    self.__current = Visual.SCHEMATIC
                case Visual.SCHEMATIC:
                    self.__current = Visual.LIVE
                case _:
                    pass
            self.__free_at = datetime.now() + timedelta(seconds=STATE_COOLDOWN)
