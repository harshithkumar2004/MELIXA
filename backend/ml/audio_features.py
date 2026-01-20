import librosa
import numpy as np

SR = 22050

def extract_features(path):
    y, sr = librosa.load(path, sr=SR, mono=True)
    
    # Apply high-quality audio preprocessing
    # Remove DC offset and apply gentle high-pass filter
    y = librosa.util.normalize(y)
    
    # Extract features with improved parameters
    # Tempo with more accurate estimation
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=512, trim=False)
    
    # RMS energy with better temporal resolution
    rms = librosa.feature.rms(y=y, hop_length=512, frame_length=2048)
    
    # Spectral features with improved frequency resolution
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=512, n_fft=2048)
    zcr = librosa.feature.zero_crossing_rate(y=y, hop_length=512, frame_length=2048)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=512, n_fft=2048, roll_percent=0.85)
    
    # MFCC with better frequency resolution
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=2048, hop_length=512, n_mels=128)
    
    # Chroma features with enhanced resolution
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=512, n_fft=2048)
    
    # Onset strength with better sensitivity
    onset = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512, n_fft=2048)
    
    # Spectral contrast with more frequency bands
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=512, n_fft=2048, n_bands=6)
    
    # Extract exactly 15 features in the specified order with improved statistics
    features = [
        np.mean(tempo),                    # feature_0: tempo_mean
        np.mean(rms),                      # feature_1: energy_rms_mean
        np.mean(centroid),                 # feature_2: spectral_centroid_mean
        np.mean(zcr),                      # feature_3: zero_crossing_rate_mean
        np.mean(rolloff),                  # feature_4: spectral_rolloff_mean
        np.mean(mfcc[1]),                  # feature_5: mfcc_1_mean (2nd MFCC)
        np.mean(mfcc[2]),                  # feature_6: mfcc_2_mean (3rd MFCC)
        np.mean(chroma),                   # feature_7: chroma_mean
        np.mean(onset),                    # feature_8: onset_strength_mean
        np.mean(contrast),                 # feature_9: spectral_contrast_mean
        np.std(tempo),                     # feature_10: tempo_std
        np.std(rms),                       # feature_11: energy_rms_std
        np.std(rolloff),                   # feature_12: spectral_rolloff_std
        np.std(chroma),                    # feature_13: chroma_std
        np.std(onset)                      # feature_14: onset_strength_std
    ]
    
    features_array = np.array(features, dtype=np.float32)
    
    # Apply feature stability checks
    if len(features_array) != 15:
        raise ValueError(f"Expected 15 features, got {len(features_array)}")
    
    # Check for NaN or infinite values
    if np.any(~np.isfinite(features_array)):
        # Replace NaN/inf with median values
        for i in range(len(features_array)):
            if not np.isfinite(features_array[i]):
                features_array[i] = 0.0  # Default fallback
    
    return features_array.reshape(1, -1)
