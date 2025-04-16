import typer

app = typer.Typer()

@app.command()
def play(song: str):
    """
    Play a song.
    """
    print(f"Playing {song}...")

@app.command()
def stop():
    """
    Stop the music.
    """
    print("Music stopped.")