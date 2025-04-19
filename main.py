import typer

from animations import app as animations_app
from audio import app as audio_app

app = typer.Typer()

app.add_typer(animations_app, name="animations", help="Animations commands")
app.add_typer(audio_app, name="audio", help="Audio commands")

if __name__ == "__main__":
    app()