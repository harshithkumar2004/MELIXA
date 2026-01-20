import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import joblib
from audio_features import extract_features
from model_loader import enhanced_predict, class_labels

def test_predictions():
    """Test the model with sample audio files to check prediction quality"""
    
    print("=== MELIXA Model Diagnostic ===")
    print(f"Classes: {class_labels}")
    print(f"Model type: {type(joblib.load('../../models/anti_overfitting_mood_classifier.pkl')['model'])}")
    
    # Test with a few DEAM audio files
    test_files = [
        "../../deam/audio/10.mp3",
        "../../deam/audio/100.mp3", 
        "../../deam/audio/1000.mp3"
    ]
    
    for audio_file in test_files:
        if os.path.exists(audio_file):
            print(f"\n--- Testing {os.path.basename(audio_file)} ---")
            
            try:
                # Extract features
                features = extract_features(audio_file)
                print(f"Features shape: {features.shape}")
                print(f"Feature range: [{features.min():.3f}, {features.max():.3f}]")
                print(f"Sample features: {features.flatten()[:5]}")
                
                # Get predictions
                probs, scaled = enhanced_predict(features)
                print(f"Raw probabilities: {probs}")
                
                # Get predicted mood
                mood_idx = probs.argmax()
                predicted_mood = class_labels[mood_idx]
                confidence = probs[mood_idx]
                
                print(f"Predicted mood: {predicted_mood}")
                print(f"Confidence: {confidence:.3f}")
                print(f"All probabilities:")
                for i, (mood, prob) in enumerate(zip(class_labels, probs)):
                    print(f"  {mood}: {prob:.3f}")
                
            except Exception as e:
                print(f"Error processing {audio_file}: {e}")
        else:
            print(f"File not found: {audio_file}")
    
    # Test with random data to see model behavior
    print(f"\n--- Testing with random data ---")
    random_features = np.random.rand(1, 15).astype(np.float32)
    print(f"Random features shape: {random_features.shape}")
    
    try:
        probs, scaled = enhanced_predict(random_features)
        print(f"Random data probabilities: {probs}")
        
        mood_idx = probs.argmax()
        predicted_mood = class_labels[mood_idx]
        confidence = probs[mood_idx]
        
        print(f"Random predicted mood: {predicted_mood}")
        print(f"Random confidence: {confidence:.3f}")
        
    except Exception as e:
        print(f"Error with random data: {e}")

if __name__ == "__main__":
    test_predictions()
