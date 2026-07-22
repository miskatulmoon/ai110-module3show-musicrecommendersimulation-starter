"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    header = f"Top {len(recommendations)} Recommendations for {profile_name}"
    print(f"\n{header}\n{'=' * len(header)}\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} (by {song['artist']}) - Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "danceability": 0.85,
            "tempo": 130,
            "instrumentalness": 0.05,
            "loudness": -5.0,
            "valence": 0.8,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "danceability": 0.55,
            "tempo": 75,
            "instrumentalness": 0.15,
            "loudness": -15.0,
            "valence": 0.55,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "danceability": 0.6,
            "tempo": 145,
            "instrumentalness": 0.02,
            "loudness": -6.0,
            "valence": 0.45,
            "likes_acoustic": False,
        },
    }

    for profile_name, user_prefs in user_profiles.items():
        print_recommendations(profile_name, user_prefs, songs)

    # Adversarial / edge-case profiles: these intentionally contain
    # contradictions or invalid-looking values to see whether the
    # scoring logic breaks, crashes, or produces nonsensical rankings.
    adversarial_profiles = {
        "Conflicting Energy vs Mood": {
            # Wants a rock song's raw energy but a mood the dataset
            # associates with slow/quiet tracks -- these pull the
            # score in opposite directions.
            "genre": "rock",
            "mood": "chill",
            "energy": 0.95,
            "likes_acoustic": False,
        },
        "Nonexistent Genre": {
            # No song in the catalog has this genre, so genre match
            # should always fail without raising an error.
            "genre": "vaporwave",
            "mood": "happy",
            "energy": 0.5,
            "likes_acoustic": False,
        },
        "Out-of-Range Energy": {
            # energy > 1.0 is outside the valid [0, 1] scale songs use;
            # confirms energy_contribution stays clamped to [0, 1]
            # instead of going negative or blowing up the score.
            "genre": "pop",
            "mood": "happy",
            "energy": 1.5,
            "likes_acoustic": False,
        },
        "All Preferences Missing": {
            # genre/mood/energy explicitly None simulates a user who
            # never filled out a profile; every song should tie on the
            # first three components and differ only on acousticness.
            "genre": None,
            "mood": None,
            "energy": None,
            "likes_acoustic": False,
        },
        "Acoustic Lover, Loud Genre": {
            # Wants acoustic instrumentation but picked a genre
            # (techno) that's essentially never acoustic in this
            # catalog -- checks that the acousticness component can
            # still tip a low-scoring genre mismatch.
            "genre": "techno",
            "mood": "hypnotic",
            "energy": 0.97,
            "likes_acoustic": True,
        },
    }

    for profile_name, user_prefs in adversarial_profiles.items():
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
