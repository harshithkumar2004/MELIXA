import requests

# Simple test to verify bars are working
with open('../../deam/audio/10.mp3', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    print('=== DEBUG: Probability Bars ===')
    print(f'Probabilities object: {result["probabilities"]}')
    print(f'Type: {type(result["probabilities"])}')
    
    print('\n=== Individual Probabilities ===')
    for mood, prob in result["probabilities"].items():
        print(f'{mood}: {prob} (type: {type(prob)})')
        print(f'  Percentage: {prob * 100}%')
        print(f'  Bar width: {prob * 100}%')
    
    print('\n=== Expected Frontend Display ===')
    print('✅ Container: .mood-probabilities')
    print('✅ Items: .probability-item')
    print('✅ Labels: .probability-label')
    print('✅ Bars: .probability-bar')
    print('✅ Fills: .probability-fill')
    print('✅ Height: 24px')
    print('✅ Background: #e8dcc4')
    print('✅ Fill: #D4AF37')
    print('✅ Border: 2px solid #8b4513')
    print('✅ Min width: 5px')
    print('✅ Display: block !important')
    
    print('\n=== Test Values ===')
    test_prob = 0.293
    print(f'Test probability: {test_prob}')
    print(f'Test percentage: {test_prob * 100}%')
    print(f'Test bar width: {test_prob * 100}%')
    print(f'Test bar should be: 29.3% wide, 24px tall')
