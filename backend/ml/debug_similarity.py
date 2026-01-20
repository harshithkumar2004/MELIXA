import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import json
from audio_features import extract_features
from model_loader import enhanced_predict
from recommender import similarity, recommend

def debug_similarity():
    """Debug the similarity calculation issues"""
    
    print("=== Similarity Debug ===")
    
    # Load DEAM features
    with open("../../deam/features.json", "r") as f:
        deam_features = json.load(f)
    
    print(f"DEAM entries: {len(deam_features)}")
    
    # Test with a real audio file
    test_file = "../../deam/audio/10.mp3"
    features = extract_features(test_file)
    probs, scaled = enhanced_predict(features)
    
    print(f"Test features shape: {features.shape}")
    print(f"Scaled features shape: {scaled.shape}")
    print(f"Test features range: [{features.min():.3f}, {features.max():.3f}]")
    print(f"Scaled features range: [{scaled.min():.3f}, {scaled.max():.3f}]")
    
    # Test similarity with DEAM features
    test_vec = scaled.flatten()
    
    print(f"\nTesting similarity calculations:")
    
    for i, entry in enumerate(deam_features[:5]):
        deam_vec = np.array(entry['features'])
        
        # Calculate individual components
        from scipy.spatial.distance import cosine, euclidean
        
        cos_dist = cosine(test_vec, deam_vec)
        cos_sim = 1 - cos_dist
        
        euc_dist = euclidean(test_vec, deam_vec)
        euc_sim = 1 / (1 + euc_dist)
        
        combined_sim = (0.7 * cos_sim + 0.3 * euc_sim) * 100
        
        print(f"\n{entry['filename']}:")
        print(f"  Test range: [{test_vec.min():.3f}, {test_vec.max():.3f}]")
        print(f"  DEAM range: [{deam_vec.min():.3f}, {deam_vec.max():.3f}]")
        print(f"  Cosine distance: {cos_dist:.3f}")
        print(f"  Cosine similarity: {cos_sim:.3f}")
        print(f"  Euclidean distance: {euc_dist:.3f}")
        print(f"  Euclidean similarity: {euc_sim:.3f}")
        print(f"  Combined similarity: {combined_sim:.3f}")
    
    # Test the recommend function
    print(f"\n=== Testing Recommend Function ===")
    recommendations = recommend(test_vec)
    
    print(f"Number of recommendations: {len(recommendations)}")
    for i, rec in enumerate(recommendations):
        print(f"{i+1}. {rec['filename']} - {rec['similarity']}")

def fix_recommendation_system():
    """Fix the recommendation system issues"""
    
    print("\n=== Fixing Recommendation System ===")
    
    # The issue might be that we're using scaled features (which can be negative)
    # Let's try using the original features instead
    
    test_file = "../../deam/audio/10.mp3"
    features = extract_features(test_file)
    
    print(f"Original features range: [{features.min():.3f}, {features.max():.3f}]")
    
    # Test similarity with original features
    test_vec = features.flatten()
    
    with open("../../deam/features.json", "r") as f:
        deam_features = json.load(f)
    
    print(f"\nTesting with original features:")
    
    for i, entry in enumerate(deam_features[:3]):
        deam_vec = np.array(entry['features'])
        
        from scipy.spatial.distance import cosine, euclidean
        
        cos_dist = cosine(test_vec, deam_vec)
        cos_sim = 1 - cos_dist
        
        euc_dist = euclidean(test_vec, deam_vec)
        euc_sim = 1 / (1 + euc_dist)
        
        combined_sim = (0.7 * cos_sim + 0.3 * euc_sim) * 100
        
        print(f"{entry['filename']}: {combined_sim:.3f}")

if __name__ == "__main__":
    debug_similarity()
    fix_recommendation_system()
