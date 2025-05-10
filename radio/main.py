import os
import questionary
import typer
from dotenv import load_dotenv
import requests
from urllib.parse import quote
import vlc
import time

load_dotenv()

app = typer.Typer()

YP_SHOUTCAST_URL = "http://yp.shoutcast.com"

@app.command()
def stations():
    shoutcast_api_key = os.getenv("SHOUTCAST_API_KEY")
    if not shoutcast_api_key:
        typer.echo("SHOUTCAST_API_KEY not found in .env file.")
        raise typer.Exit(1)
    
    ct = questionary.text(message="Search: ", default="us").ask()
    ct = ct.strip().replace(" ", "+")

    limit = questionary.text(message="Limit: ", default="5").ask()
    if not limit:
        limit = 5
    try:
        limit = int(limit)
    except ValueError:
        typer.echo("Invalid limit value. Please enter a number.")
        raise typer.Exit(1)
    
    if limit < 1:
        typer.echo("Limit must be greater than 0.")
        raise typer.Exit(1)
    if limit > 100:
        typer.echo("Limit must be less than 100.")
        raise typer.Exit(1)

    api_url = f"http://api.shoutcast.com/station/nowplaying?k={shoutcast_api_key}&mt=audio/mpeg&f=json&ct={ct}&limit={limit}"

    response = requests.get(api_url)

    if response.status_code != 200:
        typer.echo("Failed to fetch data from SHOUTCAST API.")
        raise typer.Exit(1)
    
    data = response.json()

    tunin = data.get("response", {}).get("data", {}).get("stationlist", {}).get("tunein", {})
    tunin_base_m3u = tunin.get("base-m3u", "")
    tunin_base_xspf = tunin.get("base-xspf", "")
    tunin_base = tunin.get("base", "")

    stations = data.get("response", {}).get("data", {}).get("stationlist", {}).get("station", {})
    
    if not stations:
        typer.echo("No stations found.")
        raise typer.Exit(1)
    
    station_options = [
        {
            "id": str(station["id"]),
            "name": f"""{station["name"]} - {station['genre']}""",
            "value": str(station["id"]),
        }
        for station in stations
    ]

    station_id = questionary.select(
        "What station do you want to play?",
        choices=station_options,
        use_jk_keys=False,
        use_search_filter=True,
    ).ask()

    if not station_id or station_id == "":
        typer.echo("No station selected.")
        raise typer.Exit(1)

    tunin_base_url = f"{YP_SHOUTCAST_URL}/{tunin_base}?id={station_id}"
    tunin_base_m3u_url = f"{YP_SHOUTCAST_URL}/{tunin_base_m3u}?id={station_id}"
    tunin_base_xspf_url = f"{YP_SHOUTCAST_URL}/{tunin_base_xspf}?id={station_id}"

    tunin_response = requests.get(tunin_base_url)
    tunin_base_m3u_response = requests.get(tunin_base_m3u_url)
    tunin_base_xspf_response = requests.get(tunin_base_xspf_url)

    if tunin_response.status_code != 200:
        typer.echo("Failed to fetch data from TUNIN API.")
        raise typer.Exit(1)
    
    tunin_content_data = tunin_response.content
    stream_url = tunin_content_data.decode("utf-8").strip()
    stream_url = stream_url.split("File1=")[1].split("Title1")[0]
    stream_url = quote(stream_url, safe=":/")
    
    print(f"Stream URL: {stream_url}")
    
    # Play the stream using VLC
    play_streaming_audio_vlc(stream_url)

def play_streaming_audio_vlc(url):
    instance = vlc.Instance(['--no-video', '--quiet'])
    player = instance.media_player_new()
    media = instance.media_new(url)
    player.set_media(media)
    player.play()

    time.sleep(2)
    state = player.get_state()

    if state == vlc.State.Error:
        typer.echo("Error playing stream")
        return
    
    typer.echo("Now playing... Press Ctrl+C to stop")

    try:
        while True:
            state = player.get_state()
            if state == vlc.State.Ended or state == vlc.State.Error:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("Stopping playback...")
    finally:
        player.stop()
        player.release()
        instance.release()
   

if __name__ == "__main__":
    app()