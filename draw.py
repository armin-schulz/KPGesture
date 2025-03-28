import math

import numpy as np
from numpy.typing import NDArray

from anatomy.hand import Hand
from color import Color
from gesture_detector import GestureDetector
from util import draw_lines, calc_angles


def add_straight_fingers(image: NDArray[np.uint8], detector: GestureDetector) -> None:
    for f in detector.get_active_fingers():
        if detector.is_straight(f):
            draw_lines(image, f.get_2d_pos(), color=Color.GREEN)
