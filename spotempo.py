import spotipy.util as util
import requests
import json
import math

scope = "playlist-modify-public playlist-read-private playlist-modify-private playlist-read-collaborative"


def main():
    # Get information from config.txt file for authorization
    dicti = get_info()
    username = dicti["username"]
    client_id = dicti["client_id"]
    client_secret = dicti["client_secret"]
    spot_token = spotify_authenticate(username, scope, client_id, client_secret)
    header = {
        "Authorization": "Bearer {}".format(spot_token)
    }

    name = raw_input("Name of playlist you would like to arrange by tempo: ").strip()

    # Get list of top 50 playlists
    playlists_req = requests.get("https://api.spotify.com/v1/users/{}/playlists?limit=50".format(username),
                                 headers=header)
    playlists_names = playlists_req.json()["items"]
    found = False
    # Get each playlist, make it lowercase and put it in a list
    for pl in playlists_names:
        low_name = pl["name"].lower()
        if low_name == name.lower():
            found = True
            playlist_id = pl["id"]
            num_of_songs = pl["tracks"]["total"]
            print "Playlist found. Number of tracks: " + str(num_of_songs)
            break
    if not found:
        print "Unable to find playlist: make sure it is in your first 50 playlists and you spell the name correctly"
        exit()

    # User chooses if they want new play list in ascending or descending order
    arrangement = raw_input("Would you like to arrange this playlist in\n"
                            "1) Ascending order (Low to high tempos)\n"
                            "2) Descending order (High to low tempos)\n"
                            "Enter either 1 or 2: ").strip()

    if arrangement != str(1) and arrangement != str(2):
        while arrangement != str(1) and arrangement != str(2):
            arrangement = raw_input("Please enter a 1 or 2: ").strip()

    # Have user choose name of new playlist
    new_name = raw_input("Name of new playlist: ").strip()

    print "Getting songs and tempos... "

    # Get each song and tempo in sets of 100 (because of API limits)
    tempos = []
    noq_round = int(math.ceil(num_of_songs / 100.0))
    for i in xrange(0, noq_round):
        # Get all the tracks in the playlist
        tr_names = []
        tr_ids = []
        queryparam = ""
        get_pl = requests.get("https://api.spotify.com/v1/playlists/{}/tracks?offset={}".format(playlist_id, i * 100),
                              headers=header)
        items = get_pl.json()["items"]
        for item in items:
            tr_names.append(item["track"]["name"])
            tr_ids.append(item["track"]["id"])
            queryparam += str(item["track"]["id"]) + ","
        tempo_req = requests.get("https://api.spotify.com/v1/audio-features?ids="+queryparam[0:-1], headers=header)
        trjson = tempo_req.json()["audio_features"]
        # Get tempo for each song and add the name, tempo, and id of the song to tempos
        for t in xrange(0, len(trjson)):
            try:
                tempos.append((tr_names[t], trjson[t]["tempo"], tr_ids[t]))
            except TypeError:  # When a song doesn't exist
                print "Error with a song"

    # Sort the list of songs by tempo
    if arrangement == str(1):
        tempos.sort(key=lambda x: x[1])  # ascending order
        first = "lowest"
        second = "highest"
    else:
        tempos.sort(key=lambda x: x[1], reverse=True)  # descending order
        first = "highest"
        second = "lowest"

    headermake = {
        "Authorization": "Bearer {}".format(spot_token),
        "Content-Type": "application/json"
    }
    data = {
        "name": str(new_name),
        "description": name + " in order of tempo from {} to {} according to Spotify analysis".format(first, second)
    }
    # Create the new playlist
    enter = requests.post("https://api.spotify.com/v1/users/{}/playlists".format(username), data=json.dumps(data),
                          headers=headermake)
    if str(enter)[11:14] == str(201) or str(enter)[11:14] == str(200):  # If response was 200 or 201 (successful)
        print "Successfully made playlist"
        new_plid = enter.json()["id"]
    else:
        print "Unable to make playlist"
        print enter
        exit()

    # Add songs to playlist in sets of 100
    noq_round = int(math.ceil(len(tempos) / 100.0))
    for i in xrange(0, noq_round):
        uris_list = []
        # For each song in the list of songs sorted by their tempo
        for song in tempos[i * 100:(i * 100) + 100]:
            uris_list.append("spotify:track:" + str(song[2]))  # song[2] is the song's tempo
        uris = {"uris": uris_list}
        # Add songs to the new playlist
        adding_songs = requests.post("https://api.spotify.com/v1/playlists/{}/tracks".format(new_plid),
                                     data=json.dumps(uris),
                                     headers=headermake)
        # If response isn't successful
        if str(adding_songs)[11:14] != str(201) and str(adding_songs)[11:14] != str(200):
            print "Error adding songs"
            print adding_songs
            exit()

    # When everything is complete and successful
    print "Success! All songs have been added to new playlist"


def spotify_authenticate(username, scope, client_id, client_secret):
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, "https://www.google.com/")
    if token:
        return token
    else:
        print("Couldn't get proper Spotify authentication, please retry")
        exit()


def get_info():
    dicti = {}
    with open("config.txt", "r") as file:
        content = file.readlines()
        for line in content:
            if "=" in line:
                parts = line.split("=")
                if len(parts) == 2:
                    dicti[parts[0].strip()] = parts[1].strip()
                else:
                    print("Please fill out the config.txt file")
                    exit()
        return dicti


if __name__ == "__main__":
    main()
