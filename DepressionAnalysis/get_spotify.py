import random
import requests
import spotipy
import datetime
import math

SPOTIPY_REDIRECT_URI ='http://127.0.0.1:8000/'
SPOTIPY_CLIENT_ID = "c9e41068300d41339499c6e8e1201c70"
SPORIPY_CLIENT_SECRET = "45c23a59b4d74eb69322ccfc98aef5a7"

def get_spotify(session, request):
    cache_handle = spotipy.cache_handler.DjangoSessionCacheHandler(request)
    auth_manager = spotipy.oauth2.SpotifyOAuth(redirect_uri=SPOTIPY_REDIRECT_URI,client_id=SPOTIPY_CLIENT_ID,client_secret=SPORIPY_CLIENT_SECRET,scope = "user-top-read", cache_handler=cache_handle,show_dialog=True)
    session.__setitem__("loggedin", True)
    return (cache_handle, auth_manager)