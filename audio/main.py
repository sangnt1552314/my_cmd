import subprocess
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def run(
    audio: str = typer.Argument(default='./audio/sample_audio/the_office_ost_piano.mp3', help="Path to the audio file"),
    duration: int = typer.Option(10, help="Duration in seconds"),
    speed: float = typer.Option(1.0, help="Speed of playback"),
):
    """
    Run the audio playback.
    """
    path = Path(audio)

    if not path.exists():
        print(f"Audio file '{audio}' not found.")
        raise typer.Exit(code=1)
    
    if not path.is_file():
        print(f"'{audio}' is not a valid file.")
        raise typer.Exit(code=1)
    
    if not path.suffix in ['.mp3', '.wav']:
        print(f"'{audio}' is not a valid audio file. Supported formats are .mp3 and .wav.")
        raise typer.Exit(code=1)
    
    if duration <= 0:
        print(f"Duration '{duration}' must be a positive integer.")
        raise typer.Exit(code=1)
    
    if speed <= 0:
        print(f"Speed '{speed}' must be a positive float.")
        raise typer.Exit(code=1)

    typer.echo(f"Playing {audio} for {duration} seconds at speed {speed}...")

    command = ["afplay", str(path.resolve())]
    if duration:
        command += ['--time', str(duration)]
    if speed:
        command += ['--rate', str(speed)]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while playing audio: {e}")
        raise typer.Exit(code=1)

    typer.echo("Playback finished.")

if __name__ == "__main__":
    app()