import logging

import cv2

from constants import IMAGE_WIDTH, IMAGE_HEIGHT, SKIP, IMAGE_SHAPE, WINDOW_NAME
from gesture_detector import GestureDetector
from draw import add_straight_fingers
from state import Visual, StateManager
from util import setup_logging, update_hands, add_stats, get_colored_image, add_hand_centers, draw_lines

from cvzone.HandTrackingModule import HandDetector

from chirality import Chirality
from anatomy.hand import Hand

logger = logging.getLogger(__name__)
setup_logging()

captor = cv2.VideoCapture(0)
captor.set(3, IMAGE_WIDTH)
captor.set(4, IMAGE_HEIGHT)

hand_detector = HandDetector()

left_hand = Hand(Chirality.LEFT)
right_hand = Hand(Chirality.RIGHT)

state_manager: StateManager = StateManager(Visual.SCHEMATIC)
gesture_detector: GestureDetector = GestureDetector(left_hand, right_hand, straight_tolerance=10)

while True:
    success, image = captor.read()
    image_live = cv2.flip(image, 1)
    hands_data, image_added = hand_detector.findHands(image_live.copy())
    update_hands(hands_data, left_hand, right_hand)

    match state_manager.state:
        case Visual.LIVE:
            image_show = image_live
        case Visual.ADDED:
            image_show = image_added
        case Visual.SCHEMATIC:
            image_schematic = get_colored_image(IMAGE_SHAPE)
            add_hand_centers(left_hand, right_hand, image_schematic)
            image_show = image_schematic
        case _:
            image_show = get_colored_image(IMAGE_SHAPE)

    add_straight_fingers(image_show, gesture_detector)
    add_stats(left_hand, right_hand, image_show, app_state=state_manager.state)
    cv2.imshow(WINDOW_NAME, image_show)
    cv2.waitKey(SKIP)

    state_manager.determine_next_state(left_hand.index, right_hand.index)




