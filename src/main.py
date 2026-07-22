"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "k-pop", "mood": "chill", "energy": 0.8, "danceability": 0.7, "tempo": 120, "instrumentalness" : 0.1, "loudness": -5.0, "valence": 0.6}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    header = f"Top {len(recommendations)} Recommendations"
    print(f"\n{header}\n{'=' * len(header)}\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} (by {song['artist']}) - Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
        print()


if __name__ == "__main__":
    main()
