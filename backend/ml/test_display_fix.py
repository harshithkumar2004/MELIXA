import requests
import json

# Test one file to verify the fix
test_file = '2.mp3'

print('🔧 TESTING FIXED DISPLAY')
print('=' * 40)

try:
    with open(f'../../deam/audio/{test_file}', 'rb') as f:
        files = {'audio': f}
        response = requests.post('http://localhost:5000/predict', files=files)
        result = response.json()
        
        mood = result['mood']
        tempo = result['processing_info']['tempo']
        energy = result['processing_info']['energy']
        
        print(f'File: {test_file}')
        print(f'Mood: {mood.upper()}')
        print(f'Tempo: {tempo:.1f} BPM')
        print(f'Energy: {energy:.4f} ({energy*100:.1f}%)')
        
        # Test frontend logic
        tempo_analysis = 'Slow tempo detected, indicating calm or melancholic mood' if tempo < 120 else 'Upbeat tempo detected, indicating energetic or happy mood'
        energy_analysis = 'Low energy detected, suggesting calm mood' if energy <= 0.15 else 'High energy detected, suggesting upbeat mood'
        
        print(f'\n🎨 FRONTEND SHOULD DISPLAY:')
        print(f'Tempo Analysis: {tempo:.1f} BPM - {tempo_analysis}')
        print(f'Energy Analysis: {energy*100:.1f}% - {energy_analysis}')
        
        # Check if analysis matches mood
        print(f'\n ANALYSIS ACCURACY:')
        if mood in ['energetic', 'happy']:
            expected_tempo = 'Upbeat'
            expected_energy = 'High'
        else:
            expected_tempo = 'Slow'
            expected_energy = 'Low'
            
        actual_tempo = 'Upbeat' if tempo >= 120 else 'Slow'
        actual_energy = 'High' if energy > 0.15 else 'Low'
        
        tempo_match = '✅' if actual_tempo == expected_tempo else '❌'
        energy_match = '✅' if actual_energy == expected_energy else '❌'
        
        print(f'Tempo Match: {tempo_match} ({actual_tempo} vs {expected_tempo})')
        print(f'Energy Match: {energy_match} ({actual_energy} vs {expected_energy})')
        
except Exception as e:
    print(f'❌ Error: {e}')

print('\n EXPECTED FRONTEND DISPLAY:')
print('Real tempo and energy values')
print(' Correct tempo analysis based on 120 BPM threshold')
print(' Correct energy analysis based on 15% threshold')
print(' Proper data path: moodData.processing_info.tempo')
