import cv2
import numpy as np
from numpy.typing import NDArray

from color import Color
from constants import FONT_SCALE, FONT, FONT_COLOR, FONT_THICKNESS, LINE_THICKNESS
from gesture_detector import GestureDetector


def add_straight_fingers(image: NDArray[np.uint8], detector: GestureDetector) -> None:
    for f in detector.get_active_fingers():
        if detector.is_straight(f):
            draw_lines(image, f.get_2d_pos(), color=detector.color)


def add_moving_tips(image: NDArray[np.uint8], detector: GestureDetector) -> None:
    for f in detector.get_active_fingers():
        if detector.tip_moves(f):
            add_circle(image, f.tip[:2], 3, color=detector.color)


def add_txt_at(image: NDArray[np.uint8], s: str, pos: tuple[int, int,], font: int = FONT, font_scale: int = FONT_SCALE,
               font_thickness: int = FONT_THICKNESS, color: Color = FONT_COLOR) -> None:
    cv2.putText(image, s, pos, font, font_scale, color.rgb, font_thickness)


def add_circle(image: NDArray[np.uint8], point: NDArray[int], radius: int, thickness: int = None,
               color: Color = FONT_COLOR) -> None:
    if thickness is None:
        thickness = radius
    cv2.circle(image, point, radius, color.rgb, thickness)


def draw_lines(image: NDArray[np.uint8], points: NDArray[int], color: Color = FONT_COLOR,
               thickness: int = LINE_THICKNESS) -> None:
    for i in range(points.shape[0] - 1):
        draw_line(image, points[i], points[i + 1], color=color, thickness=thickness)


def draw_line(image: NDArray[np.uint8], source: NDArray[int], target: NDArray[int], color: Color = FONT_COLOR,
              color_rgb: tuple[np.uint8, np.uint8, np.uint8,] = None, thickness: int = LINE_THICKNESS) -> None:
    color_value = color.rgb if color_rgb is None else color_rgb
    cv2.line(image, source, target, color_value, thickness)


def draw_line_alpha(image: NDArray[np.uint8], source: tuple[int, int], target: tuple[int, int], alpha: float,
                    color: Color = FONT_COLOR, color_rgb: tuple[int, int, int] = None,
                    thickness: int = LINE_THICKNESS) -> None:
    # Get the final color
    color_value = color.rgb if color_rgb is None else color_rgb
    color_value = tuple(int(c) for c in color_value)  # Ensure it's int tuple

    # Create an overlay
    overlay = image.copy()

    # Draw on the overlay
    cv2.line(overlay, source, target, color_value, thickness)

    # Blend overlay with original image
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

def emposeFrame(f: NDArray[bool], image: NDArray[np.uint8], pos: NDArray[int] = np.zeros(2, dtype=int),
           color: Color = FONT_COLOR) -> None:
    total_width, total_height = image.shape[:2]
    for r in range(f.shape[0]):
        for c in range(f.shape[1]):
            if f[r, c]:
                image[(pos[0] + r) % total_width][(pos[1] + c) % total_height] = color.rgb


def normalize_3d(p: NDArray[int]) -> NDArray[int]:
    return np.array([np.clip(p[0], 0, 1279), np.clip(p[1], 0, 719)], dtype=int)
