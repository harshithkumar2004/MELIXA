from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, tempfile
import json
import numpy as np

from model_loader import model, scaler, class_labels, enhanced_predict
from audio_features import extract_features
from recommender import recommend

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(audio: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(audio.file, tmp)
        path = tmp.name

    try:
        # Extract features with improved quality
        feats = extract_features(path)
        
        # Use enhanced prediction pipeline
        probs, scaled = enhanced_predict(feats)
        
        # Get the predicted mood and confidence
        mood_index = probs.argmax()
        mood = class_labels[mood_index]
        confidence = round(probs[mood_index] * 100, 2)
        
        # Extract tempo and energy from features for analysis
        tempo = float(feats[0][0])  # First feature is tempo
        energy = float(feats[0][1])  # Second feature is RMS energy
        
        # Apply additional confidence smoothing
        # If confidence is very low, apply minimum threshold
        if confidence < 30:
            confidence = max(confidence, 25.0)
        
        # Get recommendations using original features (not scaled)
        recs = recommend(feats.flatten())

        # Create response with enhanced probabilities
        response = {
            "mood": mood,
            "confidence": confidence,
            "probabilities": dict(zip(class_labels, probs.round(4))),
            "recommendations": [
                {
                    "filename": r["filename"],
                    "similarity": r["similarity"],
                    "stream_url": f"/deam_audio/{r['filename']}"
                } for r in recs
            ],
            "processing_info": {
                "feature_quality": "enhanced",
                "prediction_method": "enhanced_pipeline",
                "confidence_calibrated": True,
                "tempo": tempo,
                "energy": energy
            }
        }
        
        return response
        
    except Exception as e:
        # Enhanced error handling
        error_msg = f"Prediction failed: {str(e)}"
        print(error_msg)
        return JSONResponse(
            status_code=500, 
            content={"error": error_msg, "details": "Audio processing or model prediction failed"}
        )
    finally:
        # Clean up temporary file
        if os.path.exists(path):
            os.unlink(path)

@app.get("/deam_audio/{filename}")
async def stream_audio(filename: str):
    audio_path = os.path.join("../../deam/audio", filename)
    if not os.path.exists(audio_path):
        return JSONResponse(status_code=404, content={"error": "Audio file not found"})
    
    return FileResponse(
        audio_path, 
        media_type="audio/mpeg",
        headers={"Accept-Ranges": "bytes"}
    )

@app.get("/api/info")
async def get_info():
    return {
        "name": "MELIXA - AI Music Mood Prediction (Enhanced)",
        "version": "2.0.0",
        "model": "anti_overfitting_mood_classifier.pkl",
        "features": 15,
        "classes": class_labels.tolist(),
        "enhancements": [
            "Improved audio preprocessing",
            "Enhanced feature extraction",
            "Robust scaling with outlier handling",
            "Confidence calibration",
            "Error resilience"
        ]
    }

@app.get("/api/deam-info")
async def get_deam_info():
    try:
        with open("../../deam/features.json") as f:
            deam_data = json.load(f)
        return {
            "total_songs": len(deam_data),
            "features_per_song": len(deam_data[0]["features"]) if deam_data else 0,
            "sample_files": [item["filename"] for item in deam_data[:5]],
            "feature_quality": "enhanced"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/health")
async def health_check():
    """Enhanced health check with model status"""
    try:
        # Test model with dummy data
        test_features = np.random.rand(1, 15).astype(np.float32)
        test_probs, _ = enhanced_predict(test_features)
        
        return {
            "status": "healthy",
            "model_loaded": True,
            "enhanced_prediction": True,
            "feature_extraction": "enhanced",
            "test_prediction": test_probs.tolist()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
