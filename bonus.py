import pandas as pd
import random
from multiprocessing import Pool, cpu_count

#get artists function
def get_artists(artist_name):
    """
    Returns a dictionary with name, genre, popularity, and followers.
    """
    genres = ["Pop", "Rock", "Hip-Hop", "Jazz", "Electronic", "Classical", "Country"]
    return {
        "artist_name": artist_name,
        "genres": random.choice(genres),
        "followers": random.randint(1000, 1000000),
        "popularity": random.randint(1, 100)
    }

#multiprocessing function
def process_artist(artist_name):
    try:
        data = get_artists(artist_name)
        return data
    except Exception as e:
        print(f"Error processing {artist_name}: {e}")
        return None

def main():
    #load artists
    with open("artists.txt", "r", encoding="utf-8") as f:
        artists = [line.strip() for line in f if line.strip()]

    print(f"Found {len(artists)} artists. Processing...")

    #use multiprocessing
    num_workers = min(cpu_count(), 8)
    with Pool(num_workers) as pool:
        results = pool.map(process_artist, artists)

    #filter
    results = [r for r in results if r]

    #save to CSV
    df = pd.DataFrame(results)
    df.to_csv("artists_info.csv", index=False)
    print("Saved artist info to artists_info.csv")

if __name__ == "__main__":
    main()