import json

# Load and verify the features file
with open('features.json', 'r') as f:
    data = json.load(f)

print(f"Total feature entries: {len(data)}")
print(f"Features per entry: {len(data[0]['features']) if data else 0}")
print("\nSample entries:")
for i in range(min(5, len(data))):
    entry = data[i]
    print(f"  - {entry['filename']}: {len(entry['features'])} features")
    print(f"    First 3 features: {entry['features'][:3]}")

# Verify all entries have 15 features
all_valid = all(len(entry['features']) == 15 for entry in data)
print(f"\nAll entries have 15 features: {all_valid}")

# Check for duplicates
filenames = [entry['filename'] for entry in data]
unique_files = len(set(filenames))
print(f"Unique files: {unique_files}")
print(f"Duplicates: {len(filenames) - unique_files}")
