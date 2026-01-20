import requests

# Test the debug version of probability bars
with open('../../deam/audio/10.mp3', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    print('=== DEBUG TEST ===')
    print(f'Upload successful: {response.status_code}')
    print(f'Mood: {result["mood"]}')
    print(f'Probabilities: {result["probabilities"]}')
    
    print('\n=== Frontend Should Show ===')
    print('✅ RED DEBUG BOX with probabilities object')
    print('✅ YELLOW PROBABILITY ITEMS')
    print('✅ BLUE BARS with GREEN FILLS')
    print('✅ DEBUG TEXT inside bars showing percentage')
    
    print('\n=== If you see this in the browser, the bars are working! ===')
