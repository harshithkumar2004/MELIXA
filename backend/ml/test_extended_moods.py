import requests
import os

# Test more files to find happy and calm predictions
test_files = [
    '1.mp3', '2.mp3', '3.mp3', '4.mp3', '5.mp3', '6.mp3', '7.mp3', '8.mp3', '9.mp3',
    '11.mp3', '12.mp3', '13.mp3', '14.mp3', '15.mp3', '16.mp3', '17.mp3', '18.mp3', '19.mp3', '20.mp3'
]

print('=== Extended Mood Prediction Analysis ===')
print('Testing more files to find happy and calm predictions...\n')

happy_files = []
calm_files = []
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
                    happy_files.append(filename)
                elif mood == 'calm':
                    calm_files.append(filename)
                
                print(f'{filename}: {mood.upper()} ({confidence}% confidence)')
                if mood in ['happy', 'calm']:
                    print(f'  *** TARGET MOOD FOUND ***')
                    print(f'  Probabilities: {probabilities}')
                else:
                    print(f'  Happy prob: {probabilities["happy"]:.3f}, Calm prob: {probabilities["calm"]:.3f}')
                print()
                
        except Exception as e:
            print(f'Error processing {filename}: {e}')
    else:
        print(f'File not found: {filename}')

print('=== SUMMARY ===')
print(f'Total files tested: {len(all_results)}')
print(f'Happy predictions: {len(happy_files)} - {happy_files}')
print(f'Calm predictions: {len(calm_files)} - {calm_files}')

if happy_files or calm_files:
    print('\n=== TARGET MOOD FILES ANALYSIS ===')
    for filename in happy_files + calm_files:
        for result in all_results:
            if result['file'] == filename:
                print(f'{filename}:')
                print(f'  Mood: {result["mood"]}')
                print(f'  Confidence: {result["confidence"]}%')
                print(f'  Probabilities: {result["probabilities"]}')
                break
else:
    print('\n=== HIGHEST PROBABILITY ANALYSIS ===')
    print('Files with highest happy/calm probabilities:')
    
    happy_candidates = []
    calm_candidates = []
    
    for result in all_results:
        happy_prob = result['probabilities']['happy']
        calm_prob = result['probabilities']['calm']
        
        if happy_prob > 0.25:
            happy_candidates.append((result['file'], happy_prob, result['mood']))
        if calm_prob > 0.25:
            calm_candidates.append((result['file'], calm_prob, result['mood']))
    
    print('\nHAPPY CANDIDATES (probability > 25%):')
    for file, prob, mood in sorted(happy_candidates, key=lambda x: x[1], reverse=True):
        print(f'  {file}: {prob:.3f} (predicted: {mood})')
    
    print('\nCALM CANDIDATES (probability > 25%):')
    for file, prob, mood in sorted(calm_candidates, key=lambda x: x[1], reverse=True):
        print(f'  {file}: {prob:.3f} (predicted: {mood})')

print('\n=== AUDIO CHARACTERISTICS ANALYSIS ===')
print('To get HAPPY predictions:')
print('- Upload audio with: moderate-fast tempo (120-140 BPM)')
print('- Moderate energy levels (0.4-0.7)')
print('- Major key, upbeat melodies')
print('- Clear, bright instrumentation')
print()
print('To get CALM predictions:')
print('- Upload audio with: slow tempo (60-100 BPM)')
print('- Low energy levels (< 0.3)')
print('- Minor key, smooth melodies')
print('- Soft instrumentation, minimal percussion')
