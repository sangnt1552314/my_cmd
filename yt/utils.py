import os
import vlc
from pytubefix import YouTube
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .constants import *

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def youtube_search(query, max_results=5, type="video"):
    """
    Search for videos on YouTube using the YouTube Data API.
    
    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to return.
    
    Returns:
        list: A list of video IDs that match the search query.
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

    try:
        request = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type=type,
        )
        response = request.execute()

        videos = [item for item in response.get("items", [])]

        return videos
    except HttpError as e:
        print(f"An error occurred: {e}")
        return []


def get_video_path(video_id):
    """
    Get the path to a video file.
    
    Args:
        video_id (str): The ID of the video.
    
    Returns:
        str: The path to the video file.
    """
    return f"https://www.youtube.com/watch?v={video_id}"


def get_video_paths(video_ids):
    """
    Get the paths to multiple video files.
    
    Args:
        video_ids (list): A list of video IDs.
    
    Returns:
        list: A list of paths to the video files.
    """
    return [get_video_path(video_id) for video_id in video_ids]


class YouTubeVideo:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video_path = get_video_path(video_id)
        self.youtube = YouTube(self.video_path)

    def download(self, output_path, file_extension="mp4"):
        """
        Download the video.
        
        Args:
            output_path (str): The path to save the downloaded video.
        
        Returns:
            str: The path to the downloaded video file.
        """
        stream = self.youtube.streams.filter(
            progressive=True, file_extension=file_extension).first()
        stream.download(output_path)

        return os.path.join(output_path, stream.default_filename)

    def stream(self):
        """
        Play the video.
        
        Returns:
            None
        """
        url = self.youtube.streams.filter(only_audio=True).first().url

        # Use VLC to play the audio stream
        try:
            print("Playing audio stream with VLC...")
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new(url)
            player.set_media(media)
            player.play()

            input("Press Enter to stop playback.")  # Keep the script running while VLC plays
        except Exception as e:
            print(f"Error while playing audio with VLC: {e}")
