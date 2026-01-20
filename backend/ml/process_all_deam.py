import os
import json
import sys
import glob
from pathlib import Path
import time
import numpy as np

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio_features import extract_features

def process_all_deam_audio():
    """Process all MP3 files in deam/audio/ and extract features"""
    
    audio_dir = "../../deam/audio"
    features_file = "../../deam/features.json"
    
    print(f"Processing audio files from: {audio_dir}")
    print(f"Output features to: {features_file}")
    
    # Get all MP3 files
    mp3_files = glob.glob(os.path.join(audio_dir, "*.mp3"))
    total_files = len(mp3_files)
    
    print(f"Found {total_files} MP3 files to process")
    
    # Load existing features if file exists
    existing_features = []
    processed_filenames = set()
    
    if os.path.exists(features_file):
        try:
            with open(features_file, 'r') as f:
                existing_features = json.load(f)
                processed_filenames = {item['filename'] for item in existing_features}
                print(f"Loaded {len(existing_features)} existing features")
        except (json.JSONDecodeError, FileNotFoundError):
            print("Starting with empty features file")
            existing_features = []
    
    # Process each file
    new_features = []
    processed_count = 0
    error_count = 0
    
    for i, audio_path in enumerate(mp3_files):
        filename = os.path.basename(audio_path)
        
        # Skip if already processed
        if filename in processed_filenames:
            processed_count += 1
            if processed_count % 100 == 0:
                print(f"Skipped {processed_count} already processed files...")
            continue
        
        try:
            # Extract features
            features = extract_features(audio_path)
            
            # Create feature entry
            feature_entry = {
                "filename": filename,
                "features": features.flatten().tolist()
            }
            
            new_features.append(feature_entry)
            processed_count += 1
            
            # Progress update
            if processed_count % 50 == 0:
                progress = (processed_count / total_files) * 100
                print(f"Processed {processed_count}/{total_files} files ({progress:.1f}%)")
                
                # Save intermediate results
                all_features = existing_features + new_features
                with open(features_file, 'w') as f:
                    json.dump(all_features, f, indent=2)
                print(f"Saved intermediate results")
            
        except Exception as e:
            error_count += 1
            print(f"Error processing {filename}: {str(e)}")
            continue
    
    # Combine existing and new features
    all_features = existing_features + new_features
    
    # Save final results
    with open(features_file, 'w') as f:
        json.dump(all_features, f, indent=2)
    
    print(f"\nProcessing complete!")
    print(f"Total features in file: {len(all_features)}")
    print(f"Newly processed: {len(new_features)}")
    print(f"Errors: {error_count}")
    print(f"Features saved to: {features_file}")
    
    return all_features

if __name__ == "__main__":
    start_time = time.time()
    features = process_all_deam_audio()
    end_time = time.time()
    
    print(f"Total processing time: {end_time - start_time:.2f} seconds")
    print(f"Average time per file: {(end_time - start_time) / len(features):.2f} seconds")
