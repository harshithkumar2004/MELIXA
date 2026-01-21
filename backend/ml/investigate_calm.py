import requests
import os
import numpy as np

# Deep dive into why calm predictions are not found
print('CALM PREDICTION INVESTIGATION ')

# First, let's check the model's prediction patterns
test_files = []
for i in range(1, 51):  # Test files 1-50
    filename = f'{i}.mp3'
    file_path = f'../../deam/audio/{filename}'
    if os.path.exists(file_path):
        test_files.append(filename)

print(f'Testing {len(test_files)} files for calm predictions...\n')

calm_predictions = []
all_probabilities = []
mood_counts = {'calm': 0, 'energetic': 0, 'happy': 0, 'sad': 0}

for filename in test_files[:20]:  # Test first 20 files
    try:
        with open(f'../../deam/audio/{filename}', 'rb') as f:
            files = {'audio': f}
            response = requests.post('http://localhost:5000/predict', files=files)
            result = response.json()
            
            mood = result['mood']
            probabilities = result['probabilities']
            
            mood_counts[mood] += 1
            all_probabilities.append(probabilities['calm'])
            
            if mood == 'calm':
                calm_predictions.append(filename)
                print(f'*** CALM FOUND: {filename} ***')
            else:
                print(f'{filename}: {mood.upper()} (calm prob: {probabilities["calm"]:.3f})')
            
    except Exception as e:
        print(f'Error with {filename}: {e}')

print(f'\n MOOD DISTRIBUTION ')
for mood, count in mood_counts.items():
    percentage = (count / 20) * 100
    print(f'{mood}: {count}/20 ({percentage:.1f}%)')

print(f'\n=== CALM PROBABILITY ANALYSIS ===')
if all_probabilities:
    print(f'Max calm probability: {max(all_probabilities):.3f}')
    print(f'Min calm probability: {min(all_probabilities):.3f}')
    print(f'Average calm probability: {np.mean(all_probabilities):.3f}')
    print(f'Calm probability > 0.3: {sum(1 for p in all_probabilities if p > 0.3)} files')
    print(f'Calm probability > 0.4: {sum(1 for p in all_probabilities if p > 0.4)} files')

# Let's check the model's bias by looking at class labels and prediction strategy
print(f'\n MODEL ANALYSIS ')
print('Checking model prediction patterns...')

# Test with a few more files to see pattern
for filename in test_files[20:30]:
    try:
        with open(f'../../deam/audio/{filename}', 'rb') as f:
            files = {'audio': f}
            response = requests.post('http://localhost:5000/predict', files=files)
            result = response.json()
            
            mood = result['mood']
            probabilities = result['probabilities']
            calm_prob = probabilities['calm']
            
            if calm_prob > 0.25:  # High calm probability threshold
                print(f'{filename}: {mood.upper()} (HIGH calm prob: {calm_prob:.3f})')
            
    except Exception as e:
        print(f'Error with {filename}: {e}')

print(f'\n=== CALM PREDICTION REQUIREMENTS ===')
print('Based on the analysis, calm predictions require:')
print('1. Calm probability > other probabilities')
print('2. Calm probability > 0.3-0.4 threshold')
print('3. Model confidence in calm prediction')
print()
print('The model may be biased towards other moods due to:')
print('- Training data imbalance')
print('- Feature weighting in the model')
print('- Prediction confidence thresholds')

# Let's create a synthetic test to see what would trigger calm
print(f'\n FEATURE ANALYSIS FOR CALM ')
print('Typical calm audio characteristics:')
print('- Low tempo (< 100 BPM)')
print('- Low energy (< 0.2 RMS)')
print('- Low spectral centroid (< 1800 Hz)')
print('- Low zero-crossing rate')
print('- Smooth spectral characteristics')
print()
print('The model might need:')
print('- More calm training examples')
print('- Adjusted confidence thresholds')
print('- Different feature weighting for calm detection')
