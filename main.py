import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import environ as env
from dotenv import load_dotenv

URL = "https://www.billboard.com/charts/hot-100/"
load_dotenv(".env")
CLIENT_ID = env.get("SPOTIFY_ID")
CLIENT_SECRET = env.get("SPOTIFY_SECRET")


class MusicTimeMachine:
    def __init__(self):
        self.date = input("Which day do you want to travel to? Type the date in the format YYYY-MM-DD, (from 1958-08).")
        response = requests.get(URL+self.date)
        website_html = response.text

        soup = BeautifulSoup(website_html, "html.parser")
        self.songs = [song.getText() for song in soup.find_all("span", class_="chart-element__information__song")]
        # we don't need to create the txt file anymore
        # with open(f"top100on{self.date}.txt", "w") as file:
        #    [file.write(f"{song}\n") for song in self.songs]
        self.sp = None
        self.user_id = self.connect_spotify()
        self.getting_spotify_songs()

    def getting_spotify_songs(self):
        song_uris = []
        year = self.date.split("-")[0]
        for song in self.songs:
            result = self.sp.search(q=f"track:{song} year:{year}", type="track")
            print(result)
            try:
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
            except IndexError:
                print(f"{song} doesn't exist in Spotify. Skipped.")

        # Creating a new private playlist in Spotify
        playlist = self.sp.user_playlist_create(user=self.user_id, name=f"{self.date} Top 100", public=False)
        print(playlist)

        # Adding songs found into the new playlist
        self.sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

    def connect_spotify(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-private",
                redirect_uri="http://example.com",
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                show_dialog=True,
                cache_path="token.txt"
            )
        )
        return self.sp.current_user()["id"]


if __name__ == '__main__':
    music_time_machine = MusicTimeMachine()

