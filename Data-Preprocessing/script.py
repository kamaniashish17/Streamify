import pandas as pd
import requests


API_KEY = 'apikey'
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'


def get_song_image(row):
    params = {
        'method': 'track.getInfo',
        'api_key': API_KEY,
        'format': 'json'
    }

    try:
        #  Use trackName and artistName
        params.update({'track': row['trackName'], 'artist': row['artistName']})
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if 'track' in data and 'album' in data['track']:
            images = data['track']['album']['image']
            if images:
                return images[-1]['#text']  # Return the largest image

        #  Use trackCensoredName and artistName
        params.update({'track': row['trackCensoredName']})
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if 'track' in data and 'album' in data['track']:
            images = data['track']['album']['image']
            if images:
                return images[-1]['#text']

        #  Use collectionName and artistName
        params.update({'track': row['collectionName']})
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if 'track' in data and 'album' in data['track']:
            images = data['track']['album']['image']
            if images:
                return images[-1]['#text']

        # Attempt 4: Use collectionCensoredName and artistName
        params.update({'track': row['collectionCensoredName']})
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if 'track' in data and 'album' in data['track']:
            images = data['track']['album']['image']
            if images:
                return images[-1]['#text']

        return None  
    except Exception as e:
        print(f"Error fetching image for {row['trackName']} by {row['artistName']}: {e}")
        return None

# Load your dataset
file_path = 'music_dataset.csv'  
df = pd.read_csv(file_path)

df['image_url'] = df.apply(get_song_image, axis=1)

# Save the updated dataset to a new CSV file
output_path = 'updated_music_dataset_with_images.csv'
df.to_csv(output_path, index=False)

print(f"Updated dataset saved to {output_path}")
