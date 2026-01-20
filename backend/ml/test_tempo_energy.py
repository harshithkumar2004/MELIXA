import requests

# Test the tempo and energy analysis fix
with open('../../deam/audio/10.mp3', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    print('=== MELIXA API Response ===')
    print(f'Mood: {result["mood"]}')
    print(f'Confidence: {result["confidence"]}')
    print(f'Probabilities: {result["probabilities"]}')
    
    # Check if processing info exists
    if 'processing_info' in result:
        print(f'Processing Info: {result["processing_info"]}')
    else:
        print('No processing info in response')
    
    print('\n=== Tempo & Energy Estimation Logic ===')
    mood = result["mood"].lower()
    if mood == 'energetic':
        tempo_range = "135-160 BPM"
        energy_range = "70-95%"
    elif mood == 'happy':
        tempo_range = "115-140 BPM"
        energy_range = "60-85%"
    elif mood == 'calm':
        tempo_range = "70-100 BPM"
        energy_range = "20-50%"
    elif mood == 'sad':
        tempo_range = "60-90 BPM"
        energy_range = "10-40%"
    else:
        tempo_range = "120 BPM (default)"
        energy_range = "50% (default)"
    
    print(f'For mood "{mood}":')
    print(f'  Estimated Tempo: {tempo_range}')
    print(f'  Estimated Energy: {energy_range}')
