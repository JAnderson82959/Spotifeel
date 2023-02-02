import random
import requests
import spotipy
import datetime
import math

client_id = "c9e41068300d41339499c6e8e1201c70"
secret_id = "45c23a59b4d74eb69322ccfc98aef5a7"
# scope = "user-read-recently-played"
scope = "user-top-read"
username = "johnhfinche"
client = requests.session()
response = client.post("https://accounts.spotify.com/api/token", {"grant_type": "client_credentials", 
                                                        "client_id": client_id, 
                                                        "client_secret": secret_id})
response_data = response.json()
access_token = response_data["access_token"]
headers = {"Authorization": "Bearer {token}".format(token=access_token)}
url = "https://api.spotify.com/v1/"
track_data = requests.get(url + "audio-features/" + 
                          "14ZsKGVCw24TXrfZwtCruS", 
                          headers=headers).json()
print(track_data)

new_access_token = spotipy.util.prompt_for_user_token(username, scope, 
                                                      client_id=client_id, 
                                                      client_secret=secret_id,
                                                      redirect_uri = "http://localhost:8888/callback")

#After : 
today = datetime.datetime.now()
last_5_days = today - datetime.timedelta(days=5)
last_5_days_unix_timestamp = int(last_5_days.timestamp()) * 1000

valences, energy, dancibility = [], [], []
min_valence = 1
min_valence_id = ""

if new_access_token:
    response = spotipy.Spotify(auth=new_access_token)
    recently_played_data = response.current_user_top_tracks()
    for item in recently_played_data["items"]:
        # track = item["track"]
        track_data = response.audio_features(item["id"])
        print(track_data)
        if track_data[0] != {}:
            valences.append(track_data[0]["valence"])
            if track_data[0]["valence"] < min_valence:
                min_valence = track_data[0]["valence"]
                min_valence_id = track_data[0]["id"]

sum = 0
for x in valences:
    sum += float(x)
percent_valence = math.floor((sum / len(valences)) * 100)
most_depressing_track = response.track(min_valence_id)
print(most_depressing_track)
dep_track = most_depressing_track["name"] + " by " + most_depressing_track["artists"][0]["name"]

print(f"You are {100 - percent_valence} percent depressed!\n", f"Most depressing track is {dep_track}")

# todo: analyze lyric content to account for part of depression estimate, playlist of most depressing saved songs, different forms of depression