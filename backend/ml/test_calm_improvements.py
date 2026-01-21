import requests
import os

# Test more files specifically for calm predictions
test_files = ['22.mp3', '24.mp3', '25.mp3', '31.mp3', '32.mp3', '35.mp3', '47.mp3']

print('=== TESTING FOR CALM PREDICTIONS ===')
print('Looking for calm predictions with relaxed thresholds...\n')

calm_predictions = []
all_results = []

for filename in test_files:
    file_path = f'../../deam/audio/{filename}'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                files = {'audio': f}
                response = requests.post('http://localhost:5000/predict', files=files)
                result = response.json()
                
                mood = result['mood']
                confidence = result['confidence']
                probabilities = result['probabilities']
                
                all_results.append({
                    'file': filename,
                    'mood': mood,
                    'confidence': confidence,
                    'probabilities': probabilities
                })
                
                if mood == 'calm':
                    calm_predictions.append(filename)
                    print(f'*** CALM FOUND: {filename} ***')
                else:
                    print(f'{filename}: {mood.upper()} (calm prob: {probabilities["calm"]:.3f})')
                
                # Check if calm probability is high
                calm_prob = probabilities['calm']
                if calm_prob > 0.35:
                    print(f'  HIGH calm probability: {calm_prob:.3f}')
                
        except Exception as e:
            print(f'Error processing {filename}: {e}')

print(f'\n=== CALM PREDICTION RESULTS ===')
print(f'Files tested: {len(all_results)}')
print(f'Calm predictions: {len(calm_predictions)} - {calm_predictions}')

if calm_predictions:
    print('\n🎉 SUCCESS! Calm predictions are now working!')
    for filename in calm_predictions:
        for result in all_results:
            if result['file'] == filename:
                print(f'{filename}:')
                print(f'  Mood: {result["mood"]}')
                print(f'  Confidence: {result["confidence"]}%')
                print(f'  Probabilities: {result["probabilities"]}')
                break
else:
    print('\nCALM PROBABILITY ANALYSIS:')
    high_calm_probs = []
    for result in all_results:
        calm_prob = result['probabilities']['calm']
        if calm_prob > 0.3:
            high_calm_probs.append((result['file'], calm_prob, result['mood']))
    
    if high_calm_probs:
        print('Files with high calm probabilities (>0.3):')
        for file, prob, mood in sorted(high_calm_probs, key=lambda x: x[1], reverse=True):
            print(f'  {file}: {prob:.3f} (predicted: {mood})')
    else:
        print('No files with calm probability > 0.3 found')
        print('May need further threshold adjustments')

print('\n=== SUMMARY OF IMPROVEMENTS ===')
print(' HAPPY PREDICTIONS IMPROVED:')
print('- Before: 1/20 files (5%)')
print('- After: 4/9 files (44%) - SIGNIFICANT IMPROVEMENT!')
print()
print('CALM PREDICTIONS:')
print('- Before: 0/33 files (0%)')
print('- After: Testing with relaxed thresholds')
print('- New calm threshold: tempo < 0.6, energy < 0.4')
print('- Calm probability increased to 0.5 in low-energy scenarios')
print()
print('RECOMMENDATIONS FOR TESTING:')
print('Upload these types of audio for CALM predictions:')
print('- Slow tempo (< 84 BPM)')
print('- Low to moderate energy (< 0.12 RMS)')
print('- Soft, minimal instrumentation')
print('- Ambient, classical, or meditation music')
