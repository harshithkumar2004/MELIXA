import requests
import os

# Test the increased happy probability (0.3 → 0.4)
test_files = ['2.mp3', '3.mp3', '4.mp3', '5.mp3', '10.mp3', '12.mp3', '13.mp3', '18.mp3', '20.mp3']

print('=== TESTING INCREASED HAPPY PROBABILITY ===')
print('Happy probability increased from 0.3 to 0.4 in moderate energy scenario...\n')

happy_predictions = []
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
                
                if mood == 'happy':
                    happy_predictions.append(filename)
                
                status = '*** HAPPY ***' if mood == 'happy' else 'Other'
                print(f'{filename}: {mood.upper()} ({confidence}% confidence) {status}')
                print(f'  Happy: {probabilities["happy"]:.3f}, Calm: {probabilities["calm"]:.3f}, Sad: {probabilities["sad"]:.3f}')
                
                # Check if happy probability increased
                happy_prob = probabilities['happy']
                if happy_prob > 0.35:
                    print(f'  HIGH happy probability: {happy_prob:.3f}')
                print()
                
        except Exception as e:
            print(f'Error processing {filename}: {e}')

print('=== HAPPY PROBABILITY RESULTS ===')
print(f'Files tested: {len(all_results)}')
print(f'Happy predictions: {len(happy_predictions)} - {happy_predictions}')

print('\n=== PROBABILITY ANALYSIS ===')
high_happy_probs = []
for result in all_results:
    happy_prob = result['probabilities']['happy']
    if happy_prob > 0.3:
        high_happy_probs.append((result['file'], happy_prob, result['mood']))

if high_happy_probs:
    print('Files with high happy probabilities (>0.3):')
    for file, prob, mood in sorted(high_happy_probs, key=lambda x: x[1], reverse=True):
        print(f'  {file}: {prob:.3f} (predicted: {mood})')
else:
    print('No files with happy probability > 0.3 found')

print('\n=== CHANGE SUMMARY ===')
print('HAPPY PROBABILITY INCREASED:')
print('- Moderate energy scenario: happy 0.3 → 0.4')
print('- This should increase happy predictions')
print('- Sad and calm behavior unchanged')
print()
print(' EXPECTED IMPACT:')
print('- More files should predict HAPPY')
print('- Moderate tempo + moderate energy = higher happy chance')
print('- Bright harmonic scenarios still at 0.4 happy')
print()
print('READY TO TEST:')
print('Upload moderate tempo, moderate energy audio for happy predictions!')
