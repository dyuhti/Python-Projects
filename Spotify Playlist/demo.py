from bs4 import BeautifulSoup
import requests
import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "9fd7a3cd4db745e799ba4351b39ef13e"
CLIENT_SECRET = "be65edb258874f4f9e95a815c0427c12"
URI_REDIRECT = "https://example.com"
ID = "AQDmSZUw9mKI9ASOaTl8HFd04N41GUD1-Isag39K1FLdkZYHWf7Ga17hicdg2c5j-dWkhsEVirva4aBrBeENVIKTiHtLTV1WamI1Njul_E-FVGH4S3IRDBgRuKrmo5zLJu12IqYEZd_Ul4WNc8eOyYpG3GPrAuvb659XXNJNuIQF0WzoN2qse3hH4nOxJQiv"

response = requests.get("https://www.billboard.com/charts/hot-100/2000-08-12/")
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")

heading = soup.select("li h3.c-title")
song_titles = [header.text.strip() for header in heading[:100]]

sp = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                 client_secret=CLIENT_SECRET,
                                 redirect_uri=URI_REDIRECT,
                                 scope="playlist-modify-private",
                                 cache_path="token.txt")
access_token = sp.get_cached_token()

travel = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
spotify = spotipy.Spotify(auth=access_token['access_token'])

for song in song_titles:
    song_details = spotify.search(
        q=f"track:{song} year:{travel}",
        limit=10,
        type="track",
        market="GB")

