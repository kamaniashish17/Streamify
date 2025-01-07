import requests
from pymongo import MongoClient
from bson.binary import Binary
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# MongoDB configuration
MONGO_URI = "mongodb://ec2-3-89-250-161.compute-1.amazonaws.com:28081"
DB_NAME = "streamify"
COLLECTION_NAME = "music"

# Path to the CSV file
csv_file_path = "./updated_music_dataset_with_coverImages.csv"

# Required attributes
required_fields = [
    "artistName",
    "country",
    "previewUrl",
    "genreName",
    "releaseDate",
    "trackName",
    "albumName",
    "duration",  # This will be converted to seconds
    "coverImage"
]

# Convert duration from milliseconds to seconds
def convert_duration_to_seconds(duration_ms):
    try:
        return int(duration_ms) // 1000  # Convert ms to seconds
    except ValueError:
        return None

# Function to process a single row
def process_row(row, collection):
    # Extract only required fields
    document = {field: row[field] for field in required_fields if field in row}

    # Convert duration to seconds
    if "duration" in document and document["duration"]:
        document["duration"] = convert_duration_to_seconds(document["duration"])

    # Fetch audio data from previewUrl
    if "previewUrl" in document and document["previewUrl"]:
        try:
            response = requests.get(document["previewUrl"])
            if response.status_code == 200:
                document["audioData"] = Binary(response.content)
            else:
                print(f"Failed to download audio for {document.get('trackName', 'Unknown')}: {response.status_code}")
                document["audioData"] = None
        except requests.RequestException as e:
            print(f"Request failed for {document.get('trackName', 'Unknown')}: {e}")
            document["audioData"] = None

    # Insert the document into the database
    try:
        collection.insert_one(document)
        return True  # Successful upload
    except Exception as e:
        print(f"Failed to upload document: {e}")
        return False  # Failed upload

if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Track upload counts
    total_records = 0
    successfully_uploaded = 0

    # Open the CSV file and read records
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows_to_process = list(csv_reader)[:5000]  # Limit to the first 5000 rows

        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust the number of threads as needed
            future_to_row = {executor.submit(process_row, row, collection): row for row in rows_to_process}

            for future in as_completed(future_to_row):
                total_records += 1
                if future.result():  # Check if the upload was successful
                    successfully_uploaded += 1

    # Print upload summary
    print(f"Upload complete. Total Records Processed: {total_records}")
    print(f"Successfully Uploaded: {successfully_uploaded}")
    print(f"Failed Uploads: {total_records - successfully_uploaded}")
