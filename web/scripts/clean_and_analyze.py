import re
import pandas as pd
from collections import Counter
import json

print("==================================================")
print(" STEP 1: CLEANING AUDIO & DURATION DATA")
print("==================================================")
# 1. Load raw audio features
feat = pd.read_csv('data/raw/bolly_song_feature.csv')
print(f"Raw audio rows: {len(feat)}")

# Clean: Drop missing years and durations, extract decade
clean_feat = feat.dropna(subset=['release_year', 'duration_min']).copy()
clean_feat['release_year'] = clean_feat['release_year'].astype(int)
clean_feat['decade'] = (clean_feat['release_year'] // 10 * 10).astype(int)

# Filter realistic decades
clean_feat = clean_feat[(clean_feat['decade'] >= 1990) & (clean_feat['decade'] <= 2020)]

# SAVE PHYSICAL FILE FOR SIR
clean_feat.to_csv('data/cleaned/cleaned_song_features.csv', index=False)
print(f"--> SAVED: data/cleaned/cleaned_song_features.csv ({len(clean_feat)} clean rows)")


print("\n==================================================")
print(" STEP 2: CLEANING & BACKFILLING LYRICS")
print("==================================================")
lyrics = pd.read_csv('data/raw/bolly_song_lyrics.csv')
albums = pd.read_csv('data/raw/dataset7_albums_master.csv')
print(f"Raw lyrics rows: {len(lyrics)}")

# Text cleaner function
def clean_text(s):
    s = str(s).lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    return ' '.join(s.split())

lyrics['film_clean'] = lyrics['Film'].apply(clean_text)
albums['album_clean'] = albums['album_title'].apply(clean_text)

# Build hashmap of Album -> Year to fix -1 years
album_map = albums.dropna(subset=['album_year']).drop_duplicates('album_clean').set_index('album_clean')['album_year'].to_dict()

lyrics['final_year'] = lyrics['Year']
missing_mask = lyrics['final_year'] <= 0
lyrics.loc[missing_mask, 'final_year'] = lyrics.loc[missing_mask, 'film_clean'].map(album_map)

# Filter: keep only verified years from 1960 to 2009
clean_lyrics = lyrics[clean_lyrics_mask := (lyrics['final_year'].notnull()) & (lyrics['final_year'] >= 1960) & (lyrics['final_year'] < 2010)].copy()
clean_lyrics['decade'] = (clean_lyrics['final_year'] // 10 * 10).astype(int)

# SAVE PHYSICAL FILE FOR SIR
clean_lyrics.to_csv('data/cleaned/cleaned_lyrics.csv', index=False)
print(f"--> SAVED: data/cleaned/cleaned_lyrics.csv ({len(clean_lyrics)} clean rows)")


print("\n==================================================")
print(" STEP 3: RUNNING ANALYSIS (DURATION & NLP)")
print("==================================================")
# Metric A: Duration analysis
duration_stats = []
for dec, grp in clean_feat.groupby('decade'):
    duration_stats.append({
        'decade': f'{dec}s',
        'mean_duration': round(float(grp['duration_min'].mean()), 2),
        'median_duration': round(float(grp['duration_min'].median()), 2),
        'sample_count': int(len(grp))
    })

# Metric B: NLP Lexical Diversity
stopwords = {
    'ke', 'ki', 'ka', 'ko', 'se', 'me', 'men', 'hai', 'hain', 'ho', 'ye', 'yehi',
    'wo', 'woh', 'tha', 'thi', 'the', 'na', 'ne', 'par', 'pe', 'aur', 'to', 'bhi',
    'hi', 'jo', 'kar', 'kya', 'kyun', 're', 'o', 'aa', 'ek', 'threedots', '2',
    'kii', 'kaa', 'bhii', 'main', 'tuu', 'naa', 'hove', 'ji'
}

def analyze_words(text):
    words = [w for w in re.findall(r'[a-z]+', str(text).lower()) if w not in stopwords and len(w) > 2]
    total = len(words)
    unique = len(set(words))
    diversity = (unique / total) if total > 0 else 0
    return pd.Series([words, total, diversity], index=['tokens', 'word_count', 'diversity'])

clean_lyrics[['tokens', 'word_count', 'diversity']] = clean_lyrics['Lyrics'].apply(analyze_words)

vocab_stats = []
for dec, grp in clean_lyrics.groupby('decade'):
    all_words = [w for sub in grp['tokens'] for w in sub]
    top_5 = [{'word': w, 'count': c} for w, c in Counter(all_words).most_common(5)]
    vocab_stats.append({
        'decade': f'{dec}s',
        'song_count': int(len(grp)),
        'avg_words_per_song': round(float(grp['word_count'].mean()), 1),
        'vocab_diversity': round(float(grp['diversity'].mean()), 3),
        'top_words': top_5
    })

# Save for the website
payload = {'duration_trends': duration_stats, 'vocabulary_trends': vocab_stats}
with open('web/story_data.json', 'w') as f:
    json.dump(payload, f, indent=2)

print("--> UPDATED: web/story_data.json")
print("PIPELINE FINISHED SUCCESSFULLY!")
