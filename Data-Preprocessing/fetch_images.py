import pandas as pd
import requests
from tqdm import tqdm

count = 0
# Default fallback image URL
fallback_image_url = "https://artists.apple.com/assets/artist-og-share-c766a5950ae664ea9073ede99da0df1094ae1a24bee32b86ab9e43e7e02bce2e.jpg"

# Function to query the iTunes API for cover image URLs
def fetch_cover_image(track_name, artist_name):
    base_url = "https://itunes.apple.com/search"
    params = {
        "term": f"{track_name}",
        "entity": "musicTrack",
        "limit": 1
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        results = response.json().get("results", [])
        if results:
            return results[0].get("artworkUrl100")  # Return the cover image URL
        else:
            print(f"No results found for {track_name} by {artist_name}")
    except requests.exceptions.RequestException as e:
        print(f"Request error for {track_name} by {artist_name}: {e}")
    return None

# Path to input CSV file
input_file = "./music_dataset.csv"
output_file = "./update_music.csv"

# Load the dataset
music_data = pd.read_csv(input_file)
sample_data = music_data.head(20)

# Create a new column for cover images
music_data["cover_image"] = None

# Iterate over rows to fetch cover images
for index, row in tqdm(music_data.iterrows(), total=len(music_data)):
    track_name = row.get("trackName")
    artist_name = row.get("artistName")
    print("TrackName", track_name)
    print("ArtistName", artist_name)
    if pd.notna(track_name) and pd.notna(artist_name):
        image_url = fetch_cover_image(track_name, artist_name)
        if image_url:
            music_data.at[index, "cover_image"] = image_url
            count += 1
        else:
            music_data.at[index, "cover_image"] = fallback_image_url
    else:
        music_data.at[index, "cover_image"] = fallback_image_url

# Save the updated dataset to a new CSV file
music_data.to_csv(output_file, index=False)
print(f"Updated dataset with cover images saved to {output_file}")
print(f"Total valid cover images fetched: {count}")
