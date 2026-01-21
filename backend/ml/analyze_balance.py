import numpy as np

print('MOOD BALANCE ANALYSIS')
print('=' * 50)

scenarios = {
    'High Energy': [0.1, 0.5, 0.4, 0.1],      # calm, energetic, happy, sad
    'Moderate Energy': [0.2, 0.3, 0.5, 0.1],
    'Low Energy': [0.5, 0.1, 0.2, 0.3],
    'Bright Harmonic': [0.2, 0.3, 0.5, 0.1],
    'Balanced': [0.35, 0.25, 0.35, 0.15],
    'Baseline': [0.25, 0.25, 0.25, 0.25]
}

print('\n CURRENT PROBABILITY DISTRIBUTIONS:')
print('Scenario' + ' ' * 12 + 'Calm | Energetic | Happy | Sad | Total')
print('-' * 55)

for scenario, probs in scenarios.items():
    total = sum(probs)
    print(f'{scenario:<15} | {probs[0]:>4.2f} | {probs[1]:>9.2f} | {probs[2]:>5.2f} | {probs[3]:>4.2f} | {total:>5.2f}')

print('\n BALANCE ANALYSIS:')
print('=' * 50)

# Calculate average probabilities across all scenarios
all_probs = np.array(list(scenarios.values()))
avg_probs = np.mean(all_probs, axis=0)

print(f'\n AVERAGE PROBABILITIES ACROSS ALL SCENARIOS:')
mood_names = ['Calm', 'Energetic', 'Happy', 'Sad']
for i, mood in enumerate(mood_names):
    print(f'  {mood:<10}: {avg_probs[i]:.3f}')

# Calculate standard deviation
std_devs = np.std(all_probs, axis=0)
print(f'\n STANDARD DEVIATION (lower = more balanced):')
for i, mood in enumerate(mood_names):
    print(f'  {mood:<10}: {std_devs[i]:.3f}')

# Overall balance score
overall_std = np.mean(std_devs)
print(f'\n OVERALL BALANCE SCORE: {overall_std:.3f}')
print('(Lower score = more balanced across scenarios)')

print('\n DETAILED BALANCE ANALYSIS:')

# Check if each scenario sums to 1.0
print('\n PROBABILITY SUM CHECK:')
for scenario, probs in scenarios.items():
    total = sum(probs)
    balanced = abs(total - 1.0) < 0.001
    status = ' BALANCED' if balanced else ' UNBALANCED'
    print(f'  {scenario:<15}: {total:.3f} {status}')

# Check mood distribution balance
print('\n MOOD DISTRIBUTION BALANCE:')
mood_totals = np.sum(all_probs, axis=0)
mood_percentages = mood_totals / np.sum(mood_totals) * 100

for i, mood in enumerate(mood_names):
    percentage = mood_percentages[i]
    ideal = 25.0  # Perfect balance would be 25% each
    diff = abs(percentage - ideal)
    balance_status = '✅' if diff < 5 else '⚠️' if diff < 10 else '❌'
    print(f'  {mood:<10}: {percentage:>5.1f}% (ideal: 25.0%) {balance_status} diff: {diff:.1f}%')

print('\n BALANCE CONCLUSIONS:')

# Check if system is mood-biased
max_mood_idx = np.argmax(mood_percentages)
min_mood_idx = np.argmin(mood_percentages)
max_diff = mood_percentages[max_mood_idx] - mood_percentages[min_mood_idx]

print(f' Most favored mood: {mood_names[max_mood_idx]} ({mood_percentages[max_mood_idx]:.1f}%)')
print(f' Least favored mood: {mood_names[min_mood_idx]} ({mood_percentages[min_mood_idx]:.1f}%)')
print(f' Mood bias range: {max_diff:.1f}%')

# Balance assessment
if max_diff < 5:
    balance_quality = 'PERFECTLY BALANCED'
elif max_diff < 10:
    balance_quality = 'SLIGHTLY UNBALANCED'
elif max_diff < 20:
    balance_quality = 'MODERATELY UNBALANCED'
else:
    balance_quality = 'SEVERELY UNBALANCED'

print(f' Overall Balance Quality: {balance_quality}')

print('\n RECOMMENDATIONS:')

if overall_std < 0.15:
    print('EXCELLENT: Very balanced across all scenarios')
elif overall_std < 0.20:
    print('GOOD: Well balanced with minor variations')
elif overall_std < 0.25:
    print('FAIR: Some imbalance present')
else:
    print('POOR: Significant imbalance detected')

# Specific mood balance checks
print('\nPER-MOOD BALANCE:')
for i, mood in enumerate(mood_names):
    if std_devs[i] < 0.15:
        print(f'{mood}: Very consistent across scenarios')
    elif std_devs[i] < 0.20:
        print(f'{mood}: Moderately consistent')
    else:
        print(f'{mood}: Highly variable (potential bias)')

print('\n' + '=' * 50)
print('SUMMARY: Perfect balance = 25% each mood across all scenarios')
print('CURRENT: Check detailed analysis above for balance assessment')
