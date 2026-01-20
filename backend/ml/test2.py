import requests

# Test with another file
with open('../../deam/audio/1000.mp3', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    print(f'File: 1000.mp3')
    print(f'Mood: {result["mood"]}')
    print(f'Confidence: {result["confidence"]}')
    print(f'Probabilities: {result["probabilities"]}')
    print('Top 3 recommendations:')
    for i, rec in enumerate(result['recommendations'][:3]):
        print(f'  {i+1}. {rec["filename"]} - {rec["similarity"]}%')
