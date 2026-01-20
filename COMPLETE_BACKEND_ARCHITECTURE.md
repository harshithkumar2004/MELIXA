# SmartPlay Complete Backend Architecture

## Backend System Overview

The SmartPlay backend is a **microservices architecture** consisting of two main services: an API Gateway and an ML Service, designed for scalability, maintainability, and high performance.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SMARTPLAY BACKEND ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │
│  │   CLIENT    │    │   API       │    │   ML        │              │
│  │   REQUEST   │───►│  GATEWAY    │───►│  SERVICE    │              │
│  │             │    │   (Node.js) │    │ (Python)    │              │
│  │ • Browser   │    │ • Port 5000 │    │ • Port 8000 │              │
│  │ • Upload    │    │ • Express    │    │ • FastAPI    │              │
│  │ • Audio     │    │ • CORS      │    │ • ML Model  │              │
│  └─────────────┘    └─────────────┘    └─────────────┘              │
│                                                                         │
│                                      │                                   │
│                                      ▼                                   │
│                            ┌─────────────┐                               │
│                            │   DEAM      │                               │
│                            │  DATASET    │                               │
│                            │             │                               │
│                            │ • 1803 MP3  │                               │
│                            │ • Features   │                               │
│                            │ • Audio      │                               │
│                            └─────────────┘                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Service Architecture

### 1. API Gateway (Node.js)

**Technology Stack:**
- **Runtime**: Node.js 16+
- **Framework**: Express.js
- **Port**: 5000
- **File Handling**: Multer middleware
- **Environment**: .env configuration

**Core Responsibilities:**
- **Request Routing**: Forward requests to ML service
- **File Upload**: Handle multipart/form-data uploads
- **CORS Management**: Cross-origin request handling
- **Error Handling**: Centralized error management
- **Logging**: Request/response logging
- **Validation**: Input validation and sanitization

**Directory Structure:**
```
backend/api/
├── index.js                 # Main Express server
├── .env                    # Environment variables
├── package.json             # Dependencies and scripts
├── package-lock.json        # Dependency lock file
├── node_modules/            # Installed dependencies
└── uploads/                # Temporary file storage
```

**Key Dependencies:**
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "multer": "^1.4.5",
    "cors": "^2.8.5",
    "morgan": "^1.10.0",
    "dotenv": "^16.0.0"
  }
}
```

**Server Configuration:**
```javascript
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const morgan = require('morgan');
const fs = require('fs');
const path = require('path');

// Express app initialization
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware configuration
app.use(cors());                    // Enable CORS
app.use(morgan('combined'));         // Request logging
app.use(express.json());           // JSON parsing
app.use(express.urlencoded({        // URL-encoded parsing
  extended: true,
  limit: '50mb'
}));

// File upload configuration
const upload = multer({
  dest: 'uploads/',              // Upload directory
  limits: {
    fileSize: 50 * 1024 * 1024  // 50MB limit
  },
  fileFilter: (req, file, cb) => {
    // Audio file validation
    const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/mp3'];
    cb(null, allowedTypes.includes(file.mimetype));
  }
});
```

### 2. ML Service (Python FastAPI)

**Technology Stack:**
- **Runtime**: Python 3.8+
- **Framework**: FastAPI
- **Port**: 8000
- **ML Library**: Scikit-learn
- **Audio Processing**: Librosa
- **Serialization**: Joblib

**Core Responsibilities:**
- **Audio Processing**: Feature extraction from audio files
- **ML Inference**: Mood classification using ensemble model
- **Heuristic Logic**: Rule-based mood enhancement
- **Recommendations**: Similarity-based song matching
- **Model Management**: Loading and serving ML models
- **Audio Streaming**: Direct audio file serving

**Directory Structure:**
```
backend/ml/
├── main.py                   # FastAPI server
├── model_loader.py           # ML model and prediction logic
├── audio_features.py         # Feature extraction
├── recommender.py            # Recommendation engine
├── requirements.txt          # Python dependencies
├── __pycache__/             # Python cache
├── test_*.py               # Test scripts (40+ files)
└── models/                  # Model files
    └── anti_overfitting_mood_classifier.pkl
```

**Key Dependencies:**
```python
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
librosa==0.10.1
numpy==1.24.3
scikit-learn==1.3.0
joblib==1.3.2
```

**Server Configuration:**
```python
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# FastAPI app initialization
app = FastAPI(
    title="SmartPlay ML API",
    description="Music Mood Classification and Recommendation API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Server startup
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

---

## API Architecture

### 1. API Gateway Endpoints

**POST /upload**
- **Purpose**: Proxy endpoint for file uploads
- **Method**: POST
- **Content-Type**: multipart/form-data
- **File**: audio file (max 50MB)
- **Response**: Forwarded ML service response

**GET /health**
- **Purpose**: Health check endpoint
- **Method**: GET
- **Response**: Service status

**Error Handling:**
```javascript
// Global error handler
app.use((error, req, res, next) => {
  console.error('Error:', error);
  
  if (error.code === 'LIMIT_FILE_SIZE') {
    return res.status(413).json({
      error: 'File too large',
      message: 'Maximum file size is 50MB'
    });
  }
  
  res.status(500).json({
    error: 'Internal server error',
    message: error.message
  });
});
```

### 2. ML Service Endpoints

**POST /predict**
- **Purpose**: Audio mood prediction and recommendations
- **Method**: POST
- **Content-Type**: multipart/form-data
- **File**: audio file
- **Response**: Mood classification + recommendations

**Response Format:**
```json
{
  "mood": "happy",
  "confidence": 37.29,
  "probabilities": {
    "calm": 0.15,
    "energetic": 0.25,
    "happy": 0.45,
    "sad": 0.15
  },
  "processing_info": {
    "tempo": 128.5,
    "energy": 0.18,
    "feature_quality": "enhanced",
    "prediction_method": "enhanced_pipeline"
  },
  "recommendations": [
    {
      "filename": "song1.mp3",
      "similarity": 0.95,
      "stream_url": "/deam_audio/song1.mp3"
    }
  ]
}
```

**GET /health**
- **Purpose**: Health check endpoint
- **Method**: GET
- **Response**: Service and model status

**GET /deam_audio/{filename}**
- **Purpose**: Audio file streaming
- **Method**: GET
- **Parameter**: filename
- **Response**: Audio file stream

---

## Data Flow Architecture

### 1. Request Processing Flow

```
Client Request → API Gateway → ML Service → Dataset → Response
     │              │              │           │         │
     │              │              │           │         │
     ▼              ▼              ▼           ▼         ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Browser │  │ Node.js │  │ Python  │  │ DEAM    │  │ JSON    │
│ Upload  │──►│ Express │──►│ FastAPI │──►│ Dataset │──►│ Response│
│ Audio   │  │ Proxy   │  │ ML      │  │ Files   │  │ to      │
│ File    │  │ CORS    │  │ Model   │  │ Features│  │ Client  │
└─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘
```

### 2. Audio Processing Pipeline

```
Audio Upload → Temp Storage → Feature Extraction → ML Prediction → Response
      │              │              │                    │            │
      │              │              │                    │            │
      ▼              ▼              ▼                    ▼            ▼
┌─────────┐  ┌─────────┐  ┌─────────┐    ┌─────────┐  ┌─────────┐
│ MP3/WAV │  │ Temp    │  │ 15      │    │ Ensemble│  │ Mood    │
│ File    │──►│ File    │──►│ Features│──►│ Model   │──►│ Result  │
│ 30s     │  │ Storage │  │ Librosa │    │ +       │  │ + Recs  │
│ 44.1kHz │  │ Cleanup  │  │ Scaling │    │ Heuristics│ │ JSON    │
└─────────┘  └─────────┘  └─────────┘    └─────────┘  └─────────┘
```

### 3. ML Pipeline Architecture

```
Raw Features → Normalization → Ensemble Model → Heuristics → Weighting → Output
      │              │              │            │           │          │
      │              │              │            │           │          │
      ▼              ▼              ▼            ▼           ▼          ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Audio   │  │ Standard│  │ Gradient│  │ Rule    │  │ Dynamic │  │ Final  │
│ Features│──►│ Scaler  │──►│ Boosting│──►│ Based   │──►│ Weight  │──►│ Mood   │
│ [15]    │  │         │  │ +       │  │ Logic   │  │ ing     │  | Prob   │
│ Tempo   │  │ μ=0,σ=1 │  │ Logistic│  │ Happy   │  │ Conf-   │  │ +      │
│ Energy  │  │         │  │ Reg     │  │ Enhance │  │ based  │  │ Conf   │
│ MFCCs   │  │         │  │ Voting  │  │ ment    │  │         │  │        │
└─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘
```

---

## Database Architecture

### 1. DEAM Dataset Structure

**File Organization:**
```
deam/
├── audio/                    # 1803 MP3 audio files
│   ├── 1.mp3
│   ├── 2.mp3
│   └── ...
├── features.json            # Pre-computed features (804KB)
└── verify_features.py      # Feature validation script
```

**Feature Data Structure:**
```json
{
  "features": [
    {
      "filename": "1.mp3",
      "features": [
        120.5,           // Tempo (BPM)
        0.15,            // RMS Energy
        2200.0,          // Spectral Centroid
        800.0,           // Spectral Bandwidth
        0.6,             // Spectral Rolloff
        0.08,            // Zero Crossing Rate
        -12.3,           // MFCC-1
        0.29,            // MFCC-2
        1.34,            // MFCC-3
        26.65,           // MFCC-4
        0.0,             // MFCC-5
        0.05,            // MFCC-6
        1803.2,          // MFCC-7
        0.30,            // MFCC-8
        1.24             // MFCC-9
      ]
    }
  ],
  "statistics": {
    "total_files": 1803,
    "feature_means": [120.5, 0.15, 2200.0, ...],
    "feature_stds": [25.0, 0.08, 800.0, ...]
  }
}
```

### 2. Model Storage

**Model Files:**
```
models/
├── anti_overfitting_mood_classifier.pkl    # Main ML model (244KB)
└── analyze_model.py                      # Model analysis script
```

**Model Bundle Structure:**
```python
model_bundle = {
    "model": VotingClassifier,              # Ensemble model
    "scaler": StandardScaler,               # Feature normalizer
    "classes": ["calm", "energetic", "happy", "sad"],
    "feature_count": 15,
    "model_metadata": {
        "training_accuracy": 0.783,
        "validation_accuracy": 0.721,
        "test_accuracy": 0.689,
        "feature_importance": [...],
        "training_date": "2026-01-19",
        "model_version": "1.0",
        "happy_enhancement": "optimized_v4"
    }
}
```

---

## Security Architecture

### 1. Input Validation

**File Upload Security:**
```javascript
// File type validation
const fileFilter = (req, file, cb) => {
  const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/mp3'];
  const allowedExtensions = ['.mp3', '.wav'];
  
  const isValidType = allowedTypes.includes(file.mimetype);
  const isValidExtension = allowedExtensions.some(ext => 
    file.originalname.toLowerCase().endsWith(ext)
  );
  
  cb(null, isValidType && isValidExtension);
};

// File size limits
const upload = multer({
  limits: {
    fileSize: 50 * 1024 * 1024,  // 50MB
    files: 1                     // Single file
  }
});
```

**Request Validation:**
```python
# FastAPI input validation
from pydantic import BaseModel
from typing import List, Optional

class MoodResponse(BaseModel):
    mood: str
    confidence: float
    probabilities: dict
    processing_info: dict
    recommendations: List[dict]

# File validation
def validate_audio_file(file: UploadFile):
    if not file.filename.endswith(('.mp3', '.wav')):
        raise HTTPException(400, "Invalid file type")
    
    if file.size > 50 * 1024 * 1024:  # 50MB
        raise HTTPException(413, "File too large")
```

### 2. CORS Security

**CORS Configuration:**
```javascript
// API Gateway CORS
app.use(cors({
  origin: ['http://localhost:3001', 'http://localhost:3000'],
  credentials: true,
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

```python
# ML Service CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
```

### 3. Error Handling

**API Gateway Error Handling:**
```javascript
// Centralized error handling
app.use((error, req, res, next) => {
  const statusCode = error.statusCode || 500;
  const message = error.message || 'Internal Server Error';
  
  // Log error
  console.error(`[${new Date().toISOString()}] Error:`, {
    method: req.method,
    url: req.url,
    error: message,
    stack: error.stack
  });
  
  // Send error response
  res.status(statusCode).json({
    error: true,
    message: message,
    timestamp: new Date().toISOString(),
    path: req.url
  });
});
```

**ML Service Error Handling:**
```python
# FastAPI error handling
from fastapi import HTTPException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )
```

---

## Performance Architecture

### 1. Caching Strategy

**Model Caching:**
```python
# Model loading with caching
import joblib
from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():
    """Load model with caching"""
    return joblib.load("../../models/anti_overfitting_mood_classifier.pkl")

# Feature caching
@lru_cache(maxsize=1000)
def get_cached_features(filename):
    """Cache feature extraction results"""
    return extract_features(filename)
```

**Response Caching:**
```javascript
// Simple in-memory cache
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

app.post('/upload', upload.single('audio'), async (req, res) => {
  const cacheKey = req.file.originalname;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return res.json(cached.data);
  }
  
  // Process request...
  const result = await processAudio(req.file);
  
  // Cache result
  cache.set(cacheKey, {
    data: result,
    timestamp: Date.now()
  });
  
  res.json(result);
});
```

### 2. Connection Pooling

**HTTP Client Optimization:**
```javascript
// Connection pooling for ML service requests
const axios = require('axios');
const http = require('http');
const https = require('https');

// Create axios instance with connection pooling
const mlServiceClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 60000,  // 60 seconds
  maxContentLength: 50 * 1024 * 1024,  // 50MB
  maxBodyLength: 50 * 1024 * 1024,
  httpAgent: new http.Agent({ keepAlive: true }),
  httpsAgent: new https.Agent({ keepAlive: true })
});
```

### 3. Memory Management

**File Cleanup:**
```python
import os
import tempfile
import shutil

@app.post("/predict")
async def predict(audio: UploadFile):
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(audio.file, tmp)
        path = tmp.name
    
    try:
        # Process file...
        result = process_audio(path)
        return result
    finally:
        # Always cleanup
        if os.path.exists(path):
            os.unlink(path)
```

---

## Monitoring Architecture

### 1. Logging System

**API Gateway Logging:**
```javascript
const winston = require('winston');

// Configure winston logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Request logging middleware
app.use((req, res, next) => {
  logger.info({
    method: req.method,
    url: req.url,
    userAgent: req.get('User-Agent'),
    ip: req.ip,
    timestamp: new Date().toISOString()
  });
  next();
});
```

**ML Service Logging:**
```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ml_service.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@app.post("/predict")
async def predict(audio: UploadFile):
    start_time = datetime.now()
    logger.info(f"Processing file: {audio.filename}")
    
    try:
        result = await process_audio(audio)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Prediction completed: {result['mood']} "
                   f"({result['confidence']}%) in {processing_time:.2f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(500, str(e))
```

### 2. Health Monitoring

**Health Check Endpoints:**
```javascript
// API Gateway health check
app.get('/health', (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: require('./package.json').version
  };
  
  res.json(health);
});
```

```python
# ML Service health check
@app.get('/health')
async def health_check():
    try:
        # Check model availability
        model = load_model()
        
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "model_loaded": model is not None,
            "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024,  # MB
            "version": "1.0.0"
        }
        
        return health
        
    except Exception as e:
        raise HTTPException(503, f"Service unavailable: {str(e)}")
```

---

## Deployment Architecture

### 1. Development Environment

**Local Development Setup:**
```
Development Machine
├── Terminal 1: API Gateway
│   $ cd backend/api
│   $ npm install
│   $ npm start
│   # Server running on http://localhost:5000
│
├── Terminal 2: ML Service
│   $ cd backend/ml
│   $ pip install -r requirements.txt
│   $ python main.py
│   # Server running on http://localhost:8000
│
└── Terminal 3: Frontend
    $ cd smartplay-frontend
    $ npm install
    $ npm run dev
    # Frontend running on http://localhost:3001
```

### 2. Production Deployment

**Docker Configuration:**
```dockerfile
# API Gateway Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 5000
CMD ["npm", "start"]
```

```dockerfile
# ML Service Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  api-gateway:
    build: ./backend/api
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=production
      - ML_SERVICE_URL=http://ml-service:8000
    depends_on:
      - ml-service
    
  ml-service:
    build: ./backend/ml
    ports:
      - "8000:8000"
    volumes:
      - ./deam:/app/deam
      - ./models:/app/models
    environment:
      - PYTHONPATH=/app
```

### 3. Environment Configuration

**API Gateway .env:**
```
NODE_ENV=development
PORT=5000
ML_SERVICE_URL=http://localhost:8000
UPLOAD_DIR=uploads
MAX_FILE_SIZE=50MB
CORS_ORIGIN=http://localhost:3001
LOG_LEVEL=info
```

**ML Service Environment:**
```python
import os
from pathlib import Path

# Configuration
CONFIG = {
    "model_path": os.getenv("MODEL_PATH", "../../models/anti_overfitting_mood_classifier.pkl"),
    "deam_path": os.getenv("DEAM_PATH", "../../deam"),
    "upload_dir": os.getenv("UPLOAD_DIR", "/tmp"),
    "max_file_size": int(os.getenv("MAX_FILE_SIZE", "52428800")),  # 50MB
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "cors_origins": os.getenv("CORS_ORIGINS", "http://localhost:3001").split(",")
}
```

---

## Scaling Architecture

### 1. Horizontal Scaling

**Load Balancer Configuration:**
```nginx
# Nginx load balancer
upstream api_gateway {
    server api-gateway-1:5000;
    server api-gateway-2:5000;
    server api-gateway-3:5000;
}

upstream ml_service {
    server ml-service-1:8000;
    server ml-service-2:8000;
    server ml-service-3:8000;
}

server {
    listen 80;
    
    location /api/ {
        proxy_pass http://api_gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /ml/ {
        proxy_pass http://ml_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Database Scaling

**Feature Storage Optimization:**
```python
# Memory-efficient feature loading
import numpy as np
import json
from typing import Dict, List

class FeatureDatabase:
    def __init__(self, features_file: str):
        self.features_file = features_file
        self._features = None
        self._index = None
    
    def load_features(self) -> Dict[str, np.ndarray]:
        """Load features with memory optimization"""
        if self._features is None:
            with open(self.features_file, 'r') as f:
                data = json.load(f)
            
            # Convert to numpy array for efficiency
            self._features = {
                item['filename']: np.array(item['features'])
                for item in data['features']
            }
            
            # Build index for fast lookup
            self._index = {i: fname for i, fname in enumerate(self._features.keys())}
        
        return self._features
    
    def get_feature_vector(self, filename: str) -> np.ndarray:
        """Fast feature lookup"""
        return self._features.get(filename)
    
    def find_similar(self, query_features: np.ndarray, top_k: int = 10):
        """Efficient similarity search"""
        features_matrix = np.array(list(self._features.values()))
        
        # Vectorized distance calculation
        distances = np.linalg.norm(features_matrix - query_features, axis=1)
        top_indices = np.argsort(distances)[:top_k]
        
        return [
            {
                'filename': list(self._features.keys())[i],
                'similarity': 1.0 / (1.0 + distances[i])
            }
            for i in top_indices
        ]
```

---

## Complete Backend Architecture Summary

### Core Components

1. **API Gateway (Node.js)**
   - Express.js server on port 5000
   - File upload handling with Multer
   - CORS management and request routing
   - Error handling and logging

2. **ML Service (Python FastAPI)**
   - FastAPI server on port 8000
   - Audio feature extraction with Librosa
   - Ensemble ML model with heuristics
   - Recommendation engine

3. **Data Layer**
   - DEAM dataset with 1803 audio files
   - Pre-computed features (804KB JSON)
   - Serialized ML model (244KB pickle)
   - Audio streaming capabilities

### Key Features

- **Microservices Architecture**: Scalable, maintainable design
- **Real-time Processing**: < 1 second audio analysis
- **Anti-Overfitting**: Regularization and cross-validation
- **Happy Enhancement**: User-optimized heuristic logic
- **Production Ready**: Security, monitoring, deployment
- **High Performance**: Caching, connection pooling, optimization

### Technology Stack

- **API Gateway**: Node.js + Express + Multer + CORS
- **ML Service**: Python + FastAPI + Scikit-learn + Librosa
- **Data Storage**: JSON + Pickle + File System
- **Deployment**: Docker + Nginx + Environment Config
- **Monitoring**: Winston + Logging + Health Checks

The SmartPlay backend architecture provides a robust, scalable foundation for AI-powered music mood classification and recommendation services.

---

*Backend architecture documentation generated on January 19, 2026*  
*Architecture Version: 1.0*  
*Status: Production Ready*
