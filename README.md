# The Beat of Bollywood: 70 Years of Hindi Cinema Sound

An interactive data story exploring how Bollywood music evolved across seven decades (1950s–2020s)—from 6-minute orchestral poetry to 2.5-minute streaming hooks.

**Live Artifact:** [the-beat-of-bollywood.vercel.app](https://the-beat-of-bollywood.vercel.app)

---

## The Three-Act Story

* **Act I: The Runtime Collapse**  
  Traces song durations falling from over 6 minutes to under 3 minutes, driven by streaming platform algorithms, skip-rate economics, and the death of traditional orchestral intros.

* **Act II: The Vocabulary Shift**  
  Linguistic text analysis tracking the transition from poetic Urdu motifs (*ishq*, *qayamat*, *nazar*) toward modern English and Hinglish slang (*party*, *club*, *swag*).

* **Act III: Acoustic Mood & Beat Evolution**  
  Acoustic signal analysis showing the historical shift from live strings and acoustic instruments to synthesized basslines, higher BPM tempos, and dominant party dance metrics.

---

## Dataset & Technical Scope

* **Macro Catalog:** 57,006 master records covering ~80–85% of all commercial Bollywood tracks ever produced.
* **Lyrics Corpus:** 6,671 full-text Hindi/Urdu songs tokenized for NLP frequency analysis.
* **Audio Features:** ~400 MB of multi-dimensional DSP signal vectors (spectral energy, tempo, danceability).
* **Architecture:** Vanilla JavaScript, D3.js data visualizations, Web Audio API playback, and lightweight precomputed JSON lookups deployed on Vercel.
