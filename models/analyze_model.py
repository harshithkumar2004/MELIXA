import joblib
import numpy as np

# Load the model bundle
bundle = joblib.load('anti_overfitting_mood_classifier.pkl')

# Get detailed model information
model = bundle['model']
scaler = bundle['scaler']

print('=== BASE ML MODEL: ANTI-OVERFITTING MOOD CLASSIFIER ===')
print()

# Voting Classifier details
print('MODEL TYPE: VotingClassifier (Ensemble)')
print('Voting Method: soft (probability averaging)')
print('Number of Estimators: 2')
print('Weights: [2, 1]')
print()

# Get estimator details
estimators = model.named_estimators_
print('ESTIMATOR DETAILS:')

for name, estimator in estimators.items():
    print(f'ESTIMATOR: {name.upper()} - {type(estimator).__name__}')
    weight_idx = list(estimators.keys()).index(name)
    print(f'  Weight: {model.weights[weight_idx]}')
    
    if hasattr(estimator, 'n_estimators'):
        print(f'  Trees: {estimator.n_estimators}')
    if hasattr(estimator, 'learning_rate'):
        print(f'  Learning Rate: {estimator.learning_rate}')
    if hasattr(estimator, 'C'):
        print(f'  Regularization C: {estimator.C}')
    if hasattr(estimator, 'solver'):
        print(f'  Solver: {estimator.solver}')
    if hasattr(estimator, 'max_depth'):
        print(f'  Max Depth: {estimator.max_depth}')
    if hasattr(estimator, 'max_features'):
        print(f'  Max Features: {estimator.max_features}')
    if hasattr(estimator, 'class_weight'):
        print(f'  Class Weight: {estimator.class_weight}')
    print()

print('FEATURE PREPROCESSING:')
print(f'Scaler: {type(scaler).__name__}')
print(f'Input Features: {scaler.n_features_in_}')
print(f'Output Classes: {len(bundle["classes"])}')
print(f'Class Labels: {list(bundle["classes"])}')
print()

print('MODEL ARCHITECTURE SUMMARY:')
print('1. GradientBoostingClassifier (Weight: 2)')
print('   - 50 decision trees')
print('   - Learning rate: 0.05')
print('   - Max depth: 3')
print('   - Captures non-linear patterns')
print()
print('2. LogisticRegression (Weight: 1)')
print('   - Linear classifier')
print('   - Regularization C: 0.1')
print('   - Balanced class weights')
print('   - Provides linear baseline')
print()
print('3. StandardScaler Preprocessing')
print('   - Normalizes 15 audio features')
print('   - Zero mean, unit variance')
print('   - Ensures feature comparability')
print()
print('WHY THIS MODEL?')
print('- Ensemble reduces overfitting')
print('- Gradient boosting captures complex patterns')
print('- Logistic regression prevents overfitting')
print('- Soft voting provides probability outputs')
print('- Weighted ensemble prioritizes tree model')
