# SpoTempo
SpoTempo **sorts tracks** from a Spotify playlist **by tempo**, and creates a new playlist with the sorted tracks in either ascending or descending order. 

# What You Will Need
- Spotify account
- Spotify client id (tutorial below)
- Spotify client secret (tutorial below)

# Set Up
**1. Get Spotify client id and client secret, and set redirect URI**
- Visit https://developer.spotify.com/dashboard/

- Create an app 

![alt text](https://github.com/codycoogan/metronomeforlifx/blob/master/images/spotclient.gif)

- Here are your client id and client secret
![alt text](https://github.com/codycoogan/metronomeforlifx/blob/master/images/spotblurred_g.jpg)

- Press edit settings, then once in the Spotify project settings add https://www.google.com/ as the redirect URI


**2. Fill out config.txt** 
- Open config.txt
- Paste your Spotify client id, secret, and spotify username in the respective spots in the file
- Save the file


**3. Download requirements.txt**
- After downloading requirements.txt open terminal or command prompt
- Go to the directory where this project is saved in
- Run: pip install -r requirements.txt    in the command line to install the necessary libraries


**4. Sign in to Spotify in SpoTempo app**
- Run spotempo.py in terminal/command prompt
- Sign in to Spotify account when prompted in browser
- If sign in was successful, copy the URL of the page that you were redirected to after signing in (google.com/...). This is for Spotify authorization purposes. (If sign in is unsuccessful re-run the program and attempt to sign in again)
- Paste this URL into prompt in command line

# Troubleshooting
- Make sure config.txt is filled out with valid information
- Make sure config.txt, requirements.txt, and spotempo.py are all in the same directory on your computer
- Make sure you have https://www.google.com/ saved as the redirect URI in your Spotify app settings
- Make sure the playlist you would like to sort is in your first 50 playlists. You can rearrange your playlists and/or playlists you follow to make sure they are in your first 50. 
