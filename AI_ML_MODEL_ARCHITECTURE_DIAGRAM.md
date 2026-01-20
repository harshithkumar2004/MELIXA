# SmartPlay AI/ML Model Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           SMARTPLAY AI/ML ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   AUDIO     │    │  FEATURE    │    │   ML MODEL  │    │  OUTPUT     │      │
│  │   INPUT     │───►│ EXTRACTION  │───►│ PIPELINE    │───►│ LAYER       │      │
│  │             │    │             │    │             │    │             │      │
│  │ • MP3/WAV   │    │ • 15 Acoustic│    │ • Ensemble   │    │ • Mood      │      │
│  │ • 30s clips │    │   Features  │    │ • Heuristics│    │ • Confidence│      │
│  │ • Upload    │    │ • Scaling   │    │ • Weighting  │    │ • Recommendations│   │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Detailed ML Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            ML PIPELINE ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   AUDIO     │    │  FEATURE    │    │   ENSEMBLE  │    │  ENHANCED   │      │
│  │  PROCESSING │───►│ ENGINEERING │───►│   MODEL     │───►│ PREDICTION  │      │
│  │             │    │             │    │             │    │             │      │
│  │ • Librosa   │    │ • Tempo     │    │ • Gradient  │    │ • Dynamic   │      │
│  │ • 30s window│    │ • Energy    │    │   Boosting  │    │   Weighting  │      │
│  │ • 44.1kHz    │    │ • Spectral  │    │ • Logistic  │    │ • Temp      │      │
│  │ • Mono       │    │ • MFCCs     │    │   Regression│    │   Calibration│      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Feature Extraction Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        FEATURE EXTRACTION ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   AUDIO     │    │  TEMPORAL   │    │  SPECTRAL   │    │   TIMBRAL   │      │
│  │   LOADING   │───►│ FEATURES   │───►│ FEATURES   │───►│ FEATURES   │      │
│  │             │    │             │    │             │    │             │      │
│  │ • librosa   │    │ • Tempo     │    │ • Spectral  │    │ • MFCCs     │      │
│  │ • 30s clip  │    │ • RMS Energy│    │   Centroid  │    │ • 10 Coeffs │      │
│  │ • 44.1kHz    │    │ • ZCR       │    │ • Bandwidth │    │ • Mel Scale │      │
│  │ • Mono       │    │             │    │ • Rolloff   │    │             │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│                                      │                                           │
│                                      ▼                                           │
│                            ┌─────────────┐                                     │
│                            │   FEATURE   │                                     │
│                            │  VECTOR     │                                     │
│                            │             │                                     │
│                            │ [15 Features]│                                     │
│                            │ • Tempo     │                                     │
│                            │ • Energy    │                                     │
│                            │ • Spectral  │                                     │
│                            │ • MFCCs     │                                     │
│                            └─────────────┘                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Ensemble Model Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          ENSEMBLE MODEL ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   INPUT     │    │  GRADIENT   │    │  LOGISTIC   │    │   VOTING    │      │
│  │  FEATURES   │───►│  BOOSTING   │───►│ REGRESSION  │───►│ CLASSIFIER  │      │
│  │             │    │             │    │             │    │             │      │
│  │ • 15 Features│    │ • 100 Trees │    │ • L2 Reg    │    │ • Soft      │      │
│  │ • Normalized│    │ • Max Depth │    │ • Multi-class│    │   Voting    │      │
│  │ • Scaled    │    │ • Learning  │    │ • Coeffs    │    │ • Weighted   │      │
│  │             │    │   Rate     │    │             │    │ • Prob      │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│                                      │                                           │
│                                      ▼                                           │
│                            ┌─────────────┐                                     │
│                            │   MODEL     │                                     │
│                            │ PROBABILITIES│                                     │
│                            │             │                                     │
│                            │ [P1, P2, P3, P4]│                                 │
│                            │ • Calm      │                                     │
│                            │ • Energetic │                                     │
│                            │ • Happy     │                                     │
│                            │ • Sad       │                                     │
│                            └─────────────┘                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Enhanced Prediction Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                      ENHANCED PREDICTION ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   MODEL     │    │  HEURISTIC  │    │  BASELINE   │    │   DYNAMIC   │      │
│  │ PREDICTION  │    │   LOGIC     │    │ PREDICTION │    │  WEIGHTING  │      │
│  │             │    │             │    │             │    │             │      │
│  │ • Ensemble  │    │ • Tempo     │    │ • Equal     │    │ • Confidence│      │
│  │ • Prob      │    │ • Energy    │    │   Prob      │    │   Based    │      │
│  │ • 4 Classes │    │ • Rules     │    │ • [0.25,0.25│    │ • Weighted   │      │
│  │             │    │ • Happy     │    │   ,0.25,0.25]│    │   Sum      │      │
│  │             │    │   Enhance   │    │             │    │             │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│                                      │                                           │
│                                      ▼                                           │
│                            ┌─────────────┐                                     │
│                            │  COMBINED   │                                     │
│                            │ PROBABILITIES│                                     │
│                            │             │                                     │
│                            │ • Weighted   │                                     │
│                            │   Average   │                                     │
│                            │ • 4 Moods    │                                     │
│                            │ • Enhanced   │                                     │
│                            │   Happy     │                                     │
│                            └─────────────┘                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Heuristic Logic Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        HEURISTIC LOGIC ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   FEATURE   │    │   FEATURE   │    │   RULE      │    │   MOOD      │      │
│  │  SCORING   │───►│  ANALYSIS   │───►│   ENGINE    │───►│ PROBABILITIES│      │
│  │             │    │             │    │             │    │             │      │
│  │ • Tempo     │    │ • High      │    │ • IF-THEN   │    │ • Calm      │      │
│  │ • Energy    │    │   Energy    │    │   Rules     │    │ • Energetic │      │
│  │ • Brightness│    │ • Moderate  │    │ • Thresholds│    │ • Happy     │      │
│  │ • Harmonic  │    │   Energy    │    │ • Happy     │    │ • Sad       │      │
│  │ • Rhythmic  │    │ • Low       │    │   Enhance   │    │             │      │
│  │             │    │   Energy    │    │             │    │             │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           RULE EXAMPLES                                    │   │
│  │                                                                         │   │
│  │ IF tempo > 0.7 AND energy > 0.5:                                      │   │
│  │    Happy = 0.4, Energetic = 0.5, Calm = 0.1, Sad = 0.1              │   │
│  │                                                                         │   │
│  │ IF tempo > 0.5 AND energy > 0.3:                                      │   │
│  │    Happy = 0.5, Energetic = 0.3, Calm = 0.2, Sad = 0.1              │   │
│  │                                                                         │   │
│  │ IF tempo < 0.6 AND energy < 0.4:                                      │   │
│  │    Happy = 0.25, Energetic = 0.1, Calm = 0.5, Sad = 0.3              │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Dynamic Weighting Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                      DYNAMIC WEIGHTING ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  CONFIDENCE │    │   WEIGHT    │    │   WEIGHTED  │    │   FINAL     │      │
│  │   ANALYSIS  │───►│ CALCULATION │───►│ COMBINATION│───►│ PROBABILITIES│      │
│  │             │    │             │    │             │    │             │      │
│  │ • Model     │    │ • High Conf │    │ • Weighted   │    │ • Calibrated│      │
│  │   Confidence│    │   (0.6,0.3,0.1)│    │   Sum      │    │ • Smooth    │      │
│  │ • Thresholds │    │ • Med Conf  │    │ • 4 Moods    │    │ • Enhanced  │      │
│  │ • Ranges    │    │   (0.4,0.4,0.2)│    │ • Happy     │    │   Happy     │      │
│  │ • Decision  │    │ • Low Conf  │    │   Boost     │    │             │      │
│  │   Logic     │    │   (0.2,0.5,0.3)│    │             │    │             │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           WEIGHTING EXAMPLES                                │   │
│  │                                                                         │   │
│  │ HIGH CONFIDENCE (>0.6):                                                  │   │
│  │    Final = 0.6×Model + 0.3×Heuristic + 0.1×Baseline                     │   │
│  │                                                                         │   │
│  │ MEDIUM CONFIDENCE (0.4-0.6):                                             │   │
│  │    Final = 0.4×Model + 0.4×Heuristic + 0.2×Baseline                     │   │
│  │                                                                         │   │
│  │ LOW CONFIDENCE (<0.4):                                                   │   │
│  │    Final = 0.2×Model + 0.5×Heuristic + 0.3×Baseline                     │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Model Training Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         MODEL TRAINING ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   DEAM      │    │   FEATURE   │    │   MODEL     │    │   MODEL     │      │
│  │  DATASET    │───►│  EXTRACTION │───►│  TRAINING   │───►│ VALIDATION  │      │
│  │             │    │             │    │             │    │             │      │
│  │ • 1803 Files│    │ • 15 Features│    │ • Ensemble  │    │ • 5-Fold CV │      │
│  │ • 30s Clips │    │ • Scaling   │    │ • Regular   │    │ • Metrics   │      │
│  │ • MP3 Format│    │ • Preproc   │    │ • Hyperparam │    │ • Accuracy  │      │
│  │ • Labeled   │    │             │    │ • Grid Search│    │ • Confusion │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│                                      │                                           │
│                                      ▼                                           │
│                            ┌─────────────┐                                     │
│                            │   TRAINED   │                                     │
│                            │   MODEL     │                                     │
│                            │             │                                     │
│                            │ • 68.9% Acc │                                     │
│                            │ • Anti-Over │                                     │
│                            │ • Pickle     │                                     │
│                            │ • Metadata   │                                     │
│                            └─────────────┘                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          DEPLOYMENT ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   MODEL     │    │   FASTAPI   │    │   API       │    │   FRONTEND  │      │
│  │  SERVING   │───►│   SERVER    │───►│  GATEWAY    │───►│   CLIENT    │      │
│  │             │    │             │    │             │    │             │      │
│  │ • Pickle    │    │ • Port 8000 │    │ • Port 5000 │    │ • React     │      │
│  │ • Memory    │    │ • Async     │    │ • CORS      │    │ • Upload    │      │
│  │ • 50MB      │    │ • Temp Files│    │ • Proxy     │    │ • Display   │      │
│  │ • <1s Latency│    │ • Cleanup   │    │ • Validation│    │ • Audio     │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           INFERENCE FLOW                                  │   │
│  │                                                                         │   │
│  │ 1. Frontend uploads audio → API Gateway                                    │   │
│  │ 2. API Gateway forwards → FastAPI ML Server                                 │   │
│  │ 3. FastAPI extracts features → Model prediction                              │   │
│  │ 4. Model returns mood + confidence + recommendations                           │   │
│  │ 5. Response flows back → Frontend display                                    │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         MONITORING ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   MODEL     │    │   PERFORMANCE│    │   DRIFT     │    │   ALERTS    │      │
│  │  METRICS   │───►│   TRACKING  │───►│ DETECTION  │───►│ SYSTEM      │      │
│  │             │    │             │    │             │    │             │      │
│  │ • Accuracy  │    │ • Latency   │    │ • Accuracy  │    │ • Email     │      │
│  │ • Confidence│    │ • Memory    │    │   Drop      │    │ • Dashboard │      │
│  │ • Distribution│    │ • CPU       │    │ • Thresholds│    │ • Logs      │      │
│  │ • Volume    │    │ • Requests  │    │ • Retraining│    │ • Auto-fix  │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           MAINTENANCE CYCLE                                 │   │
│  │                                                                         │   │
│  │ 1. Monitor performance metrics                                             │   │
│  │ 2. Detect model drift                                                      │   │
│  │ 3. Trigger alerts if thresholds exceeded                                     │   │
│  │ 4. Schedule retraining with new data                                        │   │
│  │ 5. Deploy updated model                                                    │   │
│  │ 6. Validate performance                                                    │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            DATA FLOW ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  USER UPLOAD → FEATURE EXTRACTION → MODEL PREDICTION → ENHANCEMENT → OUTPUT      │
│                                                                                 │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │  Audio  │───►│  Features   │───►│  Ensemble   │───►│  Dynamic    │───►│  Mood   │ │
│  │  File   │    │  (15)      │    │  Model      │    │  Weighting  │    │  Result │ │
│  │         │    │             │    │             │    │             │    │         │ │
│  │ • MP3   │    │ • Tempo     │    │ • Gradient  │    │ • Confidence│    │ • Calm  │ │
│  │ • 30s   │    │ • Energy    │    │   Boosting  │    │   Based    │    │ • Ener  │ │
│  │ • 44.1kHz│    │ • Spectral  │    │ • Logistic  │    │ • Happy     │    │ • Happy │ │
│  │ • Mono  │    │ • MFCCs     │    │   Regression│    │   Enhance  │    │ • Sad   │ │
│  └─────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────┘ │
│                                                                                 │
│                                      │                                           │
│                                      ▼                                           │
│                            ┌─────────────┐                                     │
│                            │ RECOMMEND   │                                     │
│                            │ ENGINE      │                                     │
│                            │             │                                     │
│                            │ • Similarity│                                     │
│                            │ • 1803 Songs│                                     │
│                            │ • Audio     │                                     │
│                            │   Streaming │                                     │
│                            └─────────────┘                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Complete System Integration

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                      COMPLETE SYSTEM INTEGRATION                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   USER      │    │   FRONTEND  │    │   BACKEND   │    │   ML MODEL  │      │
│  │  INTERFACE  │───►│   SERVICE   │───►│   SERVICES  │───►│   PIPELINE  │      │
│  │             │    │             │    │             │    │             │      │
│  │ • Browser  │    │ • React     │    │ • API       │    │ • Feature   │      │
│  │ • Upload   │    │ • Vite      │    │ • Gateway   │    │   Extraction│      │
│  │ • Playback │    │ • Audio     │    │ • FastAPI   │    │ • Ensemble  │      │
│  │ • Display  │    │ • Player    │    │ • Temp Files│    │ • Heuristics│      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│                                      │                                           │
│                                      ▼                                           │
│                            ┌─────────────┐                                     │
│                            │   DEAM      │                                     │
│                            │  DATASET    │                                     │
│                            │             │                                     │
│                            │ • 1803 Songs│                                     │
│                            │ • Features   │                                     │
│                            │ • Audio      │                                     │
│                            │   Streaming │                                     │
│                            │ • Similarity│                                     │
│                            └─────────────┘                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Performance Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        PERFORMANCE ARCHITECTURE                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   INPUT    │    │   PROCESS   │    │   MODEL     │    │   OUTPUT    │      │
│  │  STAGE     │───►│   STAGE     │───►│   STAGE     │───►│   STAGE     │      │
│  │             │    │             │    │             │    │             │      │
│  │ • Upload   │    │ • Feature   │    │ • Ensemble  │    │ • Mood      │      │
│  │ • <1s      │    │   Extraction│    │ • Heuristics│    │ • Confidence│      │
│  │ • 50MB     │    │ • 0.3s     │    │ • 0.01s    │    │ • Recs      │      │
│  │ • Temp     │    │ • Scaling   │    │ • Weighting  │    │ • <1s total │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           PERFORMANCE METRICS                              │   │
│  │                                                                         │   │
│  │ • Total Processing: < 1 second                                            │   │
│  │ • Memory Usage: 50MB peak                                                  │   │
│  │ • Model Loading: 0.5s (one-time)                                          │   │
│  │ • Feature Extraction: 0.3s                                                 │   │
│  │ • ML Prediction: 0.01s                                                     │   │
│  │ • Heuristic Processing: 0.05s                                               │   │
│  │ • Accuracy: 68.9%                                                          │   │
│  │ • Happy Enhancement: 25-50% probability                                     │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Architecture Summary

The SmartPlay AI/ML model architecture consists of:

### Core Components
1. **Audio Processing**: Librosa-based feature extraction
2. **Feature Engineering**: 15 acoustic features with normalization
3. **Ensemble Model**: GradientBoosting + LogisticRegression
4. **Heuristic Logic**: Rule-based system with happy enhancement
5. **Dynamic Weighting**: Confidence-based combination
6. **Deployment**: FastAPI + API Gateway + Frontend

### Key Features
- **Anti-Overfitting**: Regularization + cross-validation
- **Happy Enhancement**: User-optimized heuristic rules
- **Real-time**: < 1 second processing
- **Production**: Scalable microservices architecture
- **Monitoring**: Performance tracking and drift detection

### Data Flow
Audio Upload → Feature Extraction → Ensemble Prediction → Heuristic Enhancement → Dynamic Weighting → Mood Classification + Recommendations

---

*Architecture diagrams generated on January 19, 2026*  
*Model: Anti-Overfitting Mood Classifier v1.0*  
*Status: Production Ready*
