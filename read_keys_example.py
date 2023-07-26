from spotipy.oauth2 import SpotifyOAuth

# Make a file called mykeys.py and put this in it (with your keys)
# SPOTIPY_CLIENT_ID = "dhnuaybbasehguihnr342u3hu23"
# SPOTIPY_CLIENT_SECRET = "23232hjkhbkh3jnJk"
# you also will need to explain in your user's guide how your user
# needs tp create this file!


import mykeys 

scope = 'user-library-read'
a = SpotifyOAuth(client_id=mykeys.SPOTIPY_CLIENT_ID, 
            client_secret=mykeys.SPOTIPY_CLIENT_SECRET, 
            scope=scope,
            redirect_uri="http://localhost:8888/callback", 
            cache_path=".\cache")