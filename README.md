# Streamify: A Music Streaming Application

Streamify is a music streaming platform developed using Django, inspired by Spotify. It allows users to search and upload songs, and stream music. Streamify uses a distributed database setup using MongoDB with sharding and replication for efficient data management.

## Features
- **User Registration & Login**: Secure user authentication to access the platform.
- **Song Upload**: Users can upload songs along with metadata like artist name, genre, track name, and cover image.
- **Song Search**: Search songs based on artist or genre.
- **Stream Music**: Stream audio files and display cover images dynamically.
- **Distributed Database**: The database is sharded and replicated across two shards for high availability and scalability.

## API Endpoints

### User Authentication
- `POST /register`: User Registration (creates a new user account)
- `POST /login`: User Login (returns session data)
- `POST /logout`: User Logout (ends the current session)

### Home Page
- `GET /`: Streamify Home Page (displays the dashboard with navigation menus, top 5 artists, and genres)
- `POST /`: Upload a new song and redirect to the homepage, starts playing the song

### Song Upload
- `GET /upload_song`: Upload Song Form (displays a form for uploading an audio file, cover image, and song metadata)
- `POST /new_upload`: Serve the newly uploaded song and its cover image

### Song Search and Play
- `POST /search_results`: Songs List Page (displays search results based on query input or selected artist/genre from the homepage. The ‘Play’ button can be clicked to start playing the audio file)
- `POST /audio<int:index>`: Serve audio file for searched songs dynamically (allows access via the `<audio>` tag)
- `POST /image<int:index>`: Serve cover image for searched songs dynamically (loads image via the `<img>` tag)

## Database Setup

The database uses **sharding** and **replication** to handle large amounts of data efficiently:
- **Sharding**: The database is sharded based on a composite hash of the artist name and genre.
- **Replication**: Each shard has one additional replica for fault tolerance and high availability.
- **Hosting**: The database is hosted on AWS EC2 instances for scalable and reliable storage.

## Technologies Used
- **Backend**: Django (Python Web Framework)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB
- **Cloud Hosting**: AWS EC2 for hosting the application and database

## Installation

To run Streamify locally:

1. Clone this repository:
   ```bash
   git clone https://github.com/swapneelparanjpe/Streamify.git
   cd Streamify
   ```

2. Install dependencies
    ```bash
   pip install -r requirements.txt
   ```

3. Start Django server
    ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```
