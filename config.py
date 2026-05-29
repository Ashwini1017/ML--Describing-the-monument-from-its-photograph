# Monument Vision — Project Configuration
# All path and hyperparameter settings in one place.

from pathlib import Path

# ── Directory Paths ────────────────────────────────────────
ROOT_DIR    = Path(__file__).resolve().parent
DATASET_DIR = ROOT_DIR / "archive" / "Indian-monuments" / "images"
TRAIN_DIR   = DATASET_DIR / "train"
TEST_DIR    = DATASET_DIR / "test"
MODELS_DIR  = ROOT_DIR / "models"
REPORTS_DIR = ROOT_DIR / "reports"
UPLOAD_DIR  = ROOT_DIR / "static" / "uploads"

# ── Image Processing ───────────────────────────────────────
IMAGE_SIZE    = (128, 128)   # Width x Height
AUGMENT_TRAIN = False        # Set True to enable data augmentation

# ── Feature Extraction ─────────────────────────────────────
HOG_ORIENTATIONS    = 9
HOG_PIXELS_PER_CELL = (8, 8)
HOG_CELLS_PER_BLOCK = (2, 2)
COLOR_HIST_BINS     = 32
LBP_RADIUS          = 3
LBP_N_POINTS        = 8 * LBP_RADIUS
ORB_N_FEATURES      = 500

# ── Feature Selection ──────────────────────────────────────
K_BEST_FEATURES = 500

# ── SVM Hyperparameters ────────────────────────────────────
SVM_C      = 10
SVM_KERNEL = "rbf"
SVM_GAMMA  = "scale"

# ── Random Forest Hyperparameters ─────────────────────────
RF_N_ESTIMATORS = 200
RF_MAX_DEPTH    = None

# ── KNN Hyperparameters ────────────────────────────────────
KNN_N_NEIGHBORS = 7
KNN_WEIGHTS     = "distance"

# ── Prediction ─────────────────────────────────────────────
TOP_K_PREDICTIONS = 5
