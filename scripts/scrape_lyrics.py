import lyrics_tools
# from translate import Translator
from googletrans import Translator
import pandas as pd
import lyricsgenius
import sys
from tqdm import tqdm
import json
import os

def init_genius_api(path_to_genius_config):
    """
    Initialize a session for the lyricsgenius package. The genius API from genius.com is used to scrap lyrics of songs.

    Parameters
    ----------
    path_to_genius_config : str
        Relative path to json file where the client access token for the genius API is stored.

    Returns
    -------
    lyricsgenius object
        Authenticated session for the lyricsgenius package.
    """
    with open(path_to_genius_config) as json_file:
        genius_config = json.load(json_file)
    return lyricsgenius.Genius(genius_config['Client_Access_Token'])


def scrape_lyrics(filename, path, genius, df):
    # df = df.drop_duplicates(subset=["track_id"], keep="last")
    if os.path.exists(f"{path}/{filename}.csv"):
        track_id_already_scraped = pd.read_csv(f"{path}/{filename}.csv").track_id.to_numpy()
    else:
        track_id_already_scraped = []
    track_name, track_artist, track_id = df.track_name, df.track_artist, df.track_id
    for idx, (name, artist, id) in tqdm(enumerate(zip(track_name, track_artist, track_id))):
        if id in list(track_id_already_scraped):
            continue
        try:
			# Download lyrics with the genius api
            song_lyrics = genius.search_song(name, artist).lyrics
            #song_lyrics = lyrics_tools.clean_lyrics(song_lyrics)
            #language = lyrics_tools.check_lang(translator, song_lyrics)
            #print(language)
            #if not language == 'en':
			    # translate lyrics to english, if needed
            #    song_lyrics = lyrics_tools.translate(translator, song_lyrics)


		    # merge the df with the track IDs with the downloaded lyrics
            lyrics_df = pd.DataFrame({"track_id": id, "lyrics": [song_lyrics]})
            lyrics_df.to_csv(f"{path}/{filename}.csv", mode='a', header=not os.path.exists(f"{path}/{filename}.csv"), index=False)
        except AttributeError:
            print(f'No lyrics available for track: {name} from {artist}.')
        except Exception as e:
            print(f'{e}\nContinue.')


def main():

    """
    Read the data csv as a DataFrame
    """
    name_v = "Viral"
    name_t = "Top"
    path = "Data/06_2023"
    df_t = pd.read_csv(f"{path}/{name_t}_playlists.csv")#, nrows=2)
    df_v = pd.read_csv(f"{path}/{name_v}_playlists.csv")#, nrows=2)
    df = pd.concat([df_t, df_v], ignore_index=True, sort=False)
    df = df.drop_duplicates(subset=["track_id"], keep="last")
    del df_t
    del df_v
    # translator = Translator(service_urls=[
    #   'translate.google.com',
    #   'translate.google.de',
    # ])
    # print(translator.detect('Hallo Welt.'))
    # sys.exit()
    
    #sys.exit()
	# initialise the genius api
    path_to_genius_config = "../config/genius_config.json"
    genius = init_genius_api(path_to_genius_config)
    filename = "track_id_lyrics.csv"
    scrape_lyrics(filename, path, genius, df)
    



if __name__ == "__main__":
    main()