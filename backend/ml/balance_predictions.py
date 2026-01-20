import json
import numpy as np
from collections import Counter

def analyze_deam_labels():
    """Analyze the actual mood distribution in DEAM dataset if available"""
    
    # Since we don't have the original labels, let's create a balanced prediction approach
    print("=== Creating Balanced Prediction Strategy ===")
    
    # Load features to understand the distribution
    with open("../../deam/features.json", "r") as f:
        deam_features = json.load(f)
    
    print(f"Total DEAM samples: {len(deam_features)}")
    
    # Analyze feature distribution
    all_features = np.array([entry['features'] for entry in deam_features])
    
    # Create clusters based on feature similarity to estimate mood distribution
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    # Normalize features
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(all_features)
    
    # Create 4 clusters (for 4 moods)
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(normalized_features)
    
    cluster_counts = Counter(clusters)
    print(f"Cluster distribution: {dict(cluster_counts)}")
    
    # Map clusters to moods based on feature characteristics
    cluster_centers = kmeans.cluster_centers_
    
    mood_mapping = {}
    for i, center in enumerate(cluster_centers):
        # Analyze cluster characteristics
        tempo = center[0]  # tempo feature
        energy = center[1]  # energy feature
        
        if tempo > 0.5 and energy > 0.5:
            mood = "energetic"
        elif tempo > 0 and energy > 0:
            mood = "happy"
        elif tempo < 0 and energy < 0:
            mood = "sad"
        else:
            mood = "calm"
        
        mood_mapping[i] = mood
        print(f"Cluster {i}: {mood} (tempo={tempo:.2f}, energy={energy:.2f})")
    
    return mood_mapping, cluster_centers, scaler

def create_balanced_predictor():
    """Create a more balanced prediction function"""
    
    mood_mapping, cluster_centers, feature_scaler = analyze_deam_labels()
    
    print(f"\n=== Balanced Prediction Strategy ===")
    print(f"Mood mapping: {mood_mapping}")
    
    return mood_mapping, cluster_centers, feature_scaler

if __name__ == "__main__":
    create_balanced_predictor()
