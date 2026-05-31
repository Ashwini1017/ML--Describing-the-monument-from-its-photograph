Team Members: Ashwini R, G Sahana, and K M Deepika
# Monument Vision 🏛

> **AI-Powered Indian Monument Recognition using Classical Machine Learning**

A complete final-year ML project that identifies **24 Indian monuments** from photographs using traditional computer vision and machine learning 

## 🏗 Project Structure

```
ml/
├── archive/                          ← Dataset (your existing data)
│   └── Indian-monuments/
│       └── images/
│           ├── train/               ← 24 monument class folders
│           └── test/                ← 24 monument class folders
├── src/
│   ├── __init__.py
│   ├── preprocess.py                ← Image preprocessing (CLAHE, resize, HSV)
│   ├── feature_extraction.py        ← HOG, Color Histogram, LBP, ORB
│   ├── train.py                     ← Train all 5 ML models
│   ├── predict.py                   ← Prediction module
│   └── monument_db.py               ← Monument information database
├── models/                          ← Saved trained models (auto-created)
├── reports/                         ← Accuracy plots & confusion matrix
├── static/
│   ├── css/style.css                ← Premium dark UI stylesheet
│   ├── js/app.js                    ← Frontend logic
│   └── uploads/                     ← User-uploaded images (auto-created)
├── templates/
│   └── index.html                   ← Main web page
├── app.py                           ← Flask web server
├── config.py                        ← Central configuration
├── requirements.txt
└── README.md
```


## 🔬 Feature Extraction Methods

| Feature | Description | Captures |
|---------|-------------|---------|
| **HOG** | Histogram of Oriented Gradients | Edges, shapes |
| **Color Histogram (HSV)** | H/S/V channel histograms | Color distribution |
| **LBP** | Local Binary Patterns | Texture patterns |
| **ORB Statistics** | Keypoint summary (mean, std, count) | Keypoint structure |

---

## 🤖 ML Algorithms

| Algorithm | Type | Notes |
|-----------|------|-------|
| **SVM (RBF)** | Support Vector Machine | Best for high-dim features |
| **Random Forest** | Ensemble | Handles non-linearity well |
| **KNN** | Instance-based | Distance-weighted, k=7 |
| **Decision Tree** | Tree-based | Depth-limited |
| **Naive Bayes** | Probabilistic | Gaussian NB |

---

## 🏛 Supported Monuments (24 Classes)

| # | Monument | Location |
|---|----------|----------|
| 1 | Taj Mahal | Agra, UP |
| 2 | India Gate | New Delhi |
| 3 | Qutub Minar | New Delhi |
| 4 | Gateway of India | Mumbai |
| 5 | Hawa Mahal | Jaipur |
| 6 | Golden Temple | Amritsar |
| 7 | Charminar | Hyderabad |
| 8 | Humayun's Tomb | New Delhi |
| 9 | Lotus Temple | New Delhi |
| 10 | Mysore Palace | Mysore |
| 11 | Victoria Memorial | Kolkata |
| 12 | Ajanta Caves | Aurangabad |
| 13 | Ellora Caves | Aurangabad |
| 14 | Fatehpur Sikri | Agra |
| 15 | Khajuraho | Madhya Pradesh |
| 16 | Sun Temple Konark | Odisha |
| 17 | Charar-E-Sharif | J&K |
| 18 | Chhota Imambara | Lucknow |
| 19 | Alai Darwaza | New Delhi |
| 20 | Alai Minar | New Delhi |
| 21 | Basilica of Bom Jesus | Goa |
| 22 | Iron Pillar | New Delhi |
| 23 | Jamali Kamali Tomb | New Delhi |
| 24 | Tanjavur Temple | Tamil Nadu |

---

## 🔄 ML Pipeline

```
Image Upload → Preprocessing → Feature Extraction → ML Classifier → Info Retrieval → Display
```

1. **Preprocessing**: Resize to 128×128, CLAHE enhancement, grayscale + HSV conversion
2. **Feature Extraction**: HOG + HSV Color Hist + LBP + ORB statistics → concatenated vector
3. **Scaling**: StandardScaler (zero mean, unit variance)
4. **Feature Selection**: SelectKBest (top 500 features by F-score)
5. **Classification**: Best of 5 ML models auto-selected after training
6. **Info Retrieval**: Monument info looked up from built-in database

---

## 🖥 Web Interface Features

- **Drag & Drop** image upload
- **Real-time prediction** with loading animation
- **Confidence score** with color-coded indicator
- **Top-5 predictions** bar chart
- **Complete monument info**: name, location, built by, year, architecture, entry fee, timings
- **Fun facts** and UNESCO status
- **Model comparison** — predict with all 5 models simultaneously
- **Prediction history** — save and browse past predictions
- **Save result** as JSON

---

## 💻 API Reference

### `POST /predict`
Upload an image and get monument prediction.

**Request**: `multipart/form-data` with field `image`

**Response**:
```json
{
  "success": true,
  "monument_name": "Taj Mahal",
  "location": "Agra, Uttar Pradesh, India",
  "built_by": "Mughal Emperor Shah Jahan",
  "year_built": "1632–1653",
  "architecture": "Mughal Architecture",
  "description": "...",
  "fun_fact": "...",
  "entry_fee": "₹50 (Indian), ₹1100 (Foreign)",
  "timings": "Sunrise to Sunset",
  "unesco": true,
  "confidence": 87.42,
  "top_predictions": [["Taj Mahal", 87.42], ["Humayun's Tomb", 6.1], ...],
  "model_used": "SVM (RBF)",
  "image_url": "/static/uploads/abc123.jpg"
}
```

### `GET /history`
Returns last 50 predictions as JSON array.

### `POST /all_models`
Run all 5 ML models and compare their predictions.

### `GET /models_status`
Check if models are trained.

---

## 📊 Output Files

After training, the following are saved:

| File | Description |
|------|-------------|
| `models/best_model.pkl` | Best performing ML model |
| `models/scaler.pkl` | Feature scaler |
| `models/selector.pkl` | Feature selector |
| `models/label_encoder.pkl` | Label encoder |
| `models/SVM_RBF.pkl` | SVM model |
| `models/Random_Forest.pkl` | RF model |
| `models/KNN.pkl` | KNN model |
| `models/Decision_Tree.pkl` | DT model |
| `models/Naive_Bayes.pkl` | NB model |
| `reports/confusion_matrix.png` | Confusion matrix heatmap |
| `reports/model_comparison.png` | Accuracy bar chart |
| `reports/model_comparison.csv` | Accuracy numbers CSV |

---

## 🎓 Technologies Used

- **Python 3.x**
- **OpenCV** — image loading, preprocessing
- **Scikit-learn** — ML algorithms, preprocessing, evaluation
- **Scikit-image** — HOG, LBP feature extraction
- **NumPy** — numerical computations
- **Pandas** — results tabulation
- **Matplotlib** — charts and visualizations
- **Flask** — web backend and REST API
- **Joblib** — model serialization
