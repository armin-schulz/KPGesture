import logging
import os
import sys
import time
import datetime
from pathlib import Path
from typing import Tuple

import cv2
import keyboard

from collections import deque

import numpy as np
from cvzone.HandTrackingModule import HandDetector
from numpy.typing import NDArray

from algebra import calc_distance_2d
from app_util import get_colors_simple, shrink_list, bend_list
from config import DRAW_LENGTH, THICKNESS, COOLDOWN_AUTO, COOLDOWN_MANUAL, JUMP_LIMIT
from constants import IMAGE_WIDTH, IMAGE_HEIGHT, INDEX_INDEX_LMS, SKIP

WHITE_TUPLE = (255, 255, 255)
BLUE_TUPLE = (255, 0, 0)
RED_TUPLE = (0, 0, 255)

MANUAL_COOLDOWN_POSITION = (IMAGE_WIDTH - 15, 15)

logger = logging.getLogger(__name__)


def draw_line(image: NDArray[np.uint8], source: tuple[int, int,], target: tuple[int, int,],
              color: tuple[int, int, int,], thickness: int) -> None:
    cv2.line(image, source, target, color, thickness)


def get_index_fingers(hands_data: dict) -> tuple[tuple[int, int,] | None, tuple[int, int,] | None,]:
    left_lms = None
    right_lms = None
    for hand_data in hands_data:
        chirality = hand_data.get('type')
        match chirality:
            case 'Right':
                left_lms = hand_data['lmList']
            case 'Left':
                right_lms = hand_data['lmList']
            case _:
                logger.error(f'chirality: {chirality}')
    return (None if left_lms is None else left_lms[INDEX_INDEX_LMS][:2],
            None if right_lms is None else right_lms[INDEX_INDEX_LMS][:2])


def add_to_positions(current: tuple[int, int,] | None, previous: tuple[int, int,] | None,
                     left_index_positions: deque[[int, int, ]]) -> tuple[tuple[int, int,], bool]:
    """
    Comparison with previous value to prevent jumping and misinterpreting left/right for right/left.
    """
    if current is not None:
        movement = 999 if previous is None else calc_distance_2d(previous, current)
        if movement < JUMP_LIMIT:
            left_index_positions.append(current)
            return current, False
    return previous, True


def draw_positions_connections(positions: deque[tuple[int, int,]], colors: list[tuple[int, int, int,]],
                               thicknesses: list[int], image: NDArray[np.uint8]) -> None:
    number_positions = len(positions)
    older = None if number_positions <= 0 else positions[0]
    for i in range(1, number_positions):
        previous = positions[i]
        draw_line(image, older, previous, colors[i], thicknesses[i])
        older = previous


def create_image_dirs(dir_id: str) -> tuple[Path, Path, Path,]:
    current_dir = Path(__file__).parent.absolute()
    image_dir = Path(current_dir).joinpath('fotos')
    personal_dir = image_dir.joinpath(dir_id)
    if os.path.exists(personal_dir):
        raise IOError(f'{current_dir} already exists.')
    manual_image_dir = personal_dir.joinpath('manual')
    auto_image_dir = personal_dir.joinpath('auto')
    for p in [image_dir, personal_dir, manual_image_dir, auto_image_dir]:
        p.mkdir(exist_ok=True)
    return personal_dir, manual_image_dir, auto_image_dir


def write_image(image_raw: NDArray[np.uint8], colors: list[tuple[int, int, int,]],
                thicknesses: list[int], left_positions: deque[tuple[int, int,]],
                right_positions: deque[tuple[int, int,]], image_path: str) -> None:
    image_write = cv2.flip(image_raw, 1)
    draw_positions_connections(left_positions, colors, thicknesses, image_write)
    draw_positions_connections(right_positions, colors, thicknesses, image_write)
    cv2.imwrite(image_path, image_write)


def get_options(args: list[str]) -> tuple[int, ...]:
    """
    Respect README.md...
    """
    line_length = DRAW_LENGTH
    thickness = THICKNESS
    jump_limit = JUMP_LIMIT
    cooldown_auto = COOLDOWN_AUTO
    cooldown_manual = COOLDOWN_MANUAL
    given_options = {p[0]: p[1] for p in map(lambda p: p if len(p) == 2 else [p[0], ''],
                                             map(lambda s: s.split('=', maxsplit=2), args))}

    values = [line_length, thickness, jump_limit, cooldown_auto, cooldown_manual]
    keys = ['DRAW_LENGTH', 'THICKNESS', 'JUMP_LIMIT', 'COOLDOWN_AUTO', 'COOLDOWN_MANUAL']

    for i, k in enumerate(keys):
        try:
            x = given_options.get(k)
            if x is None:
                raise ValueError(f'Arg {k} not set.')
            values[i] = int(x)
            logger.info(f'Set {k}={values[i]} from arg.')
        except ValueError as e:
            logger.info(f'Can not get value from key {k}. Use default {values[i]}: {e}')
    return tuple(values)


def painting(args: list[str] | None = None) -> None:
    if args is None:
        args = list()
    line_length, thickness, jump_limit, auto_cooldown, manual_cooldown = get_options(args)
    foto_dir, manual_dir, auto_dir = create_image_dirs(
        datetime.datetime.fromtimestamp(time.time()).strftime('%d_%m_%Y_%H_%M_%S'))
    logger.info(f'''Options
    line length: {line_length} entries
    thickness: {thickness} pixels
    jump limit: {jump_limit} pixels
    cooldown auto: {auto_cooldown} frames
    cooldown manual: {manual_cooldown} frames
    images path: {foto_dir}''')

    manual_counter, auto_counter = 1, 1
    captor = cv2.VideoCapture(0)
    captor.set(3, IMAGE_WIDTH)
    captor.set(4, IMAGE_HEIGHT)
    hand_detector = HandDetector()
    all_colors = get_colors_simple()
    colors = shrink_list(all_colors, line_length)
    thicknesses = bend_list(1, thickness, line_length)
    radius = THICKNESS
    left_start, right_start = (IMAGE_WIDTH // 4, IMAGE_HEIGHT // 2), ((3 * IMAGE_WIDTH) // 4, IMAGE_HEIGHT // 2)

    left_positions, right_positions = deque(maxlen=line_length), deque(maxlen=line_length)
    left_positions.append(left_start)
    right_positions.append(right_start)
    previous_left, previous_right = left_start, right_start

    while True:
        success, image_raw = captor.read()
        image = cv2.flip(image_raw, 1)
        hands_data, image_added = hand_detector.findHands(image.copy())
        current_left, current_right = get_index_fingers(hands_data)
        previous_left, missing_left = add_to_positions(current_left, previous_left, left_positions)
        previous_right, missing_right = add_to_positions(current_right, previous_right, right_positions)

        draw_positions_connections(left_positions, colors, thicknesses, image)
        draw_positions_connections(right_positions, colors, thicknesses, image)

        radius = radius - 2 if radius > 4 else THICKNESS // 2
        if missing_left:
            cv2.circle(image, previous_left, radius, WHITE_TUPLE, thickness=3)
        if missing_right:
            cv2.circle(image, previous_right, radius, WHITE_TUPLE, thickness=3)

        if manual_cooldown > 0:
            manual_cooldown -= 1
            cv2.circle(image, (55, 55), 25, RED_TUPLE, thickness=50)
        else:
            if keyboard.is_pressed('q'):
                logger.info(f'Quitting')
                exit(0)
            elif keyboard.is_pressed('f'):
                image_path_man = manual_dir.joinpath(f'{str(manual_counter)}.png')
                logger.info(f'Speichere Foto: {image_path_man}.')
                write_image(image_raw, colors, thicknesses, left_positions, right_positions, str(image_path_man))
                manual_counter += 1
                manual_cooldown = COOLDOWN_MANUAL
                auto_cooldown = COOLDOWN_AUTO
            else:
                if auto_cooldown > 0:
                    if auto_cooldown > COOLDOWN_AUTO - 25:
                        cv2.circle(image, MANUAL_COOLDOWN_POSITION, 5, BLUE_TUPLE, thickness=10)
                    auto_cooldown -= 1
                else:
                    image_path_auto = auto_dir.joinpath(f'{str(auto_counter)}.png')
                    logger.info(f'Speichere Foto: {image_path_auto}.')
                    write_image(image_raw, colors, thicknesses, left_positions, right_positions, str(image_path_auto))
                    auto_counter += 1
                    auto_cooldown = COOLDOWN_AUTO

        cv2.imshow('Painting', image)
        cv2.waitKey(SKIP)
