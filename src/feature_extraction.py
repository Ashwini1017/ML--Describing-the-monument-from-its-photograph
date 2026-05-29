"""
feature_extraction.py — Classical Feature Extraction Module

Implements the following feature descriptors:
  - HOG  (Histogram of Oriented Gradients)  — shape/edge information
  - Color Histogram (HSV)                   — color distribution
  - LBP  (Local Binary Patterns)            — texture information
  - ORB  (Oriented FAST and Rotated BRIEF)  — keypoint statistics

All features are concatenated into a single 1-D feature vector per image.
"""

import cv2
import numpy as np
from skimage.feature import hog, local_binary_pattern


# ─── HOG Parameters ──────────────────────────────────────────────────────────
HOG_ORIENTATIONS   = 9
HOG_PIXELS_PER_CELL = (8, 8)
HOG_CELLS_PER_BLOCK = (2, 2)

# ─── LBP Parameters ──────────────────────────────────────────────────────────
LBP_RADIUS    = 3
LBP_N_POINTS  = 8 * LBP_RADIUS   # 24
LBP_N_BINS    = 64                # Histogram bins

# ─── Color Histogram Parameters ──────────────────────────────────────────────
COLOR_HIST_BINS = 32              # per channel

# ─── ORB Parameters ──────────────────────────────────────────────────────────
ORB_N_FEATURES = 500


# ─── Individual Extractors ────────────────────────────────────────────────────

def extract_hog_features(gray_image: np.ndarray) -> np.ndarray:
    """
    Extract HOG features from a grayscale image.
    HOG captures gradient orientation histograms — excellent for shape description.
    """
    features = hog(
        gray_image,
        orientations=HOG_ORIENTATIONS,
        pixels_per_cell=HOG_PIXELS_PER_CELL,
        cells_per_block=HOG_CELLS_PER_BLOCK,
        block_norm="L2-Hys",
        visualize=False,
        transform_sqrt=True,
    )
    return features.astype(np.float32)


def extract_color_histogram(hsv_image: np.ndarray, bins: int = COLOR_HIST_BINS) -> np.ndarray:
    """
    Extract a concatenated HSV color histogram.
    Robust to minor illumination changes vs. RGB histograms.
    """
    hist_h = cv2.calcHist([hsv_image], [0], None, [bins], [0, 180])
    hist_s = cv2.calcHist([hsv_image], [1], None, [bins], [0, 256])
    hist_v = cv2.calcHist([hsv_image], [2], None, [bins], [0, 256])

    # Normalize each channel histogram
    hist_h = cv2.normalize(hist_h, hist_h).flatten()
    hist_s = cv2.normalize(hist_s, hist_s).flatten()
    hist_v = cv2.normalize(hist_v, hist_v).flatten()

    return np.concatenate([hist_h, hist_s, hist_v]).astype(np.float32)


def extract_lbp_features(gray_image: np.ndarray) -> np.ndarray:
    """
    Extract LBP (Local Binary Pattern) texture features.
    LBP describes local texture patterns — good for architectural surface differentiation.
    """
    lbp = local_binary_pattern(
        gray_image, LBP_N_POINTS, LBP_RADIUS, method="uniform"
    )
    n_bins = LBP_N_POINTS + 2  # uniform LBP has P+2 patterns
    hist, _ = np.histogram(lbp.ravel(), bins=n_bins, range=(0, n_bins), density=True)
    return hist.astype(np.float32)


def extract_orb_features(gray_image: np.ndarray, n_features: int = ORB_N_FEATURES) -> np.ndarray:
    """
    Extract ORB keypoint statistics.
    Since ORB descriptors vary in count, we summarize them as a fixed-length
    statistical feature vector (mean, std, count normalized by n_features).
    """
    orb = cv2.ORB_create(nfeatures=n_features)
    keypoints, descriptors = orb.detectAndCompute(gray_image, None)

    if descriptors is None or len(descriptors) == 0:
        # No keypoints found — return zeros
        return np.zeros(66, dtype=np.float32)

    # Statistical summary of ORB descriptors (32 bytes per descriptor)
    # Mean and Std of descriptors = 64 values
    desc_mean = descriptors.mean(axis=0).astype(np.float32)   # 32 values
    desc_std  = descriptors.std(axis=0).astype(np.float32)    # 32 values

    # Keypoint statistics
    kp_count   = np.array([len(keypoints) / n_features], dtype=np.float32)
    kp_sizes   = np.array([kp.size for kp in keypoints], dtype=np.float32)
    kp_size_mean = np.array([kp_sizes.mean()], dtype=np.float32)
    kp_size_std  = np.array([kp_sizes.std()], dtype=np.float32)

    return np.concatenate([desc_mean, desc_std, kp_count, kp_size_mean, kp_size_std])


def extract_all_features(preprocessed: dict) -> np.ndarray:
    """
    Extract and concatenate ALL features from a preprocessed image dict.

    Args:
        preprocessed: dict from preprocess.py with keys 'gray' and 'hsv'

    Returns:
        1-D feature vector (HOG + Color Histogram + LBP + ORB)
    """
    gray = preprocessed["gray"]
    hsv  = preprocessed["hsv"]

    hog_feat   = extract_hog_features(gray)
    color_feat = extract_color_histogram(hsv)
    lbp_feat   = extract_lbp_features(gray)
    orb_feat   = extract_orb_features(gray)

    combined = np.concatenate([hog_feat, color_feat, lbp_feat, orb_feat])
    return combined


def get_feature_names_info() -> dict:
    """Returns info about each feature component for documentation."""
    return {
        "HOG":             f"Histogram of Oriented Gradients ({HOG_ORIENTATIONS} orient, {HOG_PIXELS_PER_CELL} ppc, {HOG_CELLS_PER_BLOCK} cpb)",
        "Color Histogram": f"HSV Histogram ({COLOR_HIST_BINS} bins/channel × 3 channels = {COLOR_HIST_BINS*3} values)",
        "LBP":             f"Local Binary Pattern (radius={LBP_RADIUS}, n_points={LBP_N_POINTS})",
        "ORB":             f"ORB Keypoint Statistics (66 values: mean+std+count+size)",
    }
