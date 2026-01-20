import requests
import os

# Test multiple audio files to see which moods they predict
test_files = [
    '10.mp3', '100.mp3', '1000.mp3', '1001.mp3', '1002.mp3',
    '1003.mp3', '1004.mp3', '1005.mp3', '1006.mp3', '1007.mp3'
]

print('=== Mood Prediction Analysis ===')
print('Testing multiple files to find happy and calm predictions...\n')

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
                print(f'  Probabilities: {probabilities}')
                print()
                
        except Exception as e:
            print(f'Error processing {filename}: {e}')
    else:
        print(f'File not found: {filename}')

print('=== SUMMARY ===')
print(f'Total files tested: {len(all_results)}')
print(f'Happy predictions: {len(happy_files)} - {happy_files}')
print(f'Calm predictions: {len(calm_files)} - {calm_files}')

print('\n=== HAPPY FILES ANALYSIS ===')
if happy_files:
    for filename in happy_files:
        for result in all_results:
            if result['file'] == filename:
                print(f'{filename}:')
                print(f'  Mood: {result["mood"]}')
                print(f'  Confidence: {result["confidence"]}%')
                print(f'  Happy probability: {result["probabilities"]["happy"]:.3f}')
                print(f'  Other probabilities: {result["probabilities"]}')
                break
else:
    print('No happy predictions found')

print('\n=== CALM FILES ANALYSIS ===')
if calm_files:
    for filename in calm_files:
        for result in all_results:
            if result['file'] == filename:
                print(f'{filename}:')
                print(f'  Mood: {result["mood"]}')
                print(f'  Confidence: {result["confidence"]}%')
                print(f'  Calm probability: {result["probabilities"]["calm"]:.3f}')
                print(f'  Other probabilities: {result["probabilities"]}')
                break
else:
    print('No calm predictions found')

print('\n=== RECOMMENDATIONS FOR HAPPY/CLAM AUDIO ===')
print('Based on the analysis, to get HAPPY predictions:')
print('- Look for audio with: higher tempo, moderate energy')
print('- Features: tempo > 120, energy 0.4-0.7')
print()
print('To get CALM predictions:')
print('- Look for audio with: lower tempo, lower energy') 
print('- Features: tempo < 100, energy < 0.3')
