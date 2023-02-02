from django.shortcuts import render, HttpResponse
from DepressionAnalysis.spotifeel import spotifeel
from django.template import loader
from django.http import HttpResponseRedirect
import spotipy

#: first get a page that logs the user into spotify, then one that displays depression stuff
SPOTIPY_REDIRECT_URI ='http://127.0.0.1:8000/DepressionAnalysis/'
SPOTIPY_CLIENT_ID = "c9e41068300d41339499c6e8e1201c70"
SPORIPY_CLIENT_SECRET = "45c23a59b4d74eb69322ccfc98aef5a7"

#new structure: base "/" page checks if redir w/ token, 
#else if has token, generates analysis, 
#saves it to session and redirs to results display page,
#else displays page with spotify login link

def index(request):
    cache_handle = spotipy.cache_handler.DjangoSessionCacheHandler(request)
    auth_manager = spotipy.oauth2.SpotifyOAuth(redirect_uri=SPOTIPY_REDIRECT_URI,client_id=SPOTIPY_CLIENT_ID,client_secret=SPORIPY_CLIENT_SECRET,scope = "user-top-read", cache_handler=cache_handle,show_dialog=True)
    
    if "code" in request.GET:
        auth_manager.get_access_token(request.GET["code"]) #code is probably authcode or whatever, check header
        return HttpResponseRedirect("/")

    if not auth_manager.validate_token(cache_handle.get_cached_token()):
        context = {'spt_url' : auth_manager.get_authorize_url(), 'headers' : request.GET}
        return render(request, "SpotifyDepression/landing.html", context)
    spotifee = spotifeel(auth_manager, cache_handle)
    context = {'results' : spotifee, 'cover_art' : spotifee[2], 'c2' : spotifee[5]}
    return render(request, "SpotifyDepression/content.html", context)

def content(request):
    #results = spotifeel()
    return HttpResponse("content to be added")