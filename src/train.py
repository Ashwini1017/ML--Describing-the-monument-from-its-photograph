# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
train.py — Model Training Module

Workflow:
  1. Walk through the dataset directory (train/)
  2. Preprocess each image
  3. Extract feature vectors
  4. Train 5 ML classifiers: SVM, Random Forest, KNN, Decision Tree, Naive Bayes
  5. Evaluate on test set and print accuracy table
  6. Save best model + scaler + label encoder to models/

Run: python src/train.py
"""

import os
import sys
import time
import warnings
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from pathlib import Path
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    ConfusionMatrixDisplay,
)
from sklearn.feature_selection import SelectKBest, chi2, f_classif

warnings.filterwarnings("ignore")

# ─── Path Setup ──────────────────────────────────────────────────────────────
ROOT_DIR   = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT_DIR / "archive" / "Indian-monuments" / "images"
TRAIN_DIR   = DATASET_DIR / "train"
TEST_DIR    = DATASET_DIR / "test"
MODELS_DIR  = ROOT_DIR / "models"
REPORTS_DIR = ROOT_DIR / "reports"
MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT_DIR / "src"))
from preprocess import preprocess_image
from feature_extraction import extract_all_features, get_feature_names_info

# ─── Label Alias (normalise folder names to clean labels) ────────────────────
LABEL_ALIASES = {
    "India gate pics":    "India Gate",
    "India_gate":         "India Gate",
    "hawa mahal pics":    "Hawa Mahal",
    "Humayun_s Tomb":     "Humayun's Tomb",
    "qutub_minar":        "Qutub Minar",
    "mysore_palace":      "Mysore Palace",
    "lotus_temple":       "Lotus Temple",
    "alai_darwaza":       "Alai Darwaza",
    "alai_minar":         "Alai Minar",
    "basilica_of_bom_jesus": "Basilica of Bom Jesus",
    "iron_pillar":        "Iron Pillar",
    "jamali_kamali_tomb": "Jamali Kamali Tomb",
    "tajmahal":           "Taj Mahal",
    "golden temple":      "Golden Temple",
    "charminar":          "Charminar",
    "victoria memorial":  "Victoria Memorial",
    "tanjavur temple":    "Tanjavur Temple",
    "Charar-E- Sharif":   "Charar-E-Sharif",
    "Chhota_Imambara":    "Chhota Imambara",
    "Hawa mahal":         "Hawa Mahal",
}

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


# ─── Data Loading ─────────────────────────────────────────────────────────────

def load_dataset(dataset_dir: Path, augment: bool = False, verbose: bool = True):
    """
    Walk through dataset_dir, process each image and extract features.
    Returns (X, y, label_names).
    """
    X, y = [], []
    skipped = 0
    total = 0

    classes = sorted([d for d in dataset_dir.iterdir() if d.is_dir()])
    if verbose:
        print(f"\n[LOAD] Loading dataset from: {dataset_dir}")
        print(f"   Found {len(classes)} monument classes.\n")

    for class_dir in classes:
        raw_label = class_dir.name
        label = LABEL_ALIASES.get(raw_label, raw_label)

        image_files = [
            f for f in class_dir.iterdir()
            if f.suffix.lower() in SUPPORTED_EXTS
        ]

        if verbose:
            print(f"  [{label}]  ->  {len(image_files)} images")

        for img_path in image_files:
            total += 1
            try:
                preprocessed = preprocess_image(str(img_path), augment=augment)
                features = extract_all_features(preprocessed)
                X.append(features)
                y.append(label)

                # Augmented images (if requested)
                if augment and "augmented" in preprocessed:
                    from preprocess import preprocess_from_array
                    for aug_img in preprocessed["augmented"]:
                        aug_prep = preprocess_from_array(aug_img)
                        aug_feat = extract_all_features(aug_prep)
                        X.append(aug_feat)
                        y.append(label)

            except Exception as e:
                skipped += 1
                if verbose:
                    print(f"    [SKIP] Skipped {img_path.name}: {e}")

    if verbose:
        print(f"\n[OK] Loaded {len(X)} samples ({skipped} skipped, total {total} images)")

    return np.array(X, dtype=np.float32), np.array(y)


# ─── Model Definitions ────────────────────────────────────────────────────────

def get_models():
    """Returns a dict of named classifier instances."""
    return {
        "SVM (RBF)": SVC(
            kernel="rbf",
            C=10,
            gamma="scale",
            probability=True,
            random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            min_samples_split=2,
            random_state=42,
            n_jobs=-1,
        ),
        "KNN": KNeighborsClassifier(
            n_neighbors=7,
            weights="distance",
            metric="euclidean",
            n_jobs=-1,
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=20,
            min_samples_split=5,
            random_state=42,
        ),
        "Naive Bayes": GaussianNB(),
    }


# ─── Training Pipeline ────────────────────────────────────────────────────────

def train_and_evaluate():
    print("=" * 65)
    print("   MONUMENT RECOGNITION - ML TRAINING PIPELINE")
    print("=" * 65)

    # ── 1. Load training data ──
    X_train, y_train = load_dataset(TRAIN_DIR, augment=False, verbose=True)

    # ── 2. Load test data ──
    print(f"\n[LOAD] Loading test set...")
    X_test, y_test = load_dataset(TEST_DIR, augment=False, verbose=False)
    print(f"[OK] Test set: {len(X_test)} samples")

    # ── 3. Encode labels ──
    le = LabelEncoder()
    le.fit(np.concatenate([y_train, y_test]))
    y_train_enc = le.transform(y_train)
    y_test_enc  = le.transform(y_test)
    print(f"\n[CLASSES] {list(le.classes_)}")

    # ── 4. Scale features ──
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # ── 5. Feature selection (keep top K features) ──
    K_FEATURES = min(500, X_train_scaled.shape[1])
    selector = SelectKBest(f_classif, k=K_FEATURES)
    # Shift to non-negative for compatibility
    X_tr_sel = selector.fit_transform(X_train_scaled - X_train_scaled.min(axis=0), y_train_enc)
    X_te_sel = selector.transform(X_test_scaled - X_test_scaled.min(axis=0))
    print(f"[FEAT] Feature selection: keeping top {K_FEATURES} / {X_train_scaled.shape[1]} features")

    # ── 6. Train all models ──
    models      = get_models()
    results     = {}
    best_acc    = 0.0
    best_name   = ""
    best_model  = None

    print("\n" + "-" * 65)
    print(f"{'Model':<20} {'Train Acc':>10} {'Test Acc':>10} {'Time':>8}")
    print("-" * 65)

    for name, clf in models.items():
        t0 = time.time()

        # Naive Bayes needs non-negative inputs (use original scaled)
        if name == "Naive Bayes":
            Xtr = X_train_scaled
            Xte = X_test_scaled
        else:
            Xtr = X_tr_sel
            Xte = X_te_sel

        clf.fit(Xtr, y_train_enc)

        train_acc = accuracy_score(y_train_enc, clf.predict(Xtr))
        test_acc  = accuracy_score(y_test_enc,  clf.predict(Xte))
        elapsed   = time.time() - t0

        results[name] = {
            "model": clf,
            "train_acc": train_acc,
            "test_acc": test_acc,
            "time": elapsed,
            "uses_selection": name != "Naive Bayes",
        }

        print(f"{name:<20} {train_acc:>9.2%} {test_acc:>9.2%} {elapsed:>6.1f}s")

        if test_acc > best_acc:
            best_acc   = test_acc
            best_name  = name
            best_model = clf

    print("-" * 65)
    print(f"\n[BEST] Best model: {best_name}  (test accuracy: {best_acc:.2%})")

    # ── 7. Detailed report for best model ──
    best_info = results[best_name]
    Xte_best = X_te_sel if best_info["uses_selection"] else X_test_scaled
    Xtr_best = X_tr_sel if best_info["uses_selection"] else X_train_scaled

    y_pred = best_model.predict(Xte_best)
    print(f"\n[REPORT] Classification Report - {best_name}:\n")
    # Note: some classes may have 0 test samples; use zero_division=0 to handle gracefully
    labels_present = sorted(set(y_test_enc))
    names_present  = [le.classes_[i] for i in labels_present]
    print(classification_report(
        y_test_enc, y_pred,
        labels=labels_present,
        target_names=names_present,
        zero_division=0,
    ))

    # ── 8. Save confusion matrix plot ──
    _save_confusion_matrix(
        y_test_enc, y_pred, names_present, best_name, labels=labels_present
    )

    # ── 9. Save accuracy comparison chart ──
    _save_accuracy_chart(results)

    # ── 10. Save models ──
    print("\n[SAVE] Saving models...")
    joblib.dump(best_model,  MODELS_DIR / "best_model.pkl")
    joblib.dump(scaler,      MODELS_DIR / "scaler.pkl")
    joblib.dump(selector,    MODELS_DIR / "selector.pkl")
    joblib.dump(le,          MODELS_DIR / "label_encoder.pkl")

    # Save all models for comparison
    for name, info in results.items():
        safe_name = name.replace(" ", "_").replace("(", "").replace(")", "")
        joblib.dump(info["model"], MODELS_DIR / f"{safe_name}.pkl")

    # Save results CSV
    df = pd.DataFrame([
        {
            "Model": name,
            "Train Accuracy": f"{info['train_acc']:.4f}",
            "Test Accuracy":  f"{info['test_acc']:.4f}",
            "Training Time (s)": f"{info['time']:.2f}",
        }
        for name, info in results.items()
    ])
    df.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)

    # Save best model name
    with open(MODELS_DIR / "best_model_name.txt", "w") as f:
        f.write(best_name)

    print(f"[OK] Models saved to: {MODELS_DIR}")
    print(f"[OK] Reports saved to: {REPORTS_DIR}")
    print("\n" + "=" * 65)
    print("   TRAINING COMPLETE!")
    print("=" * 65)
    return results


# ─── Plot Helpers ─────────────────────────────────────────────────────────────

def _save_confusion_matrix(y_true, y_pred, class_names, model_name, labels=None):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(16, 14))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    disp.plot(ax=ax, colorbar=True, xticks_rotation=45, cmap="Blues")
    ax.set_title(f"Confusion Matrix - {model_name}", fontsize=14, pad=20)
    plt.tight_layout()
    fig.savefig(REPORTS_DIR / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Confusion matrix saved -> reports/confusion_matrix.png")


def _save_accuracy_chart(results: dict):
    names      = list(results.keys())
    train_accs = [results[n]["train_acc"] * 100 for n in names]
    test_accs  = [results[n]["test_acc"]  * 100 for n in names]

    x = np.arange(len(names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width / 2, train_accs, width, label="Train Accuracy", color="#4C72B0", alpha=0.85)
    bars2 = ax.bar(x + width / 2, test_accs,  width, label="Test Accuracy",  color="#DD8452", alpha=0.85)

    ax.set_xlabel("Model", fontsize=12)
    ax.set_ylabel("Accuracy (%)", fontsize=12)
    ax.set_title("Model Comparison - Train vs Test Accuracy", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=20, ha="right")
    ax.set_ylim(0, 110)
    ax.legend()
    ax.bar_label(bars1, fmt="%.1f%%", padding=3, fontsize=8)
    ax.bar_label(bars2, fmt="%.1f%%", padding=3, fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    fig.savefig(REPORTS_DIR / "model_comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Accuracy chart saved -> reports/model_comparison.png")


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    train_and_evaluate()
