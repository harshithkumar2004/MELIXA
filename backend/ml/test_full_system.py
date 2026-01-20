import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import json
from audio_features import extract_features
from model_loader import enhanced_predict, class_labels
from recommender import recommend

def test_full_pipeline():
    """Test the complete prediction and recommendation pipeline"""
    
    print("=== Full Pipeline Test ===")
    
    # Test with a DEAM audio file
    test_file = "../../deam/audio/10.mp3"
    
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        return
    
    print(f"Testing with: {os.path.basename(test_file)}")
    
    try:
        # Step 1: Extract features
        print("1. Extracting features...")
        features = extract_features(test_file)
        print(f"   Features shape: {features.shape}")
        print(f"   Sample features: {features.flatten()[:5]}")
        
        # Step 2: Get prediction
        print("2. Getting prediction...")
        probs, scaled = enhanced_predict(features)
        print(f"   Raw probabilities: {probs}")
        
        mood_idx = probs.argmax()
        predicted_mood = class_labels[mood_idx]
        confidence = probs[mood_idx]
        
        print(f"   Predicted mood: {predicted_mood}")
        print(f"   Confidence: {confidence:.3f}")
        
        # Step 3: Get recommendations
        print("3. Getting recommendations...")
        try:
            recommendations = recommend(scaled.flatten())
            print(f"   Number of recommendations: {len(recommendations)}")
            
            for i, rec in enumerate(recommendations[:3]):  # Show top 3
                print(f"   {i+1}. {rec['filename']} - Similarity: {rec['similarity']:.3f}")
                
        except Exception as e:
            print(f"   Recommendation error: {e}")
            import traceback
            traceback.print_exc()
        
        # Step 4: Check DEAM features file
        print("4. Checking DEAM features...")
        try:
            with open("../../deam/features.json", "r") as f:
                deam_data = json.load(f)
            print(f"   DEAM entries: {len(deam_data)}")
            
            # Check if our test file exists in DEAM
            test_filename = os.path.basename(test_file)
            found = any(entry['filename'] == test_filename for entry in deam_data)
            print(f"   Test file in DEAM: {found}")
            
            # Check feature consistency
            if deam_data:
                sample_entry = deam_data[0]
                print(f"   Sample entry features: {len(sample_entry['features'])}")
                print(f"   Sample feature values: {sample_entry['features'][:5]}")
                
        except Exception as e:
            print(f"   DEAM features error: {e}")
        
    except Exception as e:
        print(f"Pipeline error: {e}")
        import traceback
        traceback.print_exc()

def test_recommendation_system():
    """Test the recommendation system specifically"""
    
    print("\n=== Recommendation System Test ===")
    
    try:
        # Load DEAM features
        with open("../../deam/features.json", "r") as f:
            deam_features = json.load(f)
        
        print(f"Loaded {len(deam_features)} DEAM features")
        
        # Test similarity calculation
        from recommender import similarity
        
        # Create test feature vector
        test_features = np.random.rand(15)
        
        # Test with a few DEAM entries
        similarities = []
        for i, entry in enumerate(deam_features[:10]):
            deam_feats = np.array(entry['features'])
            sim = similarity(test_features, deam_feats)
            similarities.append((entry['filename'], sim))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        print("Top 10 similarities:")
        for filename, sim in similarities:
            print(f"  {filename}: {sim:.3f}")
        
    except Exception as e:
        print(f"Recommendation test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_pipeline()
    test_recommendation_system()
