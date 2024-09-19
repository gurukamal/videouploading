# home/tasks.py
from celery import shared_task
from .models import Video
import time
import subprocess
import os

@shared_task
def process_video_task(video_id):
    # Simulate video processing with a sleep
    video = Video.objects.get(id=video_id)
    
    # You can add your actual video processing logic here (e.g., compress, convert, etc.)
    time.sleep(10)  # Simulates video processing
    print(f"Video {video.title} processed successfully!")
    return f"Video {video.title} processed"




@shared_task
def process_video_subtitles(video_id, language):
    """Function to process video and extract subtitles using ccextractor."""
    video = Video.objects.get(id=video_id)
    video_path = video.video.path
    subtitle_path = os.path.splitext(video_path)[0] + f"_{language}.srt"

    # Use ccextractor to extract subtitles
    command = [
        'ccextractor',
        video_path,
        '-o', subtitle_path
    ]

    try:
        subprocess.run(command, check=True)
        video.subtitle_file = subtitle_path

        # Read and save the subtitle content in the database
        with open(subtitle_path, 'r', encoding='utf-8') as subtitle_file:
            video.subtitle_content = subtitle_file.read()

        video.save()
        print(f"Subtitles extracted for video {video.title}")
    except subprocess.CalledProcessError as e:
        print(f"Error during subtitle extraction: {e}")
