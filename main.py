import typer

from radio import app as radio_app

app = typer.Typer()

app.add_typer(radio_app, name="radio", help="Radio commands")

if __name__ == "__main__":
    app()