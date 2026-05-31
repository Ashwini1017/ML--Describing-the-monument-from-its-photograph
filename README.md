Team Members: Ashwini R, G Sahana, and K M Deepika
# Monument Vision 🏛

> **AI-Powered Indian Monument Recognition using Classical Machine Learning**

 ML project that identifies **24 Indian monuments** from photographs using traditional computer vision and machine learning 

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
