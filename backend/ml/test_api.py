import requests
import json

def test_api_prediction():
    """Test the actual API prediction endpoint"""
    
    print("=== API Prediction Test ===")
    
    # Test with a real audio file
    test_file = "../../deam/audio/10.mp3"
    
    try:
        with open(test_file, 'rb') as f:
            files = {'audio': f}
            response = requests.post('http://localhost:8000/predict', files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction successful!")
            print(f"Mood: {result['mood']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Probabilities: {result['probabilities']}")
            print(f"Number of recommendations: {len(result['recommendations'])}")
            
            print("\nTop 5 recommendations:")
            for i, rec in enumerate(result['recommendations']):
                print(f"{i+1}. {rec['filename']} - Similarity: {rec['similarity']}")
            
        else:
            print(f"API error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Test failed: {e}")

def test_api_gateway():
    """Test the API gateway"""
    
    print("\n=== API Gateway Test ===")
    
    test_file = "../../deam/audio/10.mp3"
    
    try:
        with open(test_file, 'rb') as f:
            files = {'audio': f}
            response = requests.post('http://localhost:5000/predict', files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"Gateway prediction successful!")
            print(f"Mood: {result['mood']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Number of recommendations: {len(result['recommendations'])}")
            
            print("\nTop 3 recommendations:")
            for i, rec in enumerate(result['recommendations'][:3]):
                print(f"{i+1}. {rec['filename']} - Similarity: {rec['similarity']}")
            
        else:
            print(f"Gateway error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Gateway test failed: {e}")

if __name__ == "__main__":
    test_api_prediction()
    test_api_gateway()
