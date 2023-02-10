import spotipy
import datetime
import math
from lyricsgenius import Genius
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

TOKEN = "BVXDw7yIcaR3CcjlakOXJIrN5959YsW74uFCwGp7OeuKsz_DGieBsUwMFohifksd"

def spotifeel(auth_manager, cache_handle):
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    gen = Genius(TOKEN)
    sentiment = SentimentIntensityAnalyzer()
    top_tracks = spotify.current_user_top_tracks()
    names = []
    valences = []
    energies = []
    modes = []
    lyrics = []
    pols = []
    min_lyric_num = 1
    min_lyric = ""

    min_valence = 1
    min_valence_id = ""
    max_valence = 0
    max_valence_id = ""

    for item in top_tracks["items"]:
        track_data = spotify.audio_features(item["id"])
        names.append(f"{spotify.track(item['id'])['name']} by {spotify.track(item['id'])['artists'][0]['name']}")
        if track_data[0] != None:
            valences.append(float(track_data[0]["valence"]))
            energies.append(track_data[0]["energy"])
            modes.append(track_data[0]["mode"])
            lyric = gen.search_song(spotify.track(item['id'])['name'], spotify.track(item['id'])['artists'][0]['name'])
            if lyric:
                if lyric.title == spotify.track(item['id'])['name'] and lyric.artist == spotify.track(item['id'])['artists'][0]['name']:
                    lyrics.append(lyric.lyrics)
                    pols.append(sentiment.polarity_scores(lyric.lyrics))
                    valences[-1] += pols[-1]['compound'] / 100
                    if pols[-1]['compound'] < min_lyric_num:
                        min_lyric = lyrics[-1]
                        min_lyric_num = pols[-1]['compound']
                else:
                    lyrics.append([spotify.track(item['id'])['name'], spotify.track(item['id'])['artists'][0]['name'], lyric.title, lyric.artist])
            if track_data[0]["valence"] < min_valence:
                min_valence = track_data[0]["valence"]
                min_valence_id = track_data[0]["id"]
            elif track_data[0]["valence"] > max_valence:
                max_valence = track_data[0]["valence"]
                max_valence_id = track_data[0]["id"]

    dep_count = 0
    avg_valence = 0
    valence_sum = 0
    avg_energy = 0
    energy_sum = 0

    for valence in valences:
        valence_sum += valence
        if float(valence) < 0.5:
            dep_count += 1
    
    for energy in energies:
        energy_sum += float(energy)
    
    avg_valence = valence_sum / len(valences)
    avg_energy = energy_sum / len(energies)

    score = round((avg_valence - .5) * 200, 3)

    saved_valences = None

    return {'min_lyric' : min_lyric, 'pols' : pols, 'lyrics' : lyrics, 'cover_art' : spotify.track(min_valence_id)['album']['images'][0]['url'], 'c2' : spotify.track(max_valence_id)['album']['images'][0]['url'], "saved" : saved_valences, 'score' : score, 'min_name' : spotify.track(min_valence_id)['name'], "min_artist" : spotify.track(min_valence_id)['artists'][0]['name'], "max_name" : spotify.track(max_valence_id)['name'], "max_artist" : spotify.track(max_valence_id)['artists'][0]['name']}

    #to include: most depressing track, mood score converted as if from log scale, quote if too happy or sad, playlist of most depressing saved songs, collect depression data



     # saved = []
    
    # for each in range(200):
    #     batch = spotify.current_user_saved_tracks(limit=50,offset=50*each)
    #     for item in batch["items"]:
    #         saved.append(item)
    #     if saved[-1] == None:
    #         break
    
    # saved_valences = []

    # for item in saved:
    #     track = item["track"]
    #     audio = spotify.audio_features(track["id"])
    #     if track != None and audio[0] != None:
    #         saved_valences.append((audio[0]["valence"], track["name"], track["artists"][0]["name"], track["id"]))

    # saved_valences.sort(key=lambda thing : thing[0])
    # saved_valences = saved_valences[:20]