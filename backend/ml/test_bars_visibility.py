import requests

# Test the mood probability bars visibility
with open('../../deam/audio/10.mp3', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    print('=== Mood Probability Bars Test ===')
    print(f'Mood: {result["mood"]}')
    print(f'Confidence: {result["confidence"]}')
    
    print('\n=== Probability Values for Bars ===')
    for mood, prob in result["probabilities"].items():
        percentage = prob * 100
        bar_width = int(percentage)  # Simulate bar width
        bar_visual = '█' * (bar_width // 5) + '░' * (20 - bar_width // 5)
        print(f'{mood.upper():10}: {percentage:5.1f}% |{bar_visual}|')
    
    print(f'\n=== Frontend Bar Properties ===')
    print(f'Bar Height: 20px (increased for visibility)')
    print(f'Bar Border: 2px solid rgba(139, 69, 19, 0.4)')
    print(f'Bar Fill: Gold gradient with shimmer effect')
    print(f'Minimum Width: 4px (ensures visibility)')
    print(f'Animation: 1.2s cubic-bezier transition')
    
    print('\n=== Expected Visual ===')
    print('✅ Bars should be visible with gold gradient fill')
    print('✅ Bars should have shimmer animation')
    print('✅ Container should have gold/brown theme')
    print('✅ Hover effects on individual mood items')
