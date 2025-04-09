import cv2

from color import Color
from constants import IMAGE_WIDTH, IMAGE_HEIGHT, SKIP, IMAGE_SHAPE, WINDOW_NAME
from gesture_detector import GestureDetector
from draw import add_straight_fingers, add_moving_tips, emposeFrame, draw_line, normalize_3d
from state import Visual, StateManager, Geometric
from app_util import add_stats, get_colored_image, add_hand_centers, update_hands

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
