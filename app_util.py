import logging
import logging.config
import math

import cv2
import numpy as np
from numpy.typing import NDArray

from anatomy.hand import Hand
from color import Color
from constants import FONT_THICKNESS, FONT_SCALE, FONT, IMAGE_HEIGHT, FONT_COLOR, BACKGROUND, LEFT_COLOR, RIGHT_COLOR, \
    LINE_THICKNESS
from draw import add_txt_at, add_circle
from state import StateManager


def setup_logging() -> None:
    logging.config.fileConfig('logging.conf')


def add_stats(left_hand: Hand, right_hand: Hand, image: NDArray[np.uint8], state_manager: StateManager | None = None) \
        -> None:
    stats = '' if state_manager is None else (f'[{state_manager.visual_state.name}, '
                                              f'{state_manager.geometric_state.name}]: ')
    if left_hand.active:
        stats += f'Left: {left_hand.index.tip}'
    if right_hand.active:
        stats += f'{' | ' if left_hand.active else ''}Right: {right_hand.index.tip}'
    add_txt_at(image, stats, (10, IMAGE_HEIGHT - 10))


def add_hand_centers(left_hand: Hand, right_hand: Hand, image: NDArray[np.uint8]) -> None:
    if left_hand.active:
        l_pos = left_hand.get_center()
        add_circle(image, (int(l_pos[0]), int(l_pos[1])), 5, color=LEFT_COLOR)
    if right_hand.active:
        r_pos = right_hand.get_center()
        add_circle(image, (int(r_pos[0]), int(r_pos[1])), 5, color=RIGHT_COLOR)


def get_colored_image(shape: tuple[int, int], color: Color = BACKGROUND) -> NDArray[np.uint8]:
    return np.full(shape + (3,), color.rgb, dtype=np.uint8)


def update_hands(hands: list, left_hand: Hand, right_hand: Hand) -> None:
    if len(hands) == 2:
        if hands[0]['type'] == 'Right':
            left_hand.update(hands[0])
            right_hand.update(hands[1])
        else:
            right_hand.update(hands[0])
            left_hand.update(hands[1])
    elif len(hands) == 1:
        if hands[0]['type'] == 'Right':
            left_hand.update(hands[0])
            right_hand.update(None)
        else:
            right_hand.update(hands[0])
            left_hand.update(None)
    else:
        left_hand.update(None)
        right_hand.update(None)
