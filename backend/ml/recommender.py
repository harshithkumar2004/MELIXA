import json
import numpy as np
from scipy.spatial.distance import cosine, euclidean

with open("../../deam/features.json") as f:
    DEAM = json.load(f)

def similarity(v1, v2):
    cos = 1 - cosine(v1, v2)
    euc = 1 / (1 + euclidean(v1, v2))
    return (0.7 * cos + 0.3 * euc) * 100

def recommend(input_vec):
    scores = []
    for item in DEAM:
        sim = similarity(input_vec, np.array(item["features"]))
        scores.append({
            "filename": item["filename"],
            "similarity": round(sim, 2)
        })

    scores.sort(key=lambda x: x["similarity"], reverse=True)
    return scores[:5]
