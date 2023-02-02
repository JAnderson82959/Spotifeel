import spotipy
import datetime
import math

def spotifeel(auth_manager, cache_handle):
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    top_tracks = spotify.current_user_top_tracks()
    names = []
    valences = []
    energies = []
    modes = []

    min_valence = 1
    min_valence_id = ""
    max_valence = 0
    max_valence_id = ""

    for item in top_tracks["items"]:
        track_data = spotify.audio_features(item["id"])
        names.append(f"{spotify.track(item['id'])['name']} by {spotify.track(item['id'])['artists'][0]['name']}")
        if track_data[0] != {}:
            valences.append(track_data[0]["valence"])
            energies.append(track_data[0]["energy"])
            modes.append(track_data[0]["mode"])
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
        valence_sum += float(valence)
        if float(valence) < 0.5:
            dep_count += 1
    
    for energy in energies:
        energy_sum += float(energy)
    
    avg_valence = valence_sum / len(valences)
    avg_energy = energy_sum / len(energies)

    score = round((avg_valence - .5) * 200, 3)

    return [score, spotify.track(min_valence_id)['name'], spotify.track(min_valence_id)['artists'][0]['name'], spotify.track(min_valence_id)['id'], spotify.track(min_valence_id)['album']['images'][0]['url'], 
            spotify.track(max_valence_id)['name'], spotify.track(max_valence_id)['artists'][0]['name'], spotify.track(max_valence_id)['id'], spotify.track(max_valence_id)['album']['images'][0]['url'], 
            names, valences, avg_valence, avg_energy, dep_count, spotify.audio_features(min_valence_id)]
    #to include: most depressing track, mood score converted as if from log scale, quote if too happy or sad, playlist of most depressing saved songs, collect depression data