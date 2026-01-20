# SmartPlay Full Project Structure (Excluding Frontend)

## 📁 Root Directory Structure

```
d:\melixa/
├── 📄 REPORTS
│   ├── DATASET_TEST_REPORT.md          (12,620 bytes)
│   ├── FULL_PROJECT_REPORT.md          (29,795 bytes)
│   ├── ML_MODEL_TEST_REPORT.md         (15,459 bytes)
│   ├── SYSTEM_TEST_REPORT.md           (9,846 bytes)
│   └── README.md                     (5,593 bytes)
│
├── 📂 backend/                      (Backend services)
│   ├── 📂 api/                     (Node.js API Gateway)
│   │   ├── .env                     (95 bytes - Environment variables)
│   │   ├── index.js                 (4,414 bytes - Main API server)
│   │   ├── node_modules/             (Dependencies)
│   │   ├── package-lock.json         (55,666 bytes - Dependency lock)
│   │   ├── package.json              (474 bytes - Package configuration)
│   │   └── uploads/                 (File upload directory)
│   │
│   └── 📂 ml/                      (Python ML Service)
│       ├── 📂 __pycache__/           (Python cache)
│       ├── 📄 Core ML Files
│       │   ├── main.py               (5,182 bytes - FastAPI server)
│       │   ├── model_loader.py        (6,808 bytes - ML model loader)
│       │   └── recommender.py        (639 bytes - Recommendation engine)
│       │
│       ├── 📄 Feature Processing
│       │   ├── audio_features.py      (3,323 bytes - Audio feature extraction)
│       │   └── process_all_deam.py   (3,705 bytes - Batch processing)
│       │
│       ├── 📄 Analysis & Testing
│       │   ├── analyze_balance.py     (4,199 bytes - Mood balance analysis)
│       │   ├── analyze_happy_audio.py (4,062 bytes - Happy audio analysis)
│       │   ├── analyze_model.py       (3,252 bytes - Model analysis)
│       │   ├── balance_predictions.py  (2,394 bytes - Prediction balancing)
│       │   ├── debug_similarity.py    (3,731 bytes - Similarity debugging)
│       │   ├── diagnose_calm_issue.py (2,061 bytes - Calm prediction diagnosis)
│       │   ├── investigate_calm.py   (3,974 bytes - Calm investigation)
│       │   └── mood_ranges_complete.py (6,868 bytes - Complete mood ranges)
│       │
│       ├── 📄 Test Scripts (40+ files)
│       │   ├── test_*.py             (Various test scripts)
│       │   ├── test_happy_increase*.py (Happy detection tests)
│       │   ├── test_connection.py     (1,422 bytes - Connection testing)
│       │   ├── test_display_fix.py    (2,386 bytes - Display fix testing)
│       │   ├── test_analysis_boxes.py  (3,105 bytes - Analysis box testing)
│       │   └── [40+ test files]    (Comprehensive test suite)
│       │
│       └── 📄 Configuration
│           └── requirements.txt       (143 bytes - Python dependencies)
│
├── 📂 deam/                         (DEAM Dataset)
│   ├── 📂 audio/                    (1,802 MP3 audio files)
│   ├── 📄 features.json             (804,812 bytes - Pre-computed features)
│   └── 📄 verify_features.py       (826 bytes - Feature verification)
│
├── 📂 models/                       (ML Models)
│   ├── anti_overfitting_mood_classifier.pkl (244,685 bytes - Main ML model)
│   └── analyze_model.py                (2,653 bytes - Model analysis)
│
└── 📂 smartplay-frontend/           (Alternative frontend)
    └── [26 files]                   (Frontend components)
```

---

## 📊 Directory Statistics

### **📁 Backend Directory (44 items)**
- **API Gateway**: Node.js server (Port 5000)
- **ML Service**: Python FastAPI (Port 8000)
- **Test Suite**: 40+ comprehensive test scripts
- **Core Files**: Main server, model loader, recommender

### **📁 DEAM Dataset (1,804 items)**
- **Audio Files**: 1,802 MP3 files
- **Feature Data**: 804KB JSON file with 27,045 features
- **Verification**: Feature validation scripts

### **📁 Models Directory (2 items)**
- **Main Model**: 244KB serialized ML model
- **Analysis**: Model inspection and validation

### **📁 Reports (5 files)**
- **System Test**: 9.8KB comprehensive system testing
- **Dataset Test**: 12.6KB dataset validation
- **ML Model Test**: 15.5KB model performance analysis
- **Full Project**: 29.8KB complete project documentation
- **README**: 5.6KB project overview

---

## 🔧 Key Components

### **🤖 ML Pipeline**
```
backend/ml/
├── main.py                    # FastAPI server (Port 8000)
├── model_loader.py            # Ensemble ML model + heuristics
├── recommender.py            # Similarity-based recommendations
├── audio_features.py         # 15-feature extraction pipeline
└── requirements.txt          # Python dependencies
```

### **🌐 API Gateway**
```
backend/api/
├── index.js                 # Node.js server (Port 5000)
├── .env                    # Environment configuration
├── package.json             # Node.js dependencies
└── uploads/                # File upload directory
```

### **📊 Dataset Structure**
```
deam/
├── audio/                   # 1,802 MP3 files (30s each)
├── features.json           # 27,045 features (15 per file)
└── verify_features.py      # Feature validation
```

### **📈 Test Suite Coverage**
```
backend/ml/test_*.py (40+ files)
├── Connection Testing       # API connectivity
├── Model Testing         # ML model validation
├── Happy Detection       # Happy mood optimization
├── Display Testing       # UI component testing
├── Integration Testing   # End-to-end workflows
└── Performance Testing  # Speed and efficiency
```

---

## 📋 File Categories

### **🔧 Core System Files**
- `backend/ml/main.py` - FastAPI ML server
- `backend/ml/model_loader.py` - ML model with heuristics
- `backend/api/index.js` - Node.js API gateway
- `models/anti_overfitting_mood_classifier.pkl` - Trained ML model

### **📊 Data Files**
- `deam/features.json` - 27,045 pre-computed features
- `deam/audio/` - 1,802 MP3 audio files
- `backend/ml/recommender.py` - Recommendation engine

### **🧪 Test Files (40+)**
- `test_happy_increase*.py` - Happy detection optimization
- `test_connection.py` - API connectivity testing
- `test_analysis_boxes.py` - UI component testing
- `test_display_fix.py` - Display issue resolution
- `analyze_balance.py` - Mood distribution analysis

### **📄 Documentation**
- `README.md` - Project overview and setup
- `SYSTEM_TEST_REPORT.md` - System validation
- `DATASET_TEST_REPORT.md` - Dataset analysis
- `ML_MODEL_TEST_REPORT.md` - ML model performance
- `FULL_PROJECT_REPORT.md` - Complete project documentation

---

## 🎯 Architecture Summary

### **🏗️ Three-Tier Architecture**
1. **Frontend**: React application (excluded from this structure)
2. **Backend API**: Node.js gateway (Port 5000)
3. **ML Service**: Python FastAPI (Port 8000)

### **📊 Data Flow**
```
Audio Upload → Feature Extraction → ML Prediction → Heuristic Enhancement → Recommendations → Audio Streaming
```

### **🧠 ML Pipeline**
```
15 Acoustic Features → Ensemble Model → Heuristic Logic → Dynamic Weighting → Mood Classification
```

---

## 📈 Project Scale

### **📁 Total Directories**: 8 major directories
### **📄 Total Files**: 2,000+ files (including node_modules)
### **📊 Dataset Size**: 1,802 audio files + 804KB features
### **🧪 Test Coverage**: 40+ comprehensive test scripts
### **📄 Documentation**: 5 detailed reports (73KB total)

---

## 🚀 Deployment Structure

### **🌐 Services**
- **Frontend**: Port 3001 (React + Vite)
- **API Gateway**: Port 5000 (Node.js)
- **ML Service**: Port 8000 (FastAPI)

### **📊 Data Storage**
- **Audio Files**: 2.1GB (1,802 MP3 files)
- **Model Files**: 244KB (serialized ML model)
- **Feature Data**: 804KB (JSON features)

### **🔧 Configuration**
- **Environment**: `.env` files for API keys
- **Dependencies**: `requirements.txt` and `package.json`
- **Models**: Serialized pickle files for ML models

---

*Project structure generated on January 19, 2026*  
*Excluding frontend directory as requested*  
*Total backend components: 2,000+ files*
