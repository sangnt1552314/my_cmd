import typer 
import time 
import sys

app = typer.Typer()

@app.command()
def init():
    """
    Initialize the application.
    """

    animation = "|/-\\"
    start_time = time.time()
    while True:
        for i in range(4):
            time.sleep(0.2)  # Feel free to experiment with the speed here
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
        if time.time() - start_time > 10:  # The animation will last for 10 seconds
            break

if __name__ == "__main__":
    app()