import logging
import logging.config
import math

import cv2
import numpy as np
from numpy.typing import NDArray

from color import Color
from constants import FONT_THICKNESS, FONT_SCALE, FONT, IMAGE_HEIGHT, FONT_COLOR, BACKGROUND, LEFT_COLOR, RIGHT_COLOR, \
    LINE_THICKNESS
from anatomy.hand import Hand
from state import Visual


def setup_logging() -> None:
    logging.config.fileConfig('logging.conf')


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


def add_stats(left_hand: Hand, right_hand: Hand, image: NDArray[np.uint8], app_state: Visual | None = None) -> None:
    stats = '' if app_state is None else f'[{app_state.name}]: '
    if left_hand.active:
        stats += f'Left: {left_hand.index.tip}'
    if right_hand.active:
        stats += f'{' | ' if left_hand.active else ''}Right: {right_hand.index.tip}'

    add_txt_at(image, stats, (10, IMAGE_HEIGHT - 10))


def add_index_tips(left_hand: Hand, right_hand: Hand, image: NDArray[np.uint8]) -> None:
    #TODO div as anatomy draw
    pass


def add_hand_centers(left_hand: Hand, right_hand: Hand, image: NDArray[np.uint8]) -> None:
    # TODO div as anatomy draw
    if left_hand.active:
        l_pos = left_hand.get_center()
        add_circle(image, (int(l_pos[0]), int(l_pos[1])), 5, color=LEFT_COLOR)
    if right_hand.active:
        r_pos = right_hand.get_center()
        add_circle(image, (int(r_pos[0]), int(r_pos[1])), 5, color=RIGHT_COLOR)


def add_txt_at(image: NDArray[np.uint8], s: str, pos: tuple[int, int,], font: int = FONT, font_scale: int = FONT_SCALE,
               font_thickness: int = FONT_THICKNESS, color: Color = FONT_COLOR) -> None:
    cv2.putText(image, s, pos, font, font_scale, color.rgb, font_thickness)


def add_circle(image: NDArray[np.uint8], pos: tuple[int, int,], radius: int, thickness: int = None,
               color: Color = FONT_COLOR) -> None:
    if thickness is None:
        thickness = radius
    cv2.circle(image, pos, radius, color.rgb, thickness)


def draw_lines(image: NDArray[np.uint8], points: NDArray[int], color: Color = FONT_COLOR,
               thickness: int = LINE_THICKNESS) -> None:
    for i in range(points.shape[0] - 1):
        draw_line(image, points[i], points[i + 1], color=color, thickness=thickness)


def draw_line(image: NDArray[np.uint8], source: NDArray[int], target: NDArray[int], color: Color = FONT_COLOR,
              thickness: int = LINE_THICKNESS) -> None:
    cv2.line(image, source, target, color.rgb, thickness)


def get_colored_image(shape: tuple[int, int], color: Color = BACKGROUND) -> NDArray[np.uint8]:
    return np.full(shape + (3,), color.rgb, dtype=np.uint8)


def calc_angles(arr: NDArray[int]) -> NDArray[float]:
    """
    assuming vectors have length
    """
    number_of_angles = max(0, arr.shape[0] - 2)
    angles = np.zeros(number_of_angles, dtype=np.float32)
    for i in range(number_of_angles):
        v0 = arr[i + 1] - arr[i]
        v1 = arr[i + 2] - arr[i + 1]
        dot_product = np.dot(v0, v1)
        magnitude_product = np.linalg.norm(v0) * np.linalg.norm(v1)
        quotient_product = np.clip(dot_product / magnitude_product, -1, 1)
        angles[i] = np.arccos(quotient_product)
    return angles




