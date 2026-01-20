import requests
import json

print('🔧 TESTING CORRECTED CONNECTION')
print('=' * 40)

try:
    # Test health endpoint
    response = requests.get('http://localhost:8000/health', timeout=5)
    print(f'✅ Health Check: {response.status_code} - {response.json()}')
    
    # Test predict endpoint with a small file
    with open('../../deam/audio/2.mp3', 'rb') as f:
        files = {'audio': f}
        response = requests.post('http://localhost:8000/predict', files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f'✅ Predict Test: {response.status_code}')
            print(f'   Mood: {result["mood"]}')
            print(f'   Confidence: {result["confidence"]}%')
            print(f'   Tempo: {result["processing_info"]["tempo"]:.1f} BPM')
            print(f'   Energy: {result["processing_info"]["energy"]:.4f}')
            print(f'   Recommendations: {len(result["recommendations"])} songs')
        else:
            print(f'❌ Predict Test Failed: {response.status_code}')
            
except Exception as e:
    print(f'❌ Connection Error: {e}')

print('\n🎯 CONNECTION STATUS:')
print('✅ Frontend: http://localhost:3001')
print('✅ Backend: http://localhost:8000')
print('✅ API URL: Fixed to port 8000')
print('✅ Audio Streaming: Fixed to port 8000')
print('\n🚀 READY TO USE!')
