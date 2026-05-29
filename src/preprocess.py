"""
preprocess.py — Image Preprocessing Module
Handles all image loading, resizing, normalization, and augmentation.
"""

import cv2
import numpy as np
from pathlib import Path


# ─── Constants ───────────────────────────────────────────────────────────────
TARGET_SIZE = (128, 128)   # Resize target for all images
CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_GRID = (8, 8)


def load_image(image_path: str) -> np.ndarray:
    """Load an image from disk. Returns BGR numpy array or None on failure."""
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")
    return img


def resize_image(image: np.ndarray, size: tuple = TARGET_SIZE) -> np.ndarray:
    """Resize image to given size (width, height)."""
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert BGR image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def convert_to_hsv(image: np.ndarray) -> np.ndarray:
    """Convert BGR image to HSV color space."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def apply_clahe(gray_image: np.ndarray) -> np.ndarray:
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    to a grayscale image to improve local contrast.
    """
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_TILE_GRID)
    return clahe.apply(gray_image)


def denoise_image(image: np.ndarray) -> np.ndarray:
    """Apply Non-Local Means Denoising to reduce noise."""
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Normalize pixel values to range [0, 1]."""
    return image.astype(np.float32) / 255.0


def preprocess_image(image_path: str, augment: bool = False) -> dict:
    """
    Full preprocessing pipeline for a single image.
    
    Args:
        image_path: Path to the image file.
        augment   : If True, also returns augmented variants.

    Returns:
        dict with keys:
            'original'  – resized BGR image
            'gray'      – grayscale + CLAHE
            'hsv'       – HSV color space image
            'normalized'– float32 [0,1] BGR
    """
    img = load_image(image_path)
    img = resize_image(img)

    gray = convert_to_grayscale(img)
    gray = apply_clahe(gray)
    hsv = convert_to_hsv(img)
    normalized = normalize_image(img)

    result = {
        "original": img,
        "gray": gray,
        "hsv": hsv,
        "normalized": normalized,
    }

    if augment:
        result["augmented"] = _augment(img)

    return result


def preprocess_from_array(image_array: np.ndarray) -> dict:
    """
    Full preprocessing pipeline for an image already loaded as a numpy array.
    Useful for images received from Flask (in-memory).
    """
    img = resize_image(image_array)
    gray = convert_to_grayscale(img)
    gray = apply_clahe(gray)
    hsv = convert_to_hsv(img)
    normalized = normalize_image(img)
    return {
        "original": img,
        "gray": gray,
        "hsv": hsv,
        "normalized": normalized,
    }


def _augment(image: np.ndarray) -> list:
    """
    Generate augmented versions of an image for training diversity.
    Returns a list of augmented images (flips, brightness variations).
    """
    augmented = []

    # Horizontal flip
    augmented.append(cv2.flip(image, 1))

    # Brightness increase
    bright = cv2.convertScaleAbs(image, alpha=1.2, beta=20)
    augmented.append(bright)

    # Brightness decrease
    dark = cv2.convertScaleAbs(image, alpha=0.8, beta=-20)
    augmented.append(dark)

    # Rotation ±15 degrees
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    for angle in [-15, 15]:
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        augmented.append(rotated)

    return augmented
