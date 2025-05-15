import datetime
import logging
import time

import cv2
import keyboard
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from numpy.typing import NDArray

from app_util import get_colors_simple
from chirality import Chirality
from painting import create_image_dirs, get_options, get_index_fingers, meh, WHITE_TUPLE, draw_line, RED_TUPLE, \
    MANUAL_COOLDOWN_POSITION, BLUE_TUPLE

from config import THICKNESS, COOLDOWN_AUTO, COOLDOWN_MANUAL
from constants import IMAGE_WIDTH, IMAGE_HEIGHT, SKIP

logger = logging.getLogger(__name__)


def draw_positions_connections(positions: list[tuple[int, int,]], colors: list[tuple[int, int, int,]],
                               thickness: int, image: NDArray[np.uint8]) -> None:
    number_positions = len(positions)
    older = None if number_positions <= 0 else positions[0]
    for i in range(1, number_positions):
        previous = positions[i]
        draw_line(image, older, previous, colors[i % 755], thickness)
        older = previous


def write_image(image_raw: NDArray[np.uint8], colors: list[tuple[int, int, int,]],
                thickness: int, left_positions: list[tuple[int, int,]] | None,
                right_positions: list[tuple[int, int,]] | None, image_path: str) -> None:
    image_write = cv2.flip(image_raw, 1)
    if left_positions is not None:
        draw_positions_connections(left_positions, colors, thickness, image_write)
    if right_positions is not None:
        draw_positions_connections(right_positions, colors, thickness, image_write)
    cv2.imwrite(image_path, image_write)


def painting_static(args: list[str] | None = None) -> None:
    line_length, thickness, jump_limit, auto_cooldown, manual_cooldown, side_value = get_options(args)
    side = Chirality(side_value)
    foto_dir, manual_dir, auto_dir = create_image_dirs(
        datetime.datetime.fromtimestamp(time.time()).strftime('%d_%m_%Y_%H_%M_%S'), current_dir="C:\\")
    logger.info(f'''Options
       line length: {line_length} entries
       thickness: {thickness} pixels
       jump limit: {str(jump_limit) + ' pixels' if jump_limit != -1 else 'infinite'}
       side: {side.name}
       cooldown auto: {auto_cooldown} frames
       cooldown manual: {manual_cooldown} frames
       images path: {foto_dir}''')

    manual_counter, auto_counter = 1, 1
    captor = cv2.VideoCapture(0)
    captor.set(3, IMAGE_WIDTH)
    captor.set(4, IMAGE_HEIGHT)
    hand_detector = HandDetector()
    colors = get_colors_simple()
    radius = THICKNESS
    thickness = THICKNESS
    jump_limit_left, jump_limit_right = jump_limit, jump_limit
    left_start, right_start = (IMAGE_WIDTH // 4, IMAGE_HEIGHT // 2), ((3 * IMAGE_WIDTH) // 4, IMAGE_HEIGHT // 2)

    left_positions, right_positions = [left_start], [right_start]
    previous_left, previous_right = left_start, right_start
    if side == Chirality.LEFT:
        right_positions = None
        previous_right = None
        jump_limit_left = -1
    elif side == Chirality.RIGHT:
        left_positions = None
        previous_left = None
        jump_limit_right = -1

    while True:
        success, image_raw = captor.read()
        image = cv2.flip(image_raw, 1)
        radius = radius - 2 if radius > 4 else THICKNESS // 2
        hands_data, image_added = hand_detector.findHands(image.copy())
        current_left, current_right = get_index_fingers(hands_data)
        missing_left, missing_right = False, False
        if side == Chirality.BOTH or side == Chirality.LEFT:
            previous_left, missing_left = meh(previous_left, current_left, left_positions, jump_limit_left)
            draw_positions_connections(left_positions, colors, thickness, image)
            cv2.circle(image, previous_left, radius, WHITE_TUPLE, thickness=3)

        if side == Chirality.BOTH or side == Chirality.RIGHT:
            previous_right, missing_right = meh(previous_right, current_right, right_positions, jump_limit_right)

        if side == Chirality.BOTH:
            draw_positions_connections(left_positions, colors, thickness, image)
            draw_positions_connections(right_positions, colors, thickness, image)
            if missing_left:
                cv2.circle(image, previous_left, radius, WHITE_TUPLE, thickness=3)
            if missing_right:
                cv2.circle(image, previous_right, radius, WHITE_TUPLE, thickness=3)
        elif side == Chirality.LEFT:
            draw_positions_connections(left_positions, colors, thickness, image)
            if missing_left:
                cv2.circle(image, previous_left, radius, WHITE_TUPLE, thickness=3)
        elif side == Chirality.RIGHT:
            draw_positions_connections(right_positions, colors, thickness, image)
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
                write_image(image_raw, colors, thickness, left_positions, right_positions, str(image_path_man))
                manual_counter += 1
                manual_cooldown = COOLDOWN_MANUAL
                auto_cooldown = COOLDOWN_AUTO
            elif keyboard.is_pressed('r'):
                left_positions, right_positions = list(), list()
            else:
                if auto_cooldown > 0:
                    if auto_cooldown > COOLDOWN_AUTO - 25:
                        cv2.circle(image, MANUAL_COOLDOWN_POSITION, 5, BLUE_TUPLE, thickness=10)
                    auto_cooldown -= 1
                else:
                    image_path_auto = auto_dir.joinpath(f'{str(auto_counter)}.png')
                    logger.info(f'Speichere Foto: {image_path_auto}.')
                    write_image(image_raw, colors, thickness, left_positions, right_positions, str(image_path_auto))
                    auto_counter += 1
                    auto_cooldown = COOLDOWN_AUTO

        cv2.imshow('Painting', image)
        cv2.waitKey(SKIP)

