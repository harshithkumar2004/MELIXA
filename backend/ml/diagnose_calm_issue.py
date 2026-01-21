import requests
import numpy as np

# Test the calm prediction logic
print('=== CALM PREDICTION ISSUE IDENTIFIED ===')

print(' ANALYSIS OF MODEL LOGIC:')
print('Looking at model_loader.py lines 108-112:')
print('elif tempo_score < 0.4 and energy_score < 0.2:  # Low energy, slow tempo')
print('    heuristic_probs[3] = 0.4  # sad')
print('    heuristic_probs[0] = 0.3  # calm')
print('    heuristic_probs[2] = 0.2  # happy')
print('    heuristic_probs[1] = 0.1  # energetic')
print()

print('PROBLEM IDENTIFIED:')
print('The issue is in the HEURISTIC LOGIC:')
print('- For calm prediction: tempo_score < 0.4 AND energy_score < 0.2')
print('- But sad gets 0.4 while calm only gets 0.3')
print('- Sad is favored over calm in low-energy scenarios!')
print()

print('THRESHOLDS TOO STRICT:')
print('tempo_score < 0.4 = tempo < 56 BPM (very slow!)')
print('energy_score < 0.2 = energy < 0.06 (extremely low!)')
print('Most audio doesn\'t meet these strict criteria')
print()

print('ACTUAL CALM PROBABILITIES FROM TEST:')
print('Max calm probability found: 0.254 (25.4%)')
print('This is below the threshold needed for calm prediction')
print()

print('SOLUTION NEEDED:')
print('1. Adjust heuristic weights for calm vs sad')
print('2. Lower thresholds for calm detection')
print('3. Increase calm probability in heuristics')
print('4. Balance the sad/calm probability distribution')

# Test what would happen with adjusted thresholds
print('\n=== SIMULATED ADJUSTMENT ===')
print('If we adjust the logic:')
print('- Give calm: 0.4 instead of 0.3 in low-energy scenarios')
print('- Give sad: 0.3 instead of 0.4')
print('- Lower tempo threshold to < 0.6 (tempo < 84 BPM)')
print('- Lower energy threshold to < 0.4 (energy < 0.12)')

print('\nThis would allow more calm predictions!')
print('Current system is biased against calm predictions due to:')
print('❌ Too strict thresholds')
print('❌ Sad favored over calm in heuristics')
print('❌ Low maximum calm probabilities (max 0.254)')
