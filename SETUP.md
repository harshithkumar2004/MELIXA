# MELIXA - Music Mood Prediction System

## Quick Setup Guide

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/harshithkumar2004/MELIXA.git
cd MELIXA
```

### 2. Download Audio Files
 **Important**: The audio files are not included in the repository due to size.

Download the DEAM audio files and place them in:
```
deam/audio/
```

You can get the audio files from the official DEAM dataset or contact the repository maintainer.

### 3. Backend Setup

#### API Gateway (Port 5000)
```bash
cd backend/api
npm install
npm start
```

#### ML Service (Port 8000)
```bash
cd backend/ml
pip install -r requirements.txt
python main.py
```

### 4. Frontend Setup (Port 3001)
```bash
cd smartplay-frontend
npm install
npm start
```

### 5. Access the Application
- Frontend: http://localhost:3001
- API Gateway: http://localhost:5000
- ML Service: http://localhost:8000

### 6. Verify Installation
1. All three services should be running
2. Visit http://localhost:3001
3. Upload an audio file to test mood prediction
4. Check that recommendations appear

### Troubleshooting
- **Audio processing fails**: Ensure ML service is running on port 8000
- **No audio files**: Make sure `deam/audio/` contains the MP3 files
- **Port conflicts**: Change ports in the respective configuration files

### Project Structure
```
MELIXA/
├── backend/
│   ├── api/          # Express.js API Gateway
│   └── ml/           # FastAPI ML Service
├── smartplay-frontend/ # React + Vite Frontend
├── deam/
│   ├── audio/        # Audio files (download separately)
│   └── features.json # Audio features
├── models/           # Trained ML models
└── docs/             # Documentation
```

## Features
-  Real-time music mood prediction
-  Personalized song recommendations
-  Audio feature analysis
-  Modern web interface
-  RESTful API architecture

Enjoy using MELIXA! 
