import typer
import questionary
import subprocess

from .utils import *

app = typer.Typer()

@app.command()
def search(query: str = "", max_results: int = 5, type: str = "video"):
    """
    Search for a video on YouTube.
    """
    if query == "":
        query = questionary.text("Search videos:").ask()
        if not query:
            typer.echo("No search query provided.")
            raise typer.Exit(1)

    videos = youtube_search(query, max_results, type)
    if videos:
        typer.echo(f"Found {len(videos)} videos:")

        video_ids = [video["id"]["videoId"] for video in videos]
        video_titles = [video["snippet"]["title"] for video in videos]
        
        video_options = [
            {
                "id": video_id,
                "name": title,
                "value": video_id,
            }
            for title, video_id in zip(video_titles, video_ids)
        ]
        
        video = questionary.select(
            "What video do you want to play?",
            choices=video_options,
            use_jk_keys=False,
            use_search_filter=True,
        ).ask()

        if video:
            video_option = next((item for item in video_options if item["id"] == video), None)

            youtube_video = YouTubeVideo(video_option["id"])

            if video_option:
                action = questionary.select(
                    "What do you want to do?",
                    choices=[
                        {"name": "Play", "value": "play"},
                        {"name": "Download Only", "value": "download"},
                        {"name": "Download and Play", "value": "download_play"},
                    ],
                ).ask()

                if not action:
                    typer.echo("No action selected.")
                    typer.Exit(1)

                if action == "download" or action == "download_play":
                    output_path = questionary.text(message="Enter the output path for the video:", default='downloads/video').ask()
                    output_path = youtube_video.download(output_path)

                    if output_path:
                        typer.echo(f"Video downloaded to {output_path}")

                        if action == "download_play":
                            command = ["afplay", output_path]
                            try:
                                subprocess.run(command, check=True)
                            except subprocess.CalledProcessError as e:
                                typer.echo(f"Error occurred while playing video: {e}")
                    else:
                        typer.echo("Failed to download the video.")

                if action == "play":
                    youtube_video.stream()

            else:
                typer.echo("Video not found.")
    else:
        typer.echo("No videos found.")

if __name__ == "__main__":
    app()