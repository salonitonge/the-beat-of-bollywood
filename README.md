# The Beat of Bollywood: 70 Years of Hindi Cinema Sound

[![Live Demo](https://img.shields.io/badge/Live_Site-Vercel-black?style=flat&logo=vercel)](https://the-beat-of-bollywood.vercel.app)
[![Data Scope](https://img.shields.io/badge/Corpus-57%2C000%2C_Tracks-ff69b4?style=flat)](#-data-engineering--corpus-scope)
[![Stack](https://img.shields.io/badge/Stack-Vanilla_JS_%E2%80%82_D3_%E2%80%82_Audio_DSP-blue?style=flat)](#-technical-architecture)

An interactive, visual data storytelling application analyzing seven decades (1950s–2020s) of Hindi film music evolution across acoustic signals, lyrical composition, and cultural dynamics.

---

## Live Deployment

Experience the interactive scrollytelling artifact live:  
**[the-beat-of-bollywood.vercel.app](https://the-beat-of-bollywood.vercel.app)**

---

## Project Structure & Three-Act Narrative

1. **Act I: The Great Runtime Collapse**
   * Empirical analysis of track length evolution from 6+ minute orchestral arrangements to sub-3 minute streaming loops.
   * Examines algorithmic incentives, skip-rate mechanics, and hook-early composition.

2. **Act II: The Vocabulary Shift (Urdu to Hinglish)**
   * NLP tokenization and linguistic frequency shifts across 6,600+ lyric files.
   * Tracks the transition from classical Urdu poetic motifs (*ishq*, *qayamat*, *nazar*) to urban Hinglish pop vernacular (*party*, *swae�, *club*).

3. **Act III: Acoustic Mood & Genre Evolution**
   * High-dimensional acoustic feature breakdown (energy, danceability, romance vs. party ratios).
   * Highlights rhythmic modernization, synth adoption, and changing cultural consumption habits.

---

## Data Engineering & Corpus Scope

|| Records / Scale | Description |
|---|---|---|
| **Macro Catalog** | **57,006 Tracks** | Master archive capturing commercial Hindi cinema releases (1950–present). |
| **Lyric NLP Corpus** | **6,671 Documents** | Cleaned and tokenized full-text Hindi/Urdu lyrics for linguistic shift modeling. |
| **Acoustic Features** | **~400 MB DSP Data** | Multi-dimensional audio signal vectors (tempo, spectral energy, danceability). |
| **Benchmark Baseline** | **~1,500 Tracks** | Balanced historical baseline across 7 decades preventing recency/streaming bias. |

>**Methodological Note on Data Size:** Commercial Hindi cinema has produced an estimated 70,000 total songs in its history. Our raw catalog of 57,000+ tracks represents **~80–85% of the total recorded universe**, providing high population coverage rather than a sparse random sample.

---

## Technical Architecture

* **Frontend**: Responsive visual interface with custom CSS styling and scrollytelling mechanics.
* **Audio Visualizer**: Custom HTML5 Web Audio API synchronization with interactive waveform preview tracks.
* **Data Processing**: Python (`pandas`, `numpy`, NLP tokenization) with precomputed lightweight client-side JSON lookups.
* **DevOps / CI/CD**: Automated deployment pipelines through GitHub Actions and Vercel Edge Network.
