import re
import json
import pandas as pd
from collections import Counter

print("==========================================================")
print(" RUNNING FULL COMPREHENSIVE BOLLYWOOD ANALYTICS PIPELINE ")
print("==========================================================")

# 1. LOAD DATASETS
feat = pd.read_csv('data/cleaned/cleaned_song_features.csv')
lyrics = pd.read_csv('data/cleaned/cleaned_lyrics.csv')
songs_master = pd.read_csv('data/raw/dataset7_songs_master.csv')
albums_master = pd.read_csv('data/raw/dataset7_albums_master.csv')

# Merge song & album master to get ratings + release years
songs_joined = songs_master.merge(
    albums_master[['album_uuid', 'album_year', 'album_title', 'album_music_director', 'album_rating']], 
    on='album_uuid', 
    how='inner'
)
songs_joined = songs_joined.dropna(subset=['album_year', 'song_rating'])
songs_joined['album_year'] = pd.to_numeric(songs_joined['album_year'], errors='coerce')
songs_joined = songs_joined.dropna(subset=['album_year'])
songs_joined['album_year'] = songs_joined['album_year'].astype(int)
songs_joined['decade'] = (songs_joined['album_year'] // 10 * 10).astype(int)
songs_joined = songs_joined[(songs_joined['decade'] >= 1960) & (songs_joined['decade'] <= 2020)]

# ----------------------------------------------------------------
# INSIGHT 1 & 2: DURATION & HOW TUNES (MOODS) CHANGED
# ----------------------------------------------------------------
duration_stats = []
for dec, grp in feat.groupby('decade'):
    duration_stats.append({
        'decade': f'{dec}s',
        'mean': round(float(grp['duration_min'].mean()), 2),
        'median': round(float(grp['duration_min'].median()), 2),
        'count': int(len(grp))
    })

# Mood shifts over time
mood_trends = []
for dec, grp in feat.groupby('decade'):
    mood_counts = grp['mood'].value_counts(normalize=True).head(3).to_dict()
    mood_trends.append({
        'decade': f'{dec}s',
        'top_moods': {k: round(v * 100, 1) for k, v in mood_counts.items()}
    })

# ----------------------------------------------------------------
# INSIGHT 3: HOW WORDINGS DIFFER (POETIC URDU vs MODERN POP)
# ----------------------------------------------------------------
urdu_poetic = {'ishq', 'deedar', 'zulf', 'sitam', 'firaaq', 'wafa', 'nazar', 'sanam', 'aarzoo', 'kareeb', 'duniya', 'fasana', 'nasha', 'dard', 'intezaar'}
modern_pop = {'baby', 'party', 'love', 'dance', 'disco', 'club', 'sexy', 'night', 'beats', 'rock', 'girl', 'boy', 'crazy', 'music'}
stopwords = {'ke', 'ki', 'ka', 'ko', 'se', 'me', 'men', 'hai', 'hain', 'ho', 'ye', 'yehi', 'wo', 'woh', 'tha', 'thi', 'the', 'na', 'ne', 'par', 'pe', 'aur', 'to', 'bhi', 'hi', 'jo', 'kar', 'kya', 'kyun', 're', 'o', 'aa', 'ek', 'threedots', '2', 'kii', 'kaa', 'bhii', 'main', 'tuu', 'naa', 'hove', 'ji'}

def analyze_linguistics(text):
    words = [w for w in re.findall(r'[a-z]+', str(text).lower()) if len(w) > 2 and w not in stopwords]
    total = len(words)
    if total == 0:
        return pd.Series([0, 0, 0, 0, []], index=['word_count', 'diversity', 'urdu_ratio', 'pop_ratio', 'tokens'])
    unique = len(set(words))
    urdu_count = sum(1 for w in words if w in urdu_poetic)
    pop_count = sum(1 for w in words if w in modern_pop)
    return pd.Series([total, unique/total, (urdu_count/total)*100, (pop_count/total)*100, words], index=['word_count', 'diversity', 'urdu_ratio', 'pop_ratio', 'tokens'])

lyrics[['word_count', 'diversity', 'urdu_ratio', 'pop_ratio', 'tokens']] = lyrics['Lyrics'].apply(analyze_linguistics)

vocab_stats = []
for dec, grp in lyrics.groupby('decade'):
    all_words = [w for sub in grp['tokens'] for w in sub]
    top_terms = [{'word': w, 'count': c} for w, c in Counter(all_words).most_common(5)]
    vocab_stats.append({
        'decade': f'{dec}s',
        'diversity': round(float(grp['diversity'].mean()), 3),
        'urdu_poetic_pct': round(float(grp['urdu_ratio'].mean()), 2),
        'modern_pop_pct': round(float(grp['pop_ratio'].mean()), 2),
        'top_words': top_terms
    })

# ----------------------------------------------------------------
# INSIGHT 4: BEST ARTIST (SINGERS & COMPOSERS OVER TIME)
# ----------------------------------------------------------------
best_singers = []
for dec, grp in songs_joined.groupby('decade'):
    singers_list = grp['song_singers'].dropna().str.split(',').explode().str.strip()
    top_singer = singers_list.value_counts().head(1)
    if not top_singer.empty:
        best_singers.append({
            'decade': f'{dec}s',
            'artist': top_singer.index[0],
            'hit_count': int(top_singer.values[0])
        })

# ----------------------------------------------------------------
# INSIGHT 5 & 6: BEST SONG & TRENDING SONG OVER TIME
# ----------------------------------------------------------------
best_songs = []
for dec, grp in songs_joined.groupby('decade'):
    top_rated = grp.sort_values(by='song_rating', ascending=False).iloc[0]
    best_songs.append({
        'decade': f'{dec}s',
        'song_title': top_rated['song_title'],
        'album': top_rated['album_title'],
        'rating': round(float(top_rated['song_rating']), 2),
        'singers': str(top_rated['song_singers']),
        'year': int(top_rated['album_year'])
    })

# ----------------------------------------------------------------
# EXPORT UNIFIED STORY PAYLOAD
# ----------------------------------------------------------------
payload = {
    'duration_trends': duration_stats,
    'mood_trends': mood_trends,
    'vocabulary_trends': vocab_stats,
    'best_singers': best_singers,
    'best_songs': best_songs
}

with open('web/story_data.json', 'w') as f:
    json.dump(payload, f, indent=2)

print("SUCCESS: Generated 6 analytical dimensions in web/story_data.json")
