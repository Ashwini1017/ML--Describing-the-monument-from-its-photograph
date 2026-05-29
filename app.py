# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
app.py — Flask Backend for Monument Recognition System
Endpoints:
  GET  /             → serve main HTML page
  POST /predict      → accept image upload, return monument info as JSON
  GET  /history      → return prediction history as JSON
  POST /clear_history→ clear history
  GET  /models_status→ check if models are trained
  GET  /all_models   → predict with all models (model comparison)
"""

import os
import sys
import json
import uuid
import base64
import datetime
import traceback
from pathlib import Path

import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

# ─── Path Setup ──────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from predict import predict_monument, predict_all_models, is_model_trained

# ─── Flask App ───────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload
app.config["SECRET_KEY"] = "monument-ml-secret-2024"

UPLOAD_DIR   = ROOT_DIR / "static" / "uploads"
HISTORY_FILE = ROOT_DIR / "prediction_history.json"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "tiff", "webp"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _load_history() -> list:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def _save_history(history: list):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/models_status")
def models_status():
    trained = is_model_trained()
    return jsonify({"trained": trained})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Accept an image upload and return monument prediction as JSON.
    Expects: multipart/form-data with field 'image'
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not _allowed_file(file.filename):
        return jsonify({
            "error": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 400

    try:
        # Read image into memory
        file_bytes = file.read()
        np_arr = np.frombuffer(file_bytes, np.uint8)
        image  = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Could not decode image. Please upload a valid image file."}), 400

        # Save uploaded file for display
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        save_path = UPLOAD_DIR / filename
        cv2.imwrite(str(save_path), image)

        # Run prediction
        result = predict_monument(image, top_k=5)
        info   = result["info"]

        # Build response
        response = {
            "success":        True,
            "monument_name":  info["name"],
            "location":       info["location"],
            "built_by":       info["built_by"],
            "year_built":     info["year_built"],
            "architecture":   info["architecture_style"],
            "description":    info["short_description"],
            "fun_fact":       info.get("fun_fact", ""),
            "entry_fee":      info.get("entry_fee", "N/A"),
            "timings":        info.get("timings", "N/A"),
            "unesco":         info.get("unesco", False),
            "confidence":     result["confidence"],
            "top_predictions": result["top_predictions"],
            "model_used":     result["model_used"],
            "image_url":      f"/static/uploads/{filename}",
            "timestamp":      datetime.datetime.now().isoformat(),
        }

        # Save to history
        history = _load_history()
        history.insert(0, {
            "id":            uuid.uuid4().hex,
            "monument_name": info["name"],
            "confidence":    result["confidence"],
            "image_url":     f"/static/uploads/{filename}",
            "timestamp":     response["timestamp"],
            "location":      info["location"],
        })
        # Keep only last 50 entries
        _save_history(history[:50])

        return jsonify(response)

    except FileNotFoundError as e:
        if "train" in str(e).lower() or "model" in str(e).lower():
            return jsonify({
                "error": "Models are not trained yet. Please run: python src/train.py"
            }), 503
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route("/all_models", methods=["POST"])
def all_models_predict():
    """Compare predictions from all saved models."""
    if "image" not in request.files:
        return jsonify({"error": "No image provided."}), 400

    file      = request.files["image"]
    file_bytes = file.read()
    np_arr    = np.frombuffer(file_bytes, np.uint8)
    image     = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "Could not decode image."}), 400

    try:
        results = predict_all_models(image)
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history")
def get_history():
    return jsonify(_load_history())


@app.route("/clear_history", methods=["POST"])
def clear_history():
    _save_history([])
    return jsonify({"success": True, "message": "History cleared."})


@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  MONUMENT RECOGNITION SYSTEM - FLASK SERVER")
    print("=" * 55)
    if not is_model_trained():
        print("  [WARNING] Models not trained yet!")
        print("     Run: python src/train.py   before uploading images.")
    else:
        print("  [OK] Models loaded successfully.")
    print("  Open: http://127.0.0.1:5000")
    print("=" * 55 + "\n")
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
