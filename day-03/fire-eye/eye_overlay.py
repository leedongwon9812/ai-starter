"""Overlay a.png on both eyes detected from a webcam with MediaPipe."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import mediapipe as mp
import cv2
import numpy as np


# Face Mesh landmark pairs: outer/inner eye corners and upper/lower eyelids.
EYES = ((33, 133, 159, 145), (362, 263, 386, 374))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Overlay an image on webcam eye regions")
    parser.add_argument("--image", default="a.png", help="overlay PNG path (default: a.png)")
    parser.add_argument("--camera", type=int, default=0, help="camera index (default: 0)")
    parser.add_argument("--scale", type=float, default=1.55, help="overlay size multiplier")
    parser.add_argument("--opacity", type=float, default=1.0, help="opacity from 0.0 to 1.0")
    parser.add_argument("--no-mirror", action="store_true", help="do not mirror webcam view")
    return parser.parse_args()


def load_overlay(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"Cannot read overlay image: {path.resolve()}")

    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
    elif image.shape[2] == 3:
        # When a.png has no alpha channel, add a feathered elliptical mask.
        h, w = image.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(mask, (w // 2, h // 2), (max(1, w // 2 - 1), max(1, h // 2 - 1)), 0, 0, 360, 255, -1)
        blur = max(3, (min(h, w) // 12) | 1)
        mask = cv2.GaussianBlur(mask, (blur, blur), 0)
        image = np.dstack((image, mask))
    return image


def rotate_bgra(image: np.ndarray, angle: float) -> np.ndarray:
    h, w = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    cos, sin = abs(matrix[0, 0]), abs(matrix[0, 1])
    new_w, new_h = int(h * sin + w * cos), int(h * cos + w * sin)
    matrix[0, 2] += new_w / 2 - w / 2
    matrix[1, 2] += new_h / 2 - h / 2
    return cv2.warpAffine(image, matrix, (new_w, new_h), flags=cv2.INTER_AREA,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def alpha_blend(frame: np.ndarray, overlay: np.ndarray, center: tuple[int, int], opacity: float) -> None:
    h, w = overlay.shape[:2]
    x1, y1 = center[0] - w // 2, center[1] - h // 2
    x2, y2 = x1 + w, y1 + h
    fx1, fy1 = max(0, x1), max(0, y1)
    fx2, fy2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
    if fx1 >= fx2 or fy1 >= fy2:
        return

    ox1, oy1 = fx1 - x1, fy1 - y1
    ox2, oy2 = ox1 + (fx2 - fx1), oy1 + (fy2 - fy1)
    crop = overlay[oy1:oy2, ox1:ox2]
    alpha = crop[:, :, 3:4].astype(np.float32) / 255.0 * opacity
    target = frame[fy1:fy2, fx1:fx2]
    target[:] = (crop[:, :, :3] * alpha + target * (1.0 - alpha)).astype(np.uint8)


def draw_eye_overlay(frame: np.ndarray, landmarks, source: np.ndarray, scale: float, opacity: float) -> None:
    height, width = frame.shape[:2]
    points = [(int(p.x * width), int(p.y * height)) for p in landmarks.landmark]
    for outer_i, inner_i, upper_i, lower_i in EYES:
        outer, inner = np.array(points[outer_i]), np.array(points[inner_i])
        upper, lower = np.array(points[upper_i]), np.array(points[lower_i])
        eye_width = max(8, int(np.linalg.norm(inner - outer) * scale))
        eye_height = max(6, int(max(np.linalg.norm(lower - upper) * 2.2, eye_width * 0.45)))
        angle = float(np.degrees(np.arctan2(inner[1] - outer[1], inner[0] - outer[0])))
        resized = cv2.resize(source, (eye_width, eye_height), interpolation=cv2.INTER_AREA)
        rotated = rotate_bgra(resized, angle)
        center = tuple(((outer + inner) / 2).astype(int))
        alpha_blend(frame, rotated, center, opacity)


def main() -> int:
    args = parse_args()
    if args.scale <= 0 or not 0.0 <= args.opacity <= 1.0:
        print("Error: --scale must be positive and --opacity must be between 0 and 1.", file=sys.stderr)
        return 2

    try:
        overlay = load_overlay(Path(args.image))
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    camera = cv2.VideoCapture(args.camera)
    if not camera.isOpened():
        print(f"Error: cannot open camera index {args.camera}.", file=sys.stderr)
        return 1

    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    print("Running. Press Q or ESC to quit.")
    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                print("Error: failed to read a webcam frame.", file=sys.stderr)
                break
            if not args.no_mirror:
                frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(rgb)
            if result.multi_face_landmarks:
                draw_eye_overlay(frame, result.multi_face_landmarks[0], overlay, args.scale, args.opacity)

            cv2.imshow("MediaPipe Eye Overlay", frame)
            if cv2.waitKey(1) & 0xFF in (27, ord("q"), ord("Q")):
                break
    except KeyboardInterrupt:
        pass
    finally:
        face_mesh.close()
        camera.release()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
