"""
predict.py — Prediction Module

Loads trained models and makes predictions on new images.
Returns monument name + confidence + info from the database.
"""

import sys
import numpy as np
import cv2
import joblib
from pathlib import Path

ROOT_DIR   = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / "models"
sys.path.insert(0, str(ROOT_DIR / "src"))

from preprocess import preprocess_from_array, preprocess_image
from feature_extraction import extract_all_features
from monument_db import get_monument_info


# ─── Model Cache (loaded once) ────────────────────────────────────────────────
_cache = {}


def _load_models():
    """Load all saved model artifacts into cache (called once)."""
    global _cache
    if _cache:
        return _cache

    required = ["best_model.pkl", "Naive_Bayes.pkl", "scaler.pkl", "selector.pkl", "label_encoder.pkl"]
    for fname in required:
        path = MODELS_DIR / fname
        if not path.exists():
            raise FileNotFoundError(
                f"Model file not found: {path}\n"
                "Please run 'python src/train.py' first to train the models."
            )

    _cache = {
        "model":   joblib.load(MODELS_DIR / "best_model.pkl"),
        "naive_bayes": joblib.load(MODELS_DIR / "Naive_Bayes.pkl"),
        "scaler":  joblib.load(MODELS_DIR / "scaler.pkl"),
        "selector":joblib.load(MODELS_DIR / "selector.pkl"),
        "le":      joblib.load(MODELS_DIR / "label_encoder.pkl"),
    }

    # Read best model name
    name_file = MODELS_DIR / "best_model_name.txt"
    _cache["model_name"] = name_file.read_text().strip() if name_file.exists() else "Unknown"

    return _cache


def _extract_feature_vector(image_array: np.ndarray) -> np.ndarray:
    """Preprocess image and extract feature vector."""
    preprocessed = preprocess_from_array(image_array)
    features = extract_all_features(preprocessed)
    return features


def _apply_transforms(features: np.ndarray, cache: dict) -> np.ndarray:
    """Apply scaler + feature selector transforms."""
    scaler   = cache["scaler"]
    selector = cache["selector"]

    scaled = scaler.transform(features.reshape(1, -1))
    # Shift to non-negative for selector
    min_vals = scaled.min(axis=1, keepdims=True)
    shifted  = scaled - min_vals
    selected = selector.transform(shifted)
    return selected


def predict_monument(image_array: np.ndarray, top_k: int = 3) -> dict:
    """
    Predict monument class from a BGR image array using Naive Bayes by default.

    Args:
        image_array: NumPy BGR image (e.g. from cv2.imread or decoded upload)
        top_k:       Number of top predictions to return

    Returns:
        dict with keys:
            'monument_name'  – predicted monument label
            'confidence'     – confidence percentage (0-100)
            'top_predictions'– list of (label, confidence%) tuples
            'info'           – monument info dict from monument_db
            'model_used'     – name of model used
    """
    cache = _load_models()
    model = cache["naive_bayes"]  # Bypassing SVM and using Naive Bayes directly
    le    = cache["le"]
    scaler = cache["scaler"]

    # Feature extraction
    features = _extract_feature_vector(image_array)
    
    # Naive Bayes is trained on scaled features without feature selection
    scaled = scaler.transform(features.reshape(1, -1))
    X = scaled

    # Predict
    if hasattr(model, "predict_proba"):
        proba     = model.predict_proba(X)[0]
        pred_idx  = int(np.argmax(proba))
        confidence = float(proba[pred_idx]) * 100.0

        # Top-K predictions
        top_k = min(top_k, len(le.classes_))
        top_idxs = np.argsort(proba)[::-1][:top_k]
        top_preds = [
            (le.inverse_transform([i])[0], round(float(proba[i]) * 100, 2))
            for i in top_idxs
        ]
    else:
        pred_idx   = int(model.predict(X)[0])
        confidence = 100.0  # No probability support
        top_preds  = [(le.inverse_transform([pred_idx])[0], 100.0)]

    monument_name = le.inverse_transform([pred_idx])[0]
    info = get_monument_info(monument_name)

    return {
        "monument_name":   monument_name,
        "confidence":      round(confidence, 2),
        "top_predictions": top_preds,
        "info":            info,
        "model_used":      "Naive Bayes",
    }


def predict_from_path(image_path: str, top_k: int = 3) -> dict:
    """Predict from file path."""
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")
    return predict_monument(img, top_k=top_k)


def predict_all_models(image_array: np.ndarray) -> list:
    """
    Run prediction with ALL saved models and compare results.
    Returns a list of dicts with model name, prediction, and confidence.
    """
    cache = _load_models()
    le    = cache["le"]
    scaler   = cache["scaler"]
    selector = cache["selector"]

    # Extract features once
    features = _extract_feature_vector(image_array)
    scaled   = scaler.transform(features.reshape(1, -1))
    shifted  = scaled - scaled.min(axis=1, keepdims=True)
    selected = selector.transform(shifted)

    results = []
    model_files = list(MODELS_DIR.glob("*.pkl"))
    model_files = [f for f in model_files if f.name not in (
        "best_model.pkl", "scaler.pkl", "selector.pkl", "label_encoder.pkl"
    )]

    MODEL_NAMES = {
        "SVM_RBF.pkl":        "SVM (RBF)",
        "Random_Forest.pkl":  "Random Forest",
        "KNN.pkl":            "KNN",
        "Decision_Tree.pkl":  "Decision Tree",
        "Naive_Bayes.pkl":    "Naive Bayes",
    }

    NB_MODELS = {"Naive Bayes"}

    for model_file in sorted(model_files):
        try:
            clf = joblib.load(model_file)
            display_name = MODEL_NAMES.get(model_file.name, model_file.stem)

            X = scaled if display_name in NB_MODELS else selected

            if hasattr(clf, "predict_proba"):
                proba     = clf.predict_proba(X)[0]
                pred_idx  = int(np.argmax(proba))
                conf      = float(proba[pred_idx]) * 100.0
            else:
                pred_idx = int(clf.predict(X)[0])
                conf     = 100.0

            label = le.inverse_transform([pred_idx])[0]
            results.append({
                "model":      display_name,
                "prediction": label,
                "confidence": round(conf, 2),
                "info":       get_monument_info(label)
            })
        except Exception as e:
            results.append({
                "model":      model_file.stem,
                "prediction": "Error",
                "confidence": 0.0,
                "error":      str(e),
                "info":       None
            })

    return results


def is_model_trained() -> bool:
    """Returns True if trained model files exist."""
    required = ["best_model.pkl", "Naive_Bayes.pkl", "scaler.pkl", "selector.pkl", "label_encoder.pkl"]
    return all((MODELS_DIR / f).exists() for f in required)


# ─── CLI Usage ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python src/predict.py <image_path>")
        sys.exit(1)

    result = predict_from_path(sys.argv[1])
    info   = result["info"]
    print("\n" + "=" * 50)
    print(f"  MONUMENT IDENTIFIED")
    print("=" * 50)
    print(f"  Name        : {info['name']}")
    print(f"  Location    : {info['location']}")
    print(f"  Built By    : {info['built_by']}")
    print(f"  Year Built  : {info['year_built']}")
    print(f"  Architecture: {info['architecture_style']}")
    print(f"  Confidence  : {result['confidence']:.2f}%")
    print(f"  Model Used  : {result['model_used']}")
    print("\n  Top Predictions:")
    for label, conf in result["top_predictions"]:
        bar = "█" * int(conf / 5)
        print(f"    {label:<30} {conf:6.2f}% {bar}")
    print("\n  Description:")
    print(f"  {info['short_description'][:200]}…")
    print("=" * 50)
