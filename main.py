import typer

from animations import app as animations_app
from audio import app as audio_app
from yt import app as yt_app
from radio import app as radio_app

app = typer.Typer()

app.add_typer(animations_app, name="animations", help="Animations commands")
app.add_typer(audio_app, name="audio", help="Audio commands")
app.add_typer(yt_app, name="yt", help="YouTube commands")
app.add_typer(radio_app, name="radio", help="Radio commands")

if __name__ == "__main__":
    app()
