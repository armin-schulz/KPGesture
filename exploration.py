from constants import IMAGE_WIDTH,SKIP, IMAGE_SHAPE, WINDOW_NAME
from gesture_detector import GestureDetector
from draw import add_straight_fingers, add_moving_tips
from state import Visual, Geometric

import cv2
import numpy as np
from numpy.typing import NDArray

from color import Color
from constants import IMAGE_HEIGHT,BACKGROUND, LEFT_COLOR, RIGHT_COLOR
from draw import add_txt_at, add_circle
from state import StateManager
from cvzone.HandTrackingModule import HandDetector

from chirality import Chirality
from anatomy.hand import Hand


def exploration() -> None:
    captor = cv2.VideoCapture(0)
    captor.set(3, IMAGE_WIDTH)
    captor.set(4, IMAGE_HEIGHT)

    hand_detector = HandDetector()

    left_hand = Hand(Chirality.LEFT)
    right_hand = Hand(Chirality.RIGHT)

    state_manager: StateManager = StateManager(Visual.LIVE, Geometric.NONE,
                                               colors=[Color.VIOLET, Color.BLUE, Color.TURQUOISE, Color.GREEN,
                                                       Color.YELLOW, Color.ORANGE, Color.RED])
    gesture_detector: GestureDetector = GestureDetector(left_hand, right_hand, state_manager.color)

    while True:
        success, image = captor.read()
        image_live = cv2.flip(image, 1)
        hands_data, image_added = hand_detector.findHands(image_live.copy())
        update_hands(hands_data, left_hand, right_hand)
        gesture_detector.set_color(state_manager.color)

        match state_manager.visual_state:
            case Visual.LIVE:
                image_show = image_live
            case Visual.ADDED:
                image_show = image_added
            case Visual.SCHEMATIC:
                image_schematic = get_colored_image(IMAGE_SHAPE)
                image_show = image_schematic
            case _:
                image_show = get_colored_image(IMAGE_SHAPE)

        match state_manager.geometric_state:
            case Geometric.CENTER:
                add_hand_centers(left_hand, right_hand, image_show)
            case Geometric.STRAIGHT:
                add_straight_fingers(image_show, gesture_detector)
            case Geometric.MOVING:
                add_moving_tips(image_show, gesture_detector)
            case Geometric.ALL:
                add_hand_centers(left_hand, right_hand, image_show)
                add_straight_fingers(image_show, gesture_detector)
                add_moving_tips(image_show, gesture_detector)
            case _:
                add_stats(left_hand, right_hand, image_show, state_manager)

        cv2.imshow(WINDOW_NAME, image_show)
        cv2.waitKey(SKIP)
        state_manager.determine_next_state(left_hand.index, right_hand.index)

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