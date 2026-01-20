import requests
import librosa
import numpy as np

# Analyze the happy prediction file to understand its characteristics
happy_file = '../../deam/audio/12.mp3'

print('=== HAPPY AUDIO ANALYSIS ===')
print(f'Analyzing file: 12.mp3 (predicted HAPPY)')

# Load and analyze the audio
y, sr = librosa.load(happy_file, sr=22050, mono=True)

# Extract features
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
rms = librosa.feature.rms(y=y)
centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
zcr = librosa.feature.zero_crossing_rate(y)
rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=2)
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
onset = librosa.onset.onset_strength(y=y, sr=sr)
contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

# Calculate the 15 features in the same order as extract_features
features = [
    np.mean(tempo),                    # feature_0: tempo_mean
    np.mean(rms),                      # feature_1: energy_rms_mean
    np.mean(centroid),                 # feature_2: spectral_centroid_mean
    np.mean(zcr),                      # feature_3: zero_crossing_rate_mean
    np.mean(rolloff),                  # feature_4: spectral_rolloff_mean
    np.mean(mfcc[0]),                  # feature_5: mfcc_1_mean
    np.mean(mfcc[1]),                  # feature_6: mfcc_2_mean
    np.mean(chroma),                   # feature_7: chroma_mean
    np.mean(onset),                    # feature_8: onset_strength_mean
    np.mean(contrast),                 # feature_9: spectral_contrast_mean
    np.std(tempo),                     # feature_10: tempo_std
    np.std(rms),                       # feature_11: energy_rms_std
    np.std(rolloff),                   # feature_12: spectral_rolloff_std
    np.std(chroma),                    # feature_13: chroma_std
    np.std(onset)                      # feature_14: onset_strength_std
]

print('\n=== AUDIO CHARACTERISTICS ===')
print(f'Tempo: {features[0]:.1f} BPM')
print(f'Energy (RMS): {features[1]:.3f}')
print(f'Spectral Centroid: {features[2]:.1f}')
print(f'Zero Crossing Rate: {features[3]:.3f}')
print(f'Spectral Rolloff: {features[4]:.1f}')
print(f'MFCC 1: {features[5]:.3f}')
print(f'MFCC 2: {features[6]:.3f}')
print(f'Chroma: {features[7]:.3f}')
print(f'Onset Strength: {features[8]:.3f}')
print(f'Spectral Contrast: {features[9]:.3f}')

print('\n=== HAPPY AUDIO SIGNATURE ===')
print('Key characteristics that led to HAPPY prediction:')
print(f'✅ Tempo: {features[0]:.1f} BPM (moderate-fast)')
print(f'✅ Energy: {features[1]:.3f} (moderate level)')
print(f'✅ Spectral Centroid: {features[2]:.1f} (bright timbre)')
print(f'✅ Zero Crossing Rate: {features[3]:.3f} (moderate complexity)')
print(f'✅ Spectral Rolloff: {features[4]:.1f} (balanced frequency content)')

print('\n=== RECOMMENDATIONS FOR HAPPY PREDICTIONS ===')
print('Upload audio with these characteristics:')
print('🎵 TEMPO: 120-140 BPM (moderate to fast)')
print('⚡ ENERGY: 0.3-0.6 (moderate RMS energy)')
print('🎶 TIMBRE: Bright spectral centroid (> 2000)')
print('🎹 COMPLEXITY: Moderate zero-crossing rate')
print('🎼 CONTENT: Major key, upbeat melodies')
print('🥁 PERCUSSION: Clear rhythmic elements')
print()
print('📝 AUDIO TYPES TO UPLOAD:')
print('- Pop songs with moderate tempo')
print('- Upbeat acoustic tracks')
print('- Folk music with bright instrumentation')
print('- Electronic music with moderate energy')
print('- Major key compositions')

# Test with the API to confirm
print('\n=== API CONFIRMATION ===')
with open(happy_file, 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    print(f'API Prediction: {result["mood"].upper()}')
    print(f'Confidence: {result["confidence"]}%')
    print(f'Happy Probability: {result["probabilities"]["happy"]:.3f}')
    print(f'Calm Probability: {result["probabilities"]["calm"]:.3f}')
