from email.mime import audio
import os
import eyed3
import spotipy
import sys
import ssl
import urllib.request
from PIL import Image
from pathlib import Path

from spotipy.oauth2 import SpotifyClientCredentials

print(sys.version)

TITLE = 'Title'
ARTIST = 'Artist'
ALBUM = 'Album'
TRACK_NUMBER = 'Track Number'
ARTWORK = "Artwork"

CLIENT_ID = 'c161d4925b3f47fd85c494d46ce24306';
CLIENT_SECRET = 'd337bb874321436ab41434d01c07b122';

client_credentials = SpotifyClientCredentials(client_id=CLIENT_ID, 
                                              client_secret=CLIENT_SECRET)

def tag(parameters, filename, directory):
    file_path = directory + filename
    print(file_path)
    audio_file = eyed3.load(file_path)

    audio_file.tag._setTitle(None)
    audio_file.tag._setArtist(None)
    audio_file.tag._setAlbum(None)
    audio_file.tag._setAlbumArtist(None)
    audio_file.tag._setGenre(None)

    for y in audio_file.tag.images:
        image_description = y.description
        audio_file.tag.images.remove(image_description)

    audio_file.tag._comments.remove('')
    audio_file.tag.lyrics.remove('')
    audio_file.tag.comments.remove('')
    audio_file.tag.composer=None
    audio_file.tag.copyright=None
    audio_file.tag.encoded_by=None
    audio_file.tag.original_artist=None
    audio_file.tag.publisher=None

    if parameters[TITLE]:
        audio_file.tag.title = parameters[TITLE]
    if parameters[ARTIST]:
        audio_file.tag.artist = parameters[ARTIST]
    if parameters[ALBUM]:
        audio_file.tag.album = parameters[ALBUM]
    if parameters[TRACK_NUMBER]:
        audio_file.tag.track_num = parameters[TRACK_NUMBER]
    if parameters[ARTWORK]:
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(parameters[ARTWORK],"temp.jpg")
        imagedata = open("temp.jpg","rb").read()
        audio_file.tag.images.set(3, imagedata, 'image/jpeg','None')
        os.remove("temp.jpg")

    try:
        audio_file.rename(str(parameters[ARTIST])+" - "+str(parameters[TITLE]))
    except OSError:
        pass

    audio_file.tag.save()
    

def search(query):
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials);
    parsed_query = f"{query[TITLE]} {query[ARTIST]}"
    results = spotify.search(q = parsed_query, type = 'track')
    results = results['tracks']['items']

    for index, item in enumerate(results, 1):

        artists=""
        x=1
        for artist in item['artists']:
            artist = artist['name']
            if len(item['artists'])>x:
                artists = artists+artist+", "
            else:
                artists = artists+artist
            x+=1

        print(f"{index}.\n\t"
            f"Track: {item['name']}\n\t"
            f"Artist: {artists}\n\t"
            f"Album: {item['album']['name']}\n\t"
            f"Track number: {item['track_number']}\n\t"
            f"Artwork URL: {item['album']['images'][0]['url']}")
    
    try:
        selection = results[0]
        print("\nSelecting first result by default...")
        #else:
        # print("Selecting first result by default...")
        # choice = int(input('\nEnter choice: '))
        # choice = 1
        # selection = results[choice - 1]

        params = dict()
        params[TITLE] = selection['name']
        params[ARTIST] = artists
        params[ALBUM] = selection['album']['name']
        params[TRACK_NUMBER] = selection['track_number']
        params[ARTWORK] = selection['album']['images'][0]['url']
    except IndexError:
        selection = "null"
        params = "null"
        print("\n*** There are no results for this query. ***\n")

    return params

def main():

    print("\n***** Welcome to the MP3 decluttering tool! *****\n")
    print("Looking for MP3 files in your DOWNLOADS folder...")
    directory = str(Path.home() / "Downloads")+"/"

    nberrors=0
    i=0
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            i+=1
            filename2 = filename.split('[')[0].rstrip()
            filename2 = filename2.split('.mp3')[0]
            print("Current MP3 File: \n" + filename)

            try:
                songName = str(filename2).split(' - ')[1].rstrip()
                songName = str(songName).split('(Original')[0].rstrip()
                songName = str(songName).split('(Extended')[0].rstrip()
                artists = str(filename2).split(' - ')[0].rstrip()
                artist1 = str(artists).split(' &')[0].rstrip()
                artist1 = str(artist1).split(',')[0].rstrip()
                artist1 = str(artist1).split('ft')[0].rstrip()
                artist1 = str(artist1).split('feat')[0].rstrip()
                print("artist: \n" + artists)
                print("songName: \n" + songName)
            except IndexError:
                songName = str(filename2)
                artist1=""

            query = menu(artist1, songName)
            parameters = search(query)
            if parameters!='null':
                tag(parameters, filename, directory)
            else:
                nberrors+=1
            
    if nberrors>1:
        print("\n* "+str(nberrors)+" files were not found on Spotify. Please update their name structure and try again.")
    elif nberrors==1:
        print("\n* 1 file was not found on Spotify. Please update its name structure and try again.")

    if i==0:
        print("\nERROR: There are no MP3 files to tag in "+directory+".\n")
    else:
        print("\nCompleted mp3 tagging in "+directory+".\n")

def menu(artist, songName):
    #print('\nPlease validate the song name and the artist name from Spotify.')
    params = dict();
    params[TITLE] = songName;
    params[ARTIST] = artist;

    return params

main ()