import requests

# Test the complete tempo and energy analysis integration
with open('../../deam/audio/10.mp3', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    print('=== Complete Integration Test ===')
    print(f'Mood: {result["mood"]}')
    print(f'Confidence: {result["confidence"]}')
    print(f'Tempo: {result["processing_info"]["tempo"]:.1f} BPM')
    print(f'Energy: {result["processing_info"]["energy"]:.3f}')
    print(f'Energy %: {result["processing_info"]["energy"] * 100:.1f}%')
    
    print('\n=== Frontend Display Values ===')
    tempo = result["processing_info"]["tempo"]
    energy = result["processing_info"]["energy"]
    
    tempo_analysis = f"{tempo:.1f} BPM - {'Slow tempo detected, indicating calm or melancholic mood' if tempo < 120 else 'Upbeat tempo detected, indicating energetic or happy mood'}"
    energy_analysis = f"{energy * 100:.1f}% - {'High energy detected, suggesting upbeat mood' if energy > 0.5 else 'Low energy detected, suggesting calm mood'}"
    
    print(f'Tempo Analysis: {tempo_analysis}')
    print(f'Energy Analysis: {energy_analysis}')
    
    print('\n=== All Probabilities ===')
    for mood, prob in result["probabilities"].items():
        print(f'{mood}: {prob * 100:.1f}%')
    
    print(f'\n=== Recommendations ===')
    print(f'Number of recommendations: {len(result["recommendations"])}')
    for i, rec in enumerate(result["recommendations"][:3]):
        print(f'{i+1}. {rec["filename"]} - {rec["similarity"]}%')
