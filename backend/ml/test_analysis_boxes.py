import requests
import json

# Test a few audio files to check tempo/energy analysis
test_files = ['2.mp3', '3.mp3', '4.mp3', '5.mp3', '10.mp3']

print('🔍 TEMPO & ENERGY ANALYSIS VALIDATION')
print('=' * 50)

for filename in test_files:
    try:
        with open(f'../../deam/audio/{filename}', 'rb') as f:
            files = {'audio': f}
            response = requests.post('http://localhost:5000/predict', files=files)
            result = response.json()
            
            mood = result['mood']
            confidence = result['confidence']
            tempo = result['processing_info']['tempo']
            energy = result['processing_info']['energy']
            
            print(f'\n📁 {filename}:')
            print(f'   Mood: {mood.upper()} ({confidence}% confidence)')
            print(f'   Tempo: {tempo:.1f} BPM')
            print(f'   Energy: {energy:.4f} ({energy*100:.1f}%)')
            
            # Check if analysis matches mood expectations
            tempo_analysis = 'Slow' if tempo < 120 else 'Upbeat'
            energy_analysis = 'Low' if energy <= 0.5 else 'High'
            
            print(f'   Tempo Analysis: {tempo_analysis} ({tempo:.1f} BPM)')
            print(f'   Energy Analysis: {energy_analysis} ({energy*100:.1f}%)')
            
            # Validate against mood expectations
            mood_tempo_match = False
            mood_energy_match = False
            
            if mood in ['calm', 'sad']:
                # Should have slow tempo and low energy
                mood_tempo_match = tempo < 120
                mood_energy_match = energy <= 0.5
            elif mood in ['energetic', 'happy']:
                # Should have upbeat tempo and/or high energy
                mood_tempo_match = tempo >= 120
                mood_energy_match = energy > 0.5
            
            tempo_status = '✅' if mood_tempo_match else '❌'
            energy_status = '✅' if mood_energy_match else '❌'
            
            print(f'   Tempo-Mood Match: {tempo_status}')
            print(f'   Energy-Mood Match: {energy_status}')
            
            # Check frontend display logic
            frontend_tempo_text = 'Slow tempo detected, indicating calm or melancholic mood' if tempo < 120 else 'Upbeat tempo detected, indicating energetic or happy mood'
            frontend_energy_text = 'Low energy detected, suggesting calm mood' if energy <= 0.5 else 'High energy detected, suggesting upbeat mood'
            
            print(f'   Frontend Tempo: {frontend_tempo_text}')
            print(f'   Frontend Energy: {frontend_energy_text}')
            
    except Exception as e:
        print(f'❌ Error processing {filename}: {e}')

print('\n' + '=' * 50)
print('📊 ANALYSIS THRESHOLDS USED:')
print('Tempo: < 120 BPM = Slow, >= 120 BPM = Upbeat')
print('Energy: <= 0.5 = Low, > 0.5 = High')
print()
print('🎯 EXPECTED MOOD-ANALYSIS CORRELATIONS:')
print('Calm/Sad: Slow tempo + Low energy')
print('Energetic/Happy: Upbeat tempo + High energy')
