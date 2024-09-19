# home/views.py
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import VideoForm
from .models import Video
import threading
import subprocess
import os
import re
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            # Start subtitle extraction in the background
            t = threading.Thread(target=extract_subtitles, args=(video.id, video.language))
            t.start()
            # Redirect to the list of all videos after successful upload
            return redirect('video_list')
    else:
        form = VideoForm()

    # Fetch all videos for display
    videos = Video.objects.all()

    return render(request, 'base.html', {'form': form, 'videos': videos})

def preprocess_video(video_path, output_path):
    """Function to preprocess the MKV video using FFmpeg."""
    ffmpeg_path = r"C:\Users\dell\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
    command = [
        ffmpeg_path, '-i', video_path, '-c', 'copy', output_path
    ]
    
    print("Preprocessing video with FFmpeg:", command)
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Video preprocessed successfully. New file: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg preprocessing: {e}")
        print(f"Command output: {e.output}")
        raise e

def extract_subtitles(video_id, language):
    """Function to process video and extract subtitles using ccextractor."""
    try:
        video = Video.objects.get(id=video_id)
        video_path = video.video.path
        subtitle_path = os.path.splitext(video_path)[0] + f"_{language}.srt"
        preprocessed_video_path = os.path.splitext(video_path)[0] + "_preprocessed.mkv"


    except ObjectDoesNotExist:
        print(f"Video with ID {video_id} does not exist.")
        return
    
    # Preprocess the video using FFmpeg
    preprocess_video(video_path, preprocessed_video_path)

    ccextractor_path = r"C:\Users\dell\Downloads\CCExtractor_win_portable\ccextractorwinfull.exe"
    if not os.path.isfile(ccextractor_path):
        raise FileNotFoundError(f"CCExtractor executable not found at {ccextractor_path}")

        # Check if the video file exists
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")

    if not os.path.isfile(preprocessed_video_path):
        raise FileNotFoundError(f"Preprocessed video file not found at {preprocessed_video_path}")

    # Use ccextractor to extract subtitles
    command = [
        ccextractor_path,
        preprocessed_video_path,
        
        '-o', subtitle_path
    ]

    print("Executing command:", command)

    try:
        # Capture stdout and stderr for better error handling
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        video.subtitle_file = subtitle_path
        video.save()
        print(f"Subtitles extracted for video '{video.title}'. Subtitle path: {subtitle_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during subtitle extraction: {e}")
        print(f"Command output: {e.output}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




def search_subtitles(subtitle_content, query):
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)\n(?:\n|$)', re.DOTALL)
    matches = []
    print("pattern::",pattern)
    for match in pattern.findall(subtitle_content):
        timestamp = f"{match[1]}"
        subtitle_text = match[4]
        if query.lower() in subtitle_text.lower():
            matches.append((timestamp, subtitle_text))
    print("Matches found:", matches)
    return matches

def search(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    query = request.GET.get('q', '')
    results = []

    if query and video.subtitle_content:
        results = search_subtitles(video.subtitle_content, query)

    return render(request, 'video_details.html', {'video': video, 'query': query, 'results': results})

# List view of uploaded videos
def video_list(request):
    videos = Video.objects.all()  # Fetch all videos from the database
    return render(request, 'video_list.html', {'videos': videos})

# Detail view for a selected video
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'video_details.html', {'video': video})