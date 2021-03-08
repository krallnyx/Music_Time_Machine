import requests
from bs4 import BeautifulSoup
# from os import environ as env
# from dotenv import load_dotenv, find_dotenv


# load_dotenv(".env")
# URL = env.get("URL")
URL = "https://www.billboard.com/charts/hot-100/"


class MusicTimeMachine:
    def __init__(self):
        date = input("Which date do you want to travel to? Type the date in the format YYYY-MM-DD, (from 1959-08-03).")
        response = requests.get(f"{URL}{date}")
        website_html = response.text

        soup = BeautifulSoup(website_html, "html.parser")
        songs = [song.getText() for song in soup.find_all("span", class_="chart-element__information__song")]
        with open(f"top100on{date}.txt", "w") as file:
            [file.write(f"{song}\n") for song in songs]


if __name__ == '__main__':
    music_time_machine = MusicTimeMachine()

