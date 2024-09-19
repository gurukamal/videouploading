# Video Upload and Processing Application

## Description

This project is a web application that allows users to upload videos, extract subtitles, and search for phrases within the subtitles. The backend is built using Django and the frontend is built using React.js. Video files are uploaded to AWS S3, and subtitles are extracted using CCExtractor. The app allows users to search for phrases in the subtitles and navigate to specific timestamps in the video.

### Features:
- **Video Upload**: Users can upload video files to the application, which are stored on AWS S3.
- **Subtitle Extraction**: Subtitles are automatically extracted from uploaded videos using CCExtractor.
- **Search Functionality**: Users can search for specific phrases within the subtitles and jump to the corresponding time in the video.
- **List View**: The app lists all uploaded videos and allows users to play them along with the extracted subtitles.

## Technologies Used

### Backend:
- **Django**: Python framework used to handle the backend logic and API.
- **Django REST Framework**: Provides RESTful API endpoints for interacting with the video and subtitle data.
- **PostgreSQL**: Relational database for storing video metadata and subtitles.
- **CCExtractor**: External tool used for extracting subtitles from video files.


### Frontend:
- **Django templates** 

### Other Tools:
- **Docker**: Used to containerize the application for easy setup and deployment.


## Features

- **Video Upload and Storage**: Upload videos from the frontend using React.js, which are stored on AWS S3.
- **Subtitle Extraction**: Automatically extract subtitles from uploaded videos using CCExtractor and save them in the PostgreSQL database.
- **Search Subtitles**: Search for specific phrases in subtitles, and click the timestamp to jump to that point in the video.
- **Docker Support**: The entire application can be run using Docker for ease of development and deployment.

## Prerequisites

Before running the project, ensure you have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started) (Optional, but recommended)


## Installation and Setup

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/video-upload-processing-app.git
cd video-upload-processing-app
```

# Backend Setup (Django)

### 1. Install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```
### 2. Run Migrations:

```bash
python manag.py makemigrations
python manage.py migrate
```

### 3. Run the Django server:

```bash
python manage.py runserver
```
# Running with Docker

### Build and run using Docker Compose:

```bash
docker-compose up --build
```
## Access the Application

http://localhost:8000

# Usage

#### 1. Upload Video: Go to the React frontend, upload a video file along with a title. The video is uploaded to AWS S3 and subtitles are extracted.
#### 2. View Videos: View the list of uploaded videos.
#### 3. Search Subtitles: Search for a phrase in the subtitles and click on the timestamp to jump to that part of the video.

