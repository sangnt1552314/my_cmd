import typer

from animations import app as animations_app

app = typer.Typer()

app.add_typer(animations_app, name="animations", help="Animations commands")

if __name__ == "__main__":
    app()