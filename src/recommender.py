import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity_score: float
    year_released: int
    duration_sec: int
    instrumentalness: float
    loudness_db: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")

    int_fields = {"id", "year_released", "duration_sec"}
    float_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "popularity_score",
        "instrumentalness",
        "loudness_db",
    }

    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences, returning (score, reasons) per the README weighting."""
    user_genre = user_prefs.get("genre", user_prefs.get("favorite_genre"))
    user_mood = user_prefs.get("mood", user_prefs.get("favorite_mood"))
    target_energy = user_prefs.get("energy", user_prefs.get("target_energy"))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    score = 0.0
    reasons = []

    if user_genre is not None and song["genre"] == user_genre:
        score += 3.0
        reasons.append("genre match (+3.0)")
    else:
        reasons.append("genre mismatch (+0.0)")

    if user_mood is not None and song["mood"] == user_mood:
        score += 2.0
        reasons.append("mood match (+2.0)")
    else:
        reasons.append("mood mismatch (+0.0)")

    if target_energy is not None:
        energy_contribution = max(0.0, min(1.0, 1 - abs(song["energy"] - target_energy)))
        score += energy_contribution
        reasons.append(f"energy closeness (+{energy_contribution:.2f})")
    else:
        reasons.append("energy closeness (+0.00)")

    song_is_acoustic = song["acousticness"] > 0.5
    if song_is_acoustic == likes_acoustic:
        score += 1.0
        reasons.append("acousticness match (+1.0)")
    else:
        reasons.append("acousticness mismatch (+0.0)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts descending, and returns the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
