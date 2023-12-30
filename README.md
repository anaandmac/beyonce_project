# Beyoncé Project

This project is an exploratory analysis with Spotify data, more specifically *Queen B*, *Mother of the House of Renaissance*, __*Beyoncé*__ data!

On this read.me, you can see how to access Spotify API using OAuth and some results from my analysis.

## Set up the Spotify Developer

The first step is to go to https://developer.spotify.com and create a new dashboard, where it will be possible to get the client id and secret. To this, after logging in with your Spotify account, you can click on Dashboard > Create app.
![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-27%20at%2022.41.54.png)

![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2020.20.18.png)


Then you need to fill in the information about your API, and in the field "*Which API/SDKs are you planning to use?*" you can mark "*Web API*" and "*Web Playback SDK*". This is how I did:
![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2020.28.25.png)

Now, let's get your client id and secret to generate the token. In your dashboard page, click on Settings > View client secret:
![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2020.30.42.png)

![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2020.32.00.png)

![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2020.32.34.png)

Cool, you have everything to start work in the python code!

## Using Python to access Spotify API

Here I will share just how to authenticate your account using python to get some Spotify data. In the Spotify documentation (https://developer.spotify.com/documentation/web-api) you can check all the information that is available and how to build queries.

Here are the libraries that is needed:
```
#Libraries
from requests import post,get
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import json
```

The next step is to paste the credentials provided in the dashboard, and give the URL:
```
#Secret
client_id = "CLIENT ID"
secret = "SECRET"
redirect_url="http://localhost:8888/callback" # the same provided when you create the dashboard

# client_id=os.getenv("client_id")
# secret=os.getenv("secret")
```

Then let's authenticate:
```# Create a Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id, secret, redirect_url, scope='user-library-read')

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()

# Open the authorization URL in the default web browser
webbrowser.open(auth_url)

# Get the authorization code from the user
auth_code = input("Enter the authorization code from the redirect URI: ")

# Get access and refresh tokens
token_info = sp_oauth.get_access_token(auth_code)
access_token = token_info['access_token']
refresh_token = token_info['refresh_token']

# Create a new Spotify client
sp = spotipy.Spotify(auth=access_token)
```

A Spotify page will open and you need to authenticate with your regular account:

<img src="https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2021.00.49.png" width="300" class="center">


After that looks like you have an error, but in the URL there is the authorization code. You can copy everything that is after the *http://localhost:8888/callback?code=* (the URL can change if you configure another path in the dashboard creation).
![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2021.22.02.png)

And just past in the python request and press enter:
![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2021.22.49.png)


After that, you should be authenticated. One way to verify is by getting the user information:
```
#have the token in the required format
def get_header(token):
    return {"Authorization": "Bearer " + token}

#Checking the account
url = "https://api.spotify.com/v1/me/"
headers = get_header(access_token)

result = get(url, headers=headers)
final=json.loads(result.content)
final
```

This is my output, so I know that I'm using my account:

![alt text](https://raw.githubusercontent.com/anaandmac/beyonce_project/main/Screenshot%202023-12-29%20at%2021.31.29.png)

