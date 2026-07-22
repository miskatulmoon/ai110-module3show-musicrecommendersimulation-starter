# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works
Real music recommendation systems mostly use collaborative filtering. The aglroithm analyzes patterns across millions of users' listens/skips such as "people who liked X also liked Y". This is combined with content-based features (audio/genre/mood similarity) and context (time of day, recent plays), often via matrix factorization or deep embeddings, because collaborative signals capture taste better than any hand-coded formula.

For this project, I prioritize only content-based recommendations. I don't have multi-user listening history, just song attributes and one profile. I have a weighted score_song (genre/mood/energy/acousticness).

Song fields:

id (int)
title (str)
artist (str)
genre (str)
mood (str)
energy (float)
tempo_bpm (float)
valence (float)
danceability (float)
acousticness (float)
popularity_score (float)
year_released (int)
duration_sec (int)
instrumentalness (float)
loudness_db (float)

UserProfile fields:
favorite_genre (str)
favorite_mood (str)
target_energy (float)
likes_acoustic (bool)



### Scoring Strategy

`score_song` compares a `Song` against a `UserProfile` on the four fields the profile actually captures (genre, mood, energy, acousticness). The other `Song` fields — `tempo_bpm`, `valence`, `danceability`, `popularity_score`, `year_released`, `duration_sec`, `instrumentalness`, `loudness_db` — are loaded and displayed, but not scored, since `UserProfile` has no matching preference for them yet.

| Feature | Type | Weight | Contribution |
|---|---|---|---|
| Genre match | binary (exact) | 3 | 3 or 0 |
| Mood match | binary (exact) | 2 | 2 or 0 |
| Energy closeness | continuous | 1 | 0–1, scaled by `1 - abs(song.energy - user.target_energy)` |
| Acousticness match | thresholded bool (`acousticness > 0.5`) vs. `likes_acoustic` | 1 | 1 or 0 |

**Max score = 7.**

Genre outweighs mood (3 vs. 2) because both are all-or-nothing matches, so the ranking needs an asymmetry to break ties — genre is treated as the more stable taste signal (instrumentation/style), while mood is a lighter-weight, more session-specific tag that often correlates with genre anyway (e.g. `chill` mood songs in this catalog tend to be lofi/ambient). Energy and acousticness get smaller weights because they already produce graded, partial credit as continuous values, so they don't need a large multiplier to differentiate songs.

**Ranking:** `recommend_songs` calls `score_song` once per song, then sorts all scored songs descending and slices to the top `k`. Scoring answers "how well does this one song match this user," ranking answers "given every song's score, what order do I show them in" — kept as separate steps so weighting can change without touching sort/tie-break logic and vice versa.

### Prompts Answered

- **What features does each `Song` use in your system?** All 15 fields are loaded (`id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, `popularity_score`, `year_released`, `duration_sec`, `instrumentalness`, `loudness_db`), but only `genre`, `mood`, `energy`, and `acousticness` are used in scoring today.
- **What information does your `UserProfile` store?** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic` — one preference per scored `Song` field.
- **How does your `Recommender` compute a score for each song?** The weighted sum above: binary genre/mood matches plus continuous energy-distance and acousticness-threshold checks.
- **How do you choose which songs to recommend?** Score every song, sort descending, return the top `k`.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loading songs from data/songs.csv...
Loaded songs: 21

Top 5 Recommendations
=====================

1. Walk (by NCT 127) - Score: 4.95
     - genre match (+3.0)
     - mood mismatch (+0.0)
     - energy closeness (+0.95)
     - acousticness match (+1.0)

2. Midnight Coding (by LoRoom) - Score: 2.62
     - genre mismatch (+0.0)
     - mood match (+2.0)
     - energy closeness (+0.62)
     - acousticness mismatch (+0.0)

3. Library Rain (by Paper Lanterns) - Score: 2.55
     - genre mismatch (+0.0)
     - mood match (+2.0)
     - energy closeness (+0.55)
     - acousticness mismatch (+0.0)

4. Spacewalk Thoughts (by Orbit Bloom) - Score: 2.48
     - genre mismatch (+0.0)
     - mood match (+2.0)
     - energy closeness (+0.48)
     - acousticness mismatch (+0.0)

5. Sunrise City (by Neon Echo) - Score: 1.98
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy closeness (+0.98)
     - acousticness match (+1.0)

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



