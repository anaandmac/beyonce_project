#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Libraries
import pandas as pd
from requests import post,get
import spotipy

from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import json
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio


# ### Accessing Spotify Token

# In[2]:


#Secret
client_id = "68046c942cde47fe8b4b9baa9fd5cf23"
secret = "298a7e08695c4d46adb3b5fa727793f5"

# client_id=os.getenv("client_id")
# secret=os.getenv("secret")


# In[3]:


redirect_url="http://localhost:8888/callback" # the same provided when you create the dashboard

# Create a Spotify OAuth object
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


# In[4]:


#have the token in the required format
def get_header(token):
    return {"Authorization": "Bearer " + token}


# In[5]:


#Checking the account
url = "https://api.spotify.com/v1/me/"
headers = get_header(access_token)

result = get(url, headers=headers)
final=json.loads(result.content)
final


# ### Functions to collect data

# In[6]:


# Function to get artist ID
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['artists']['items'][0]


# In[7]:


#Get top songs
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?&country=BR"
    headers = get_header(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


# In[8]:


#Playlist by country
def search_playlist(country_list,artist):
    url = "https://api.spotify.com/v1/search"
    query = f"?q=%{artist_name}%&type=playlist&market=BR&limit=1&offset=0" # just to get columns name
    query_url = url + query
    result = get(query_url, headers=headers)
    final=json.loads(result.content)
    df_final=pd.DataFrame(columns=(pd.DataFrame.from_dict(final['playlists']['items'])).columns)
    # loop per contry
    for country in country_list:
        query = f'?q=%{artist_name}%&type=playlist&market={country}&limit=50&offset=0'# offset 0
        query_url = url + query
        result = get(query_url, headers=headers)
        final=json.loads(result.content)

        df_country=pd.DataFrame.from_dict(final['playlists']['items'])
        df_country['country']=country
        print(country, len(df_country))
        
        df_final=pd.concat([df_final,df_country],ignore_index=True)
        
    df_final['treated_URL']=df_final['external_urls'].apply(json.dumps).apply(json.loads).apply(lambda x: x.get('spotify'))
    return(df_final)    
#     return(df_final.drop_duplicates(subset=['id'])) ## For some countries the result are equal, like "This is Beyonce" 


# ### Exploratory analisis

# In[9]:


artist_name="Beyoncé"


# In[10]:


artist_id=search_for_artist(access_token,artist_name)['id']


# In[11]:


songs=get_songs_by_artist(access_token, artist_id)

df_top_tracks=pd.DataFrame(columns=['song','song_id'])

for idx, song in enumerate(songs):
    df_top_tracks.loc[idx,'song']=song['name']
    df_top_tracks.loc[idx,'song_id']=song['id']
df_top_tracks


# In[12]:


#Checking her followers
url = "https://api.spotify.com/v1/search"
query = f"?q={artist_name}&type=artist&offset=0&limit=1"

query_url = url + query
result = get(query_url, headers=headers)
final=json.loads(result.content)

print('followers: ',"{:,}".format(int(final['artists']['items'][0]['followers']['total'])), '\n',
      'popularity: ', final['artists']['items'][0]['popularity'], sep='')


# ## Data by country

# In[13]:


#cities with Renaissance concerts and Brazil
data = {
    'ISO': ["BR","SE","BE", "GB", "GB", "GB", "FR", "GB", "ES", "FR", "DE", "NL", "DE", "DE", "PL", "CA", "US", 
            "US", "US", "US", "US", "US", "US", "US", "US", "US", "US", "US", "US", "US", "US", "US", "US",
            "US", "CA", "US", "US", "US", "US", "US"],
    'country_name': ["Brazil", "Sweden","Belgium", "United Kingdom", "United Kingdom", "United Kingdom", 
                     "France", "United Kingdom", "Spain", "France", "Germany", "Netherlands", "Germany",
                     "Germany", "Poland", "Canada", "United States", "United States", "United States",
                     "United States", "United States", "United States", "United States", "United States", 
                     "United States", "United States", "United States", "United States", "United States", 
                     "United States", "United States", "United States", "United States", "United States", 
                     "Canada", "United States", "United States", "United States", "United States", "United States"],
    'city_name':["None", "Stockholm","Brussels","Cardiff","Edinburgh", "Sunderland", "Paris", "London", "Barcelona",
                 "Marseille", "Cologne", "Amsterdam", "Hamburg", "Frankfurt", "Warsaw", "Toronto", "Philadelphia", 
                 "Nashville", "Louisville", "Minneapolis", "Chicago", "Detroit", "East Rutherford",
                 "Boston", "Washington, D.C.", "Charlotte", "Atlanta", "Tampa", "Miami", "St. Louis", "Phoenix",
                 "Las Vegas", "San Francisco", "Inglewood", "Vancouver", "Seattle", "Dallas", "Houston", 
                 "New Orleans", "Kansas City"]
}

# Create a DataFrame
df_countries = pd.DataFrame(data)
df_countries.head()


# In[14]:


df_countries['ISO'].unique()


# In[15]:


#Playlists with Beyoncé

# I believe the API brings to most relevant results, there are similar playlists between the countries
country_list=df_countries['ISO'].unique()
# country_list

df_playlist=search_playlist(country_list,artist_name)  

df_playlist.head()


# In[27]:


# df_playlist.to_csv('df_playlist.csv')
df_playlist[~df_playlist['name'].str.contains('Beyonc', case=False)][['name','description']].drop_duplicates()


# In[17]:


playlist_id_list=df_playlist['id'].unique()
df_playlist['followers']=np.NaN #creating empty column to add number of followers in the playlist dataset
df_songs_in_playlist_final=pd.DataFrame(columns=['songs','playlist_id','artists','popularity','song_id'])

for playlist_id in playlist_id_list:
#     print(playlist_id)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    result = get(url,headers=headers)
    json_result=json.loads(result.content)
#     print(playlist_id)
    df_playlist.loc[df_playlist['id'] == playlist_id, 'followers'] = json_result['followers']['total']

    #creating data frame to add songs
    df_songs_in_playlist=pd.DataFrame()
    df_songs_in_playlist['songs']=np.NaN

    for idx, songs_play_list in enumerate(json_result['tracks']['items']):
        try:
            df_songs_in_playlist.loc[idx,'songs']=(songs_play_list['track']['name']) #some dic are without name value..
            df_songs_in_playlist['playlist_id']=playlist_id
            df_songs_in_playlist.loc[idx,'artists']=songs_play_list['track']['album']['artists'][0]['name']
            df_songs_in_playlist.loc[idx,'popularity']=songs_play_list['track']['popularity']
            df_songs_in_playlist.loc[idx,'song_id']=songs_play_list['track']['id']            
        except:
            error=0
    df_songs_in_playlist_final=pd.concat([df_songs_in_playlist_final,df_songs_in_playlist],ignore_index=True)

df_songs_in_playlist_final


# In[26]:


# saving in cvs format
# df_songs_in_playlist_final.to_csv('?df_songs_in_playlist_final.csv')
# df_songs_in_playlist_final=pd.read_csv('df_songs_in_playlist_final.csv')
# df_songs_in_playlist_final


# ## Playlist analysis

# In[20]:


# How many unique playlists?
len(df_playlist['id'].unique())


# In[30]:


#Checking top playlists, the first two are from spotify
top_playlists=df_playlist[['name','followers','treated_URL','id']].drop_duplicates().sort_values(by=['followers'],ascending=False).head(20)
pd.set_option('display.max_colwidth', None) # show the text
top_playlists.head(20)


# In[31]:


#Checking in which country the BR playlists are consumed
agg_playlist=(df_playlist[['name','id','country']]).groupby(['id','name'])['country'].agg(list).reset_index()
agg_playlist=pd.merge(agg_playlist,df_playlist[['id','followers']].drop_duplicates(), on='id', how= 'left')
pd.DataFrame(agg_playlist).sort_values(by=['followers'],ascending=False).head(20)


# In[114]:


#Creating a chart
top_playlists=top_playlists[(top_playlists['name']!='This Is Beyoncé')&
                            (top_playlists['name']!='Beyoncé Radio')].sort_values(by=['followers'])

colors = ['silver',] * 18
colors[14] = 'royalblue'
colors[11] = 'royalblue'
colors[6] = 'royalblue'
colors[1] = 'royalblue'


fig = go.Figure(data=[go.Bar(
    y=top_playlists['name'],
    x=top_playlists['followers'],
    orientation='h',
    marker_color=colors # marker color can be a single color value or an iterable
)])
# fig.update_layout(
#     plot_bgcolor='black'
# )

# fig.update_layout(plot_bgcolor = "#23262F",
#                   title = {'x':0.5}, 
#                   font = {"family" : "courier"})

fig.update_layout(title_text='Top 18 user-created playlists',
                  plot_bgcolor='black',
                  paper_bgcolor='black',
                  yaxis_title="Playlist name",
                  xaxis_title="Followers (likes)",          
                  font=dict(size = 11, color = 'white',family="Courier New"),
                  margin=dict(l=0,r=10, b=50,t=50)
                 )

fig.update_xaxes(showline=True, linewidth=2, gridcolor='lightgrey')


# In[126]:


#Saving the plot
pio.write_image(fig, 'my_chart_final.png', width=1000, height=550, scale=3)


# In[49]:


#Checking if the playlists have the top tracks
df_songs_in_playlist_final_2=pd.merge(df_songs_in_playlist_final,df_top_tracks, on='song_id', how='left')
df_songs_in_playlist_final_2.rename(columns={'song':'is_top_10'}, inplace=True)
df_songs_in_playlist_final_2['is_top_10']=np.where(df_songs_in_playlist_final_2['is_top_10']==df_songs_in_playlist_final_2['songs'], True, False)

# checking which play lists are the top 20 playlists
df_songs_in_playlist_final_2=pd.merge(df_songs_in_playlist_final_2,
                                      top_playlists[['id','name']].rename(columns={'id':'playlist_id'}), 
                                      on='playlist_id',
                                      how='left')

# If is not nan, there is a macth with top playlist sd
df_songs_in_playlist_final_2['is_top_playlist']=np.where(pd.isna(df_songs_in_playlist_final_2['name'])==False, True, False)
df_songs_in_playlist_final_2['artist_is_beyonce']=np.where(df_songs_in_playlist_final_2['artists']=='Beyoncé', True, False)
df_songs_in_playlist_final_2


# In[89]:


df_songs_in_playlist_final_2


# In[125]:


top_10_by_playlist=df_songs_in_playlist_final_2[df_songs_in_playlist_final_2['is_top_playlist']==True].groupby(['name','playlist_id', 'is_top_10',]).size().unstack(fill_value=0).reset_index()
top_10_by_playlist.sort_values(by=True, ascending=False).rename(columns={True:'Top tracks',False:'Non top tracks','name':'Playlist name'})[['Playlist name','Non top tracks','Top tracks']]


# In[90]:


#For the top playlists, what is the percentage of songs that Beyonce is the author?
artist_songs_by_playlist=df_songs_in_playlist_final_2[df_songs_in_playlist_final_2['is_top_playlist']==True].groupby(['name','playlist_id', 'artist_is_beyonce',]).size().unstack(fill_value=0).reset_index()
artist_songs_by_playlist['percentage_artist_is_beyonce']=100*round(artist_songs_by_playlist[True]/(artist_songs_by_playlist[False]+artist_songs_by_playlist[True]),2)
artist_songs_by_playlist.sort_values(by='percentage_artist_is_beyonce', ascending=False)


# In[91]:


#Average popularity by playlist

df_aux=df_songs_in_playlist_final_2[df_songs_in_playlist_final_2['is_top_playlist']==True].groupby(['playlist_id'])['popularity'].agg(['mean','count']).reset_index()
df_aux.rename(columns={'mean':'mean_popularity','count':'count_popularity'},inplace=True)

artist_songs_by_playlist=pd.merge(artist_songs_by_playlist, df_aux, on='playlist_id', how='left')

artist_songs_by_playlist


# In[108]:


artist_songs_by_playlist.sort_values(by='percentage_artist_is_beyonce',ascending=False)


# In[111]:


#Chart with popularity and % of Beyonce songs
colors = ['silver',] * 18
colors[16] = 'royalblue'
colors[10] = 'royalblue'
colors[9] = 'royalblue'
colors[8] = 'royalblue'

fig = go.Figure(data=go.Scatter(
    x=artist_songs_by_playlist['percentage_artist_is_beyonce'],
    y=artist_songs_by_playlist['mean_popularity'],
    mode='markers',
    marker_color=colors,
    text=artist_songs_by_playlist['name'],
    marker=dict(size=artist_songs_by_playlist['count_popularity'])
))

fig.update_layout(title_text='Beyoncé songs on playlists versus popularity',
                  plot_bgcolor='black',
                  paper_bgcolor='black',
                  yaxis_title="Average popularity",
                  xaxis_title="Percentage of Beyoncé songs",          
                  font=dict(size = 13, color = 'white',family="Courier New"),
                  margin=dict(l=0,r=10, b=50,t=50)
                 )

fig.update_xaxes(showline=True, linewidth=2, gridcolor='lightgrey')
# fig.update_xaxes(range=[60, 10])
fig.update_xaxes(range=[60, 110])
fig.show()


# In[127]:


#Saving
pio.write_image(fig, 'my_scatter_final.png', width=1000, height=550, scale=3)
fig.write_html("plotly_chart.html")


# In[ ]:




