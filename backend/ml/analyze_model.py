import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import json
import joblib
from audio_features import extract_features
from model_loader import model, scaler, class_labels

def analyze_feature_distribution():
    """Analyze the feature distribution to identify scaling issues"""
    
    print("=== Feature Distribution Analysis ===")
    
    # Load DEAM features for comparison
    with open("../../deam/features.json", "r") as f:
        deam_features = json.load(f)
    
    print(f"DEAM dataset size: {len(deam_features)}")
    
    # Extract all feature vectors
    all_features = []
    for entry in deam_features[:100]:  # Sample first 100
        all_features.append(entry['features'])
    
    all_features = np.array(all_features)
    print(f"Feature matrix shape: {all_features.shape}")
    
    # Calculate statistics for each feature
    print(f"\nFeature Statistics (DEAM dataset):")
    for i in range(15):
        col = all_features[:, i]
        print(f"Feature {i}: mean={col.mean():.3f}, std={col.std():.3f}, min={col.min():.3f}, max={col.max():.3f}")
    
    # Test a few audio files and compare
    test_files = ["../../deam/audio/10.mp3", "../../deam/audio/1000.mp3"]
    
    for audio_file in test_files:
        if os.path.exists(audio_file):
            print(f"\n--- Analyzing {os.path.basename(audio_file)} ---")
            
            # Extract features
            features = extract_features(audio_file)
            print(f"Extracted features: {features.flatten()}")
            
            # Apply original scaling
            scaled_original = scaler.transform(features)
            print(f"Scaled features: {scaled_original.flatten()}")
            
            # Check if scaled features are within reasonable range
            print(f"Scaled range: [{scaled_original.min():.3f}, {scaled_original.max():.3f}]")
            
            # Get prediction
            probs = model.predict_proba(scaled_original)[0]
            print(f"Probabilities: {probs}")
            
            mood_idx = probs.argmax()
            predicted_mood = class_labels[mood_idx]
            print(f"Predicted: {predicted_mood} ({probs[mood_idx]:.3f})")

def check_model_training():
    """Check if the model was trained properly"""
    
    print(f"\n=== Model Training Analysis ===")
    
    bundle = joblib.load("../../models/anti_overfitting_mood_classifier.pkl")
    
    print(f"Model type: {type(bundle['model'])}")
    
    # Check if it's a VotingClassifier
    if hasattr(bundle['model'], 'estimators_'):
        print(f"Number of estimators: {len(bundle['model'].estimators_)}")
        for i, (name, estimator) in enumerate(bundle['model'].estimators_):
            print(f"  Estimator {i}: {name} - {type(estimator)}")
    
    # Check scaler parameters
    print(f"Scaler mean: {bundle['scaler'].mean_}")
    print(f"Scaler scale: {bundle['scaler'].scale_}")
    print(f"Scaler mean shape: {bundle['scaler'].mean_.shape}")
    print(f"Scaler scale shape: {bundle['scaler'].scale_.shape}")

if __name__ == "__main__":
    analyze_feature_distribution()
    check_model_training()
