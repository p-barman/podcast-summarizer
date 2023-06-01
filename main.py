from googleapiclient.discovery import build
from pytube import YouTube
import os
import whisper

# Initialize API
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

# Define channel ID
channel_id = "UCcefcZRL2oaA_uBNeo5UOWg"  # Ycombinator

# Get video IDs
def get_videos_from_channel_id(youtube, channel_id, max_results=1):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        type="video"
    )
    response = request.execute()
    return [item['id']['videoId'] for item in response['items']]

# Download audio from videos
def download_audio_from_videos(video_ids):
    for video_id in video_ids:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path='audio', filename=f"{video_id}.mp3")

# Transcribe audio files
def transcribe_audio_files(model, directory='audio'):
    audio_files = [f for f in os.listdir(directory) if f.endswith('.mp3')]
    for audio_file in audio_files:
        file_path = os.path.join(directory, audio_file)
        result = model.transcribe(audio=file_path)
        print(f"Transcription for {audio_file}: {result}")

# Execute
video_ids = get_videos_from_channel_id(youtube, channel_id)
download_audio_from_videos(video_ids)
model = whisper.load_model("large")  # Uncomment this line when the Whisper model is available
transcribe_audio_files(model)  # Uncomment this line when the Whisper model is available
