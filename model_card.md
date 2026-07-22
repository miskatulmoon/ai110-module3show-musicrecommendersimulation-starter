# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch takes a single user's taste profile (favorite genre, favorite mood, target energy, and whether they like acoustic songs) and returns the top-k songs from a small catalog that best match that profile, along with a plain-language explanation of why each song scored the way it did.

It assumes the user can articulate their taste as a few discrete preferences up front — it does not learn from listening history, skips, or likes over time, and it has no notion of multiple users or collaborative signal ("people who liked X also liked Y"). This is a classroom exploration project built to practice turning a small, hand-designed scoring rule into ranked recommendations and to reason about where that rule succeeds or fails — it is not intended for real listeners or production use.

---

## 3. How the Model Works  

Every song in the catalog is compared against the user's profile on four traits: genre, mood, energy, and whether the song sounds acoustic. Genre and mood are all-or-nothing checks — either the song's genre exactly matches what the user said they like (worth 3 points) or it doesn't (worth 0), and the same goes for mood (worth 2 points). Energy is graded rather than all-or-nothing: the closer the song's energy is to the user's target energy, the more of 1 point it earns, so a near-miss still gets partial credit instead of nothing. Acousticness works like a light switch — a song counts as "acoustic" once its acousticness rating crosses a threshold, and the user either likes acoustic songs or doesn't, so this is worth a flat 1 point if the two agree.

Adding those four numbers up gives a song a score out of 7. Every song in the catalog gets scored this way, they get sorted from highest to lowest, and the top few are shown to the user with a short explanation (like "genre match (+3.0)") for every point earned or missed.

Genre is weighted higher than mood on purpose: both are exact-match checks, so the score needs some asymmetry to break ties, and genre feels like the more stable signal of someone's taste (their instrumentation/style preference) while mood is more like a mood-of-the-moment tag. Energy and acousticness get smaller weights because they already reward partial matches on their own, so they don't need to be multiplied up to matter.

Starting from the project scaffold, the scoring logic, CSV loading, and top-k ranking were all originally unimplemented placeholders — this project fills those in with the weighted rule above, plus human-readable explanation strings for every scored song and a CLI that runs several named user profiles (not just one) to compare how the recommendations shift.

---

## 4. Data  

The catalog (`data/songs.csv`) has 21 songs, unmodified from the starter dataset. Each song lists its genre, mood, energy, tempo, valence, danceability, acousticness, popularity, release year, duration, instrumentalness, and loudness, but the scoring rule only looks at genre, mood, energy, and acousticness today.

The catalog is intentionally broad rather than deep: 18 different genres appear across the 21 songs (pop and lofi are the only ones with more than one song — 2 and 3 respectively), and moods are even more scattered, with 16 distinct moods and only "chill," "happy," and "intense" repeated. That means most genres and moods in the catalog are each represented by exactly one song, so a user profile has to get quite lucky to land an exact genre-and-mood match on more than one track.

Nothing was added or removed from the dataset. What's missing is anything that reflects taste beyond a single genre/mood/energy/acoustic snapshot — no tempo or danceability preferences, no notion of "songs like this one," no lyrical content or language, no cultural or regional context, and no way to express liking multiple genres or moods at once. The catalog is also small and hand-curated, so it reflects whatever spread of styles the starter dataset happened to include rather than any real listening population.

---

## 5. Strengths  

The scoring is transparent and predictable: because every point is explainable ("genre match (+3.0)", "energy closeness (+0.92)"), it's easy to see exactly why a song ranked where it did, which is a real strength over a black-box model for a project like this.

It works best for users whose profile happens to line up closely with one of the catalog's few "clustered" genres, like pop or lofi — a "High-Energy Pop" profile (genre `pop`, mood `happy`, energy 0.9) correctly surfaces Sunrise City and Gym Hero at the top, and a "Chill Lofi" profile correctly surfaces Library Rain and Midnight Coding ahead of everything else. The energy-closeness component also behaves sensibly on its own: within a tied genre/mood bracket, the song whose energy is numerically closest to the target always sorts first, which matches intuition.

The genre-weighted-over-mood design also captures a real pattern in this catalog — moods like "chill" already tend to co-occur with certain genres (lofi, ambient), so leaning on genre as the primary signal doesn't lose much even when mood is ignored.

---

## 6. Limitations and Bias 

The biggest limitation is the sparse genre/mood catalog described above: because 18 of 21 songs have a unique genre, most user profiles will score a genre mismatch (0 of 3 points) against nearly the entire catalog, and the "top 5" ends up being decided almost entirely by energy closeness and the acoustic flag rather than genre/mood at all. A user with a genre that isn't in the catalog (or an unusual spelling) fails every genre check silently — there's no fuzzy matching, synonym handling, or error if the genre string is wrong or unrecognized.

The acousticness weight is easy to override: because genre (3) and mood (2) together add up to more than acousticness (1), a user who explicitly wants acoustic songs can still be handed a top recommendation that is *not* acoustic, as long as it wins on genre and mood. Testing a "wants acoustic but picked a loud genre" profile confirmed this — the acoustic preference gets outvoted rather than acting as a hard filter.

The model also treats every user profile as if it has exactly one genre, one mood, one energy target, and one acoustic preference — it can't represent someone who likes two genres, is flexible on mood, or wants a range of energy rather than one number. And when a preference is missing (`None`), every song ties on that component rather than being excluded or penalized, which can silently make one field (like acousticness) the de facto tie-breaker for the whole ranking. None of the weights were tuned against real listener feedback — they're a reasonable-sounding guess, so any bias baked into "genre > mood > energy ≈ acousticness" is a design choice, not something empirically validated.

---

## 7. Evaluation  

Recommendations were checked against several deliberately different profiles: three "normal" profiles meant to represent distinct tastes ("High-Energy Pop," "Chill Lofi," "Deep Intense Rock"), and five adversarial/edge-case profiles designed to try to break or confuse the scoring — a genre/mood contradiction (rock energy with a chill mood), a genre that doesn't exist in the catalog at all, an energy value outside the valid 0–1 range, a profile with every preference set to `None`, and a profile wanting acoustic songs but naming a non-acoustic genre.

For each, the check was whether the ranking and per-song explanations made sense given the weights, and whether anything crashed. Nothing raised an exception in any case, including the out-of-range energy value and the all-`None` profile, so the scoring logic is robust to bad or missing input. What was surprising: the all-`None` profile produced a 5-way tie at the same score, meaning the "top 5" for a user with no stated preferences is really just an arbitrary slice of the catalog in CSV order — and the acoustic-preference test confirmed that genre+mood can outvote an explicit acoustic preference, which is a real design tradeoff rather than a bug, but one that's easy to miss without deliberately testing for it.

---

## 8. Future Work  

- Let a user express a *range* of acceptable energy (or tempo/danceability) instead of a single target number, and/or allow more than one acceptable genre or mood per profile.
- Normalize or fuzzy-match genre and mood strings (case, synonyms, singular/plural) so a near-miss like "Pop" vs "pop" doesn't silently score as a total mismatch.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Music recommender systems suggest songs based on user behavior (collaborative filtering) or song attributes (content-based). Using songs.csv, a content-based system might recommend "Walk" by NCT 127 to a fan of "Gym Hero" because both share high energy, tempo, and danceability.

I discovered that content-based scoring strategies can create a bubble where diversity collapses. A fan of energetic K-pop might never discover a chill lo-fi track, even if they'd secretly enjoy it, because the system only measures similarity, not surprise or emotional contrast.