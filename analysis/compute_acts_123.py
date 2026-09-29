import pandas as pd
import numpy as np
import re
import json

print("=" * 60)
print("COMPUTING 100% VERIFIED NUMBERS FOR ACTS 1, 2, AND 3")
print("=" * 60)

results = {}

# -------------------------------------------------------------
# ACT I: DURATION BY DECADE (bolly_song_feature.csv)
# -------------------------------------------------------------
print("\n--- ACT I: MEDIAN DURATION BY DECADE ---")
df_feat = pd.read_csv("data/raw/bolly_song_feature.csv")
df_feat['clean_year'] = pd.to_numeric(df_feat['release_year'], errors='coerce')
df_feat = df_feat.dropna(subset=['clean_year', 'duration_min'])
df_feat['decade'] = (df_feat['clean_year'] // 10 * 10).astype(int).astype(str) + 's'

dur_median = df_feat[df_feat['clean_year'] >= 1960].groupby('decade')['duration_min'].median().round(2)
print(dur_median.to_string())
results['act1_duration'] = dur_median.to_dict()

# -------------------------------------------------------------
# ACT III: MOOD (ROMANCE VS DANCE/PARTY) BY DECADE
# -------------------------------------------------------------
print("\n--- ACT III: MOOD COUNTS & CATEGORIES ---")
print("Unique sample moods:", df_feat['mood'].dropna().unique()[:8])

df_feat['is_dance'] = df_feat['mood'].astype(str).str.contains('happy|dance|energetic|party|excited|upbeat', case=False)
df_feat['is_romance'] = df_feat['mood'].astype(str).str.contains('sad|romance|romantic|calm|acoustic|mellow|love', case=False)

mood_eras = df_feat[df_feat['clean_year'] >= 1990].groupby('decade')[['is_romance', 'is_dance']].sum()
mood_pct = (mood_eras.div(mood_eras.sum(axis=1), axis=0) * 100).round(1)
print("\nMood Percentages (Romance vs Dance/Upbeat):")
print(mood_pct.to_string())
results['act3_mood'] = mood_pct.to_dict()

# -------------------------------------------------------------
# ACT II: WORD PROMINENCE ACROSS ERAS (hindi_lyrics.csv)
# -------------------------------------------------------------
print("\n--- ACT II: ACTIVE ERA WINDOWS FOR TOKENS ---")
df_lyr = pd.read_csv("data/raw/hindi_lyrics.csv")
df_lyr['clean_year'] = pd.to_numeric(df_lyr['Year'], errors='coerce')
df_lyr = df_lyr.dropna(subset=['clean_year', 'Lyrics'])

tokens = ['ishq', 'zulf', 'deedaar', 'jaam', 'firaaq', 'mehboob', 'sanam', 'baby', 'party', 'nacho', 'swag', 'club', 'crazy']
token_windows = {}

for t in tokens:
    matches = df_lyr[df_lyr['Lyrics'].str.contains(rf'\b{t}\b', case=False, na=False)]
    if len(matches) > 0:
        min_y = int(matches['clean_year'].quantile(0.15))
        max_y = int(matches['clean_year'].quantile(0.85))
        token_windows[t] = {
            "count": int(len(matches)),
            "window": f"{min_y}–{max_y}",
            "start": min_y,
            "end": max_y
        }
        print(f"{t:<10} | Occurrences: {len(matches):<4} | Active Core Window: {min_y}–{max_y}")
    else:
        token_windows[t] = {"count": 0, "window": "N/A", "start": None, "end": None}
        print(f"{t:<10} | Occurrences: 0")

results['act2_lexicon'] = token_windows

# -------------------------------------------------------------
# SAVE SUMMARY JSON FOR FRONTEND INTEGRATION
# -------------------------------------------------------------
with open("data/computed_acts_123_metrics.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nSaved verified metrics to data/computed_acts_123_metrics.json!")
