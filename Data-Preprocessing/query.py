import time
from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = "mongodb://ec2-3-89-250-161.compute-1.amazonaws.com:28081"
DB_NAME = "streamify"
COLLECTION_NAME = "music"

# Query Configuration
query_filter = {
    "artistName":"One Direction"
}  # Specify your filter, e.g., {"artistName": "John Doe"}
projection = None  # Specify fields to include or exclude, e.g., {"trackName": 1, "_id": 0}

def measure_query_time():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Measure start time
    start_time = time.time()

    # Execute the query
    results = list(collection.find(query_filter, projection))

    # Measure end time
    end_time = time.time()

    # Print query time and result count
    print(f"Query executed in {end_time - start_time:.2f} seconds")
    print(f"Number of documents fetched: {len(results)}")

    return results

if __name__ == "__main__":
    # Run the query and measure the time
    fetched_results = measure_query_time()

    # Optional: Display a sample of the results
    # print("Sample Results:", fetched_results[:5])
