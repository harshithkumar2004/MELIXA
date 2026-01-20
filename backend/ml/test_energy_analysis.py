import requests

# Test the energy analysis functionality
with open('../../deam/audio/10.mp3', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    print('=== Energy Analysis Test ===')
    print(f'Mood: {result["mood"]}')
    print(f'Confidence: {result["confidence"]}')
    
    print('\n=== Processing Info ===')
    if 'processing_info' in result:
        print(f'Tempo: {result["processing_info"]["tempo"]}')
        print(f'Energy: {result["processing_info"]["energy"]}')
        print(f'Energy Type: {type(result["processing_info"]["energy"])}')
    else:
        print('No processing_info found')
    
    print('\n=== Frontend Energy Display ===')
    if 'processing_info' in result:
        energy = result["processing_info"]["energy"]
        energy_percent = energy * 100
        energy_analysis = f"{energy_percent:.1f}% - {'High energy detected, suggesting upbeat mood' if energy > 0.5 else 'Low energy detected, suggesting calm mood'}"
        print(f'Energy Value: {energy}')
        print(f'Energy %: {energy_percent:.1f}%')
        print(f'Energy Analysis: {energy_analysis}')
        print(f'Energy > 0.5: {energy > 0.5}')
    else:
        print('Energy analysis not available')
    
    print('\n=== Expected Frontend Display ===')
    print('✅ Energy Analysis Box should show:')
    print('✅ Energy percentage (e.g., "11.5%")')
    print('✅ Analysis text based on energy level')
    print('✅ "High energy" if > 0.5, "Low energy" if ≤ 0.5')
