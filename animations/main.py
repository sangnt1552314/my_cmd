import typer 
import time 
import sys

from .constants import *

app = typer.Typer()

@app.command()
def run(animation: str = 'stick', duration: int = 10, speed: float = 0.2):
    """
    Run the animation.
    """
    
    if animation == 'stick':
        animation = STICK_ANIMATION
    else:
        if animation not in ANIMATIONS:
            print(f"Animation '{animation}' not found.")
            raise typer.Exit(code=1)
        
        animation = ANIMATIONS[animation]

    start_time = time.time()
    while True:
        for i in range(len(animation)):
            time.sleep(speed)
            sys.stdout.write("\r")
            sys.stdout.write(animation[i % len(animation)])
            sys.stdout.flush()
        if time.time() - start_time > duration:
            sys.stdout.write("\r")
            # sys.stdout.flush()
            break