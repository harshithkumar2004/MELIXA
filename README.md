# MELIXA – AI Music Mood Prediction & Smart Playlist Matcher

A production-grade full-stack application that performs AI-based music mood prediction and smart playlist recommendation using a pre-trained machine learning model.

## 🎯 Features

- **AI Mood Prediction**: Analyze audio files to predict mood (energetic, happy, calm, sad)
- **Smart Recommendations**: Get similar songs based on audio features
- **Professional UI**: Black & white dark theme with responsive design
- **Audio Streaming**: Play recommended songs directly in the browser
- **Real-time Analysis**: Upload and analyze audio files instantly

## 🏗️ Architecture

```
├── backend/
│   ├── ml/          # FastAPI ML Service (Port 8000)
│   └── api/         # Node.js API Gateway (Port 5000)
├── frontend/
│   └── react-app/   # React Frontend (Port 3000)
├── deam/
│   ├── audio/       # DEAM dataset audio files
│   └── features.json # Pre-computed feature vectors
├── models/
│   └── anti_overfitting_mood_classifier.pkl
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Setup ML Backend (FastAPI)

```bash
cd backend/ml
pip install -r requirements.txt
python main.py
```

The ML service will start on `http://localhost:8000`

### 2. Setup API Gateway (Node.js)

```bash
cd backend/api
npm install
npm start
```

The API gateway will start on `http://localhost:5000`

### 3. Setup Frontend (React)

```bash
cd frontend/react-app
npm install
npm start
```

The frontend will start on `http://localhost:3000`

## 📊 Model Details

- **Model**: VotingClassifier with StandardScaler
- **Features**: 15 audio features extracted using librosa
- **Classes**: energetic, happy, calm, sad
- **Input**: Audio files (MP3, WAV, M4A, FLAC)

## 🔧 Feature Extraction

The system extracts exactly 15 audio features in this order:

1. tempo_mean
2. energy_rms_mean
3. spectral_centroid_mean
4. zero_crossing_rate_mean
5. spectral_rolloff_mean
6. mfcc_1_mean
7. mfcc_2_mean
8. chroma_mean
9. onset_strength_mean
10. spectral_contrast_mean
11. tempo_std
12. energy_rms_std
13. spectral_rolloff_std
14. chroma_std
15. onset_strength_std

## 🎵 Recommendation Engine

- **Similarity Calculation**: 70% cosine + 30% Euclidean distance
- **Data Source**: DEAM dataset with pre-computed features
- **Results**: Top 5 most similar songs with similarity scores

## 🌐 API Endpoints

### ML Service (Port 8000)

- `POST /predict` - Predict mood from audio file
- `GET /deam_audio/{filename}` - Stream DEAM audio files
- `GET /api/info` - Model information
- `GET /api/deam-info` - DEAM dataset information

### API Gateway (Port 5000)

- `POST /predict` - Proxy for mood prediction
- `GET /deam_audio/{filename}` - Proxy for audio streaming
- `GET /api/info` - Proxy for model info
- `GET /api/deam-info` - Proxy for DEAM info
- `GET /health` - Health check

## 🎨 UI Components

- **Upload Section**: Drag & drop or click to upload audio files
- **Audio Preview**: Preview uploaded audio before analysis
- **Results Display**: Mood prediction with confidence score
- **Probability Bars**: Horizontal bars showing all mood probabilities
- **Recommendations**: Song cards with similarity scores and audio players

## 🔒 Production Features

- **Error Handling**: Comprehensive error handling throughout the stack
- **File Cleanup**: Automatic cleanup of temporary files
- **CORS Support**: Proper CORS configuration for cross-origin requests
- **Timeout Handling**: 60-second timeout for ML predictions
- **Input Validation**: File type and size validation
- **Graceful Shutdown**: Proper cleanup on service termination

## 📱 Responsive Design

- Mobile-friendly interface
- Adaptive layouts for different screen sizes
- Touch-friendly controls
- Optimized audio players for all devices

## 🛠️ Tech Stack

### Backend ML
- Python 3.8+
- FastAPI
- librosa
- numpy, scipy
- scikit-learn
- joblib

### API Gateway
- Node.js
- Express.js
- Multer
- Axios
- CORS

### Frontend
- React 18
- Modern CSS (no frameworks)
- HTML5 Audio API
- Axios for API calls

## 📈 Performance

- **Feature Extraction**: Optimized librosa pipeline
- **Model Loading**: Single load at startup
- **File Streaming**: Range request support for audio
- **Caching**: Browser caching for static assets
- **Async Processing**: Non-blocking I/O throughout

## 🚨 Error Handling

- Invalid file formats
- Network connectivity issues
- ML service unavailability
- Audio file corruption
- Timeout scenarios
- Memory limits

## 📝 Development

### Environment Variables

Create `.env` in `backend/api/`:
```
PORT=5000
ML_SERVICE_URL=http://localhost:8000
```

### Testing

```bash
# Test ML service
curl -X POST "http://localhost:8000/predict" -F "audio=@test.mp3"

# Test API gateway
curl -X POST "http://localhost:5000/predict" -F "audio=@test.mp3"

# Health check
curl "http://localhost:5000/health"
```

## 📄 License

This project is for educational and research purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the logs in each service
2. Verify all services are running
3. Check network connectivity
4. Validate file formats
5. Review error messages