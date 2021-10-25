"""This module provides functions for searching and processing user inputs"""
import sys
from typing import List

from librespot.audio.decoders import AudioQuality
from tabulate import tabulate

from album import download_album, download_artist_albums
from const import TRACK, NAME, ID, ARTIST, ARTISTS, ITEMS, TRACKS, EXPLICIT, ALBUM, ALBUMS, \
    OWNER, PLAYLIST, PLAYLISTS, DISPLAY_NAME, TYPE
from playlist import get_playlist_songs, get_playlist_info, download_playlist, \
    download_from_user_playlist
from podcast import download_episode, get_show_episodes
from track import download_track, get_saved_tracks
from utils import sanitize_data, splash, split_input, regex_input_for_urls
from zspotify import ZSpotify

SEARCH_URL = 'https://api.spotify.com/v1/search'


def client() -> None:
    """ Connects to spotify to perform query's and get songs to download """
    ZSpotify()
    splash()

    if ZSpotify.check_premium():
        print('[ DETECTED PREMIUM ACCOUNT - USING VERY_HIGH QUALITY ]\n\n')
        ZSpotify.DOWNLOAD_QUALITY = AudioQuality.VERY_HIGH
    else:
        print('[ DETECTED FREE ACCOUNT - USING HIGH QUALITY ]\n\n')
        ZSpotify.DOWNLOAD_QUALITY = AudioQuality.HIGH

    if len(sys.argv) > 1:
        process_sysargs_input()
    else:
        search_text = ''
        while len(search_text) == 0:
            search_text = input('Enter search or URL: ')

        process_url_input(search_text, call_search=True)


def process_sysargs_input():
    """Process the sysargs given by the user"""
    if sys.argv[1] == '-p' or sys.argv[1] == '--playlist':
        download_from_user_playlist()
    elif sys.argv[1] == '-ls' or sys.argv[1] == '--liked-songs':
        for song in get_saved_tracks():
            if not song[TRACK][NAME]:
                print(
                    '###   SKIPPING:  SONG DOES NOT EXIST ON SPOTIFY ANYMORE   ###')
            else:
                download_track(song[TRACK][ID], 'Liked Songs/')
            print('\n')
    else:
        process_url_input(sys.argv[1])


def process_url_input(url, call_search=True):
    """Process the url input and calls appropriate method for downloading"""
    track_id, album_id, playlist_id, episode_id, show_id, artist_id = regex_input_for_urls(url)

    if track_id:
        download_track(track_id)
    elif artist_id:
        download_artist_albums(artist_id)
    elif album_id:
        download_album(album_id)
    elif playlist_id:
        playlist_songs = get_playlist_songs(playlist_id)
        name, _ = get_playlist_info(playlist_id)
        for song in playlist_songs:
            download_track(song[TRACK][ID],
                           sanitize_data(name) + '/')
            print('\n')
    elif episode_id:
        download_episode(episode_id)
    elif show_id:
        for episode in get_show_episodes(show_id):
            download_episode(episode)
    elif call_search:
        search(url)


def search(search_term):
    """ Searches Spotify's API for relevant data """
    params = {'limit': '10',
              'offset': '0',
              'q': search_term,
              TYPE: 'track,album,artist,playlist'}

    # Parse args
    process_split_input(search_term.split(), params)

    if len(params[TYPE]) == 0:
        params[TYPE] = 'track,album,artist,playlist'

    # Clean search term
    search_term_list = []
    for split in search_term.split():
        if split[0] == "-":
            break
        search_term_list.append(split)
    if not search_term_list:
        raise ValueError("Invalid query.")
    params["q"] = ' '.join(search_term_list)

    resp = ZSpotify.invoke_url_with_params(SEARCH_URL, **params)

    data = []
    total_tracks = 0
    if TRACK in params[TYPE].split(','):
        tracks = resp[TRACKS][ITEMS]
        total_tracks = process_tracks_input(tracks, data, 1)

    total_albums = 0
    if ALBUM in params[TYPE].split(','):
        albums = resp[ALBUMS][ITEMS]
        total_albums = process_album_input(albums, data, total_tracks)

    total_artists = 0
    if ARTIST in params[TYPE].split(','):
        artists = resp[ARTISTS][ITEMS]
        total_artists = process_artist_input(artists, data, total_tracks + total_albums)

    total_playlists = 0
    if PLAYLIST in params[TYPE].split(','):
        playlists = resp[PLAYLISTS][ITEMS]
        total_playlists = process_playlist_input(playlists,
                                                 data, total_tracks + total_albums + total_artists)

    if total_tracks + total_albums + total_artists + total_playlists == 0:
        print('NO RESULTS FOUND - EXITING...')
    else:
        selection = ''
        while len(selection) == 0:
            selection = str(input('SELECT ITEM(S) BY S.NO: '))
        process_user_selection(selection, data)


def process_split_input(splits, params):
    """Process the user input by splitting into multiple strings"""
    for index, split in enumerate(splits):

        if split[0] == '-' and len(split) > 1 and len(splits) - 1 == index:
            raise IndexError(f'No parameters passed after option: {split}\n')

        if split in ('-l', '-limit'):
            try:
                int(splits[index + 1])
            except ValueError as err:
                raise ValueError(f'Parameter passed after {split}'
                                 f' option must be an integer.\n') from err
            if int(splits[index + 1]) > 50:
                raise ValueError('Invalid limit passed. Max is 50.\n')
            params['limit'] = splits[index + 1]

        if split in ('-t', '-type'):
            params[TYPE] = ','.join(check_for_allowed_types(splits, split, index))


def check_for_allowed_types(splits, split, current_index) -> List[str]:
    """Checks for the allowed types in users input"""
    allowed_types = ['track', 'playlist', 'album', 'artist']
    passed_types = []
    for index in range(current_index + 1, len(splits)):
        if splits[index][0] == '-':
            break

        if splits[index] not in allowed_types:
            types = '\n'.join(allowed_types)
            raise ValueError(f'Parameters passed after {split}'
                             f' option must be from this list:\n{types}')

        passed_types.append(splits[index])
    return passed_types


def process_tracks_input(tracks: list, data: list, prev_total: int) -> int:
    """Process the track input and prints the related result for user search"""
    counter = prev_total
    if len(tracks) > 0:
        print('###  TRACKS  ###')
        track_data = []
        for track in tracks:
            explicit = '[E]' if track[EXPLICIT] else ''
            track_data.append([counter, f'{track[NAME]} {explicit}',
                               ','.join([artist[NAME] for artist in track[ARTISTS]])])
            data.append({
                ID: track[ID],
                NAME: track[NAME],
                TYPE: TRACK,
            })
            counter += 1
        print(tabulate(track_data, headers=[
            'S.NO', 'Name', 'Artists'], tablefmt='pretty'))
        print('\n')
        del tracks
        del track_data
        return counter - prev_total
    return 0


def process_album_input(albums: list, data: list, prev_total: int) -> int:
    """Process the album input and prints the related result for user search"""
    counter = prev_total
    if len(albums) > 0:
        print('###  ALBUMS  ###')
        album_data = []
        for album in albums:
            album_data.append([counter + 1, album[NAME],
                               ','.join([artist[NAME] for artist in album[ARTISTS]])])
            data.append({
                ID: album[ID],
                NAME: album[NAME],
                TYPE: ALBUM,
            })

            counter += 1
        print(tabulate(album_data, headers=[
            'S.NO', 'Album', 'Artists'], tablefmt='pretty'))
        print('\n')
        del albums
        del album_data
        return counter - prev_total
    return 0


def process_artist_input(artists: list, data: list, prev_total: int) -> int:
    """Process the artist input and prints the related result for user search"""
    counter = prev_total
    if len(artists) > 0:
        print('###  ARTISTS  ###')
        artist_data = []
        for artist in artists:
            artist_data.append([counter + 1, artist[NAME]])
            data.append({
                ID: artist[ID],
                NAME: artist[NAME],
                TYPE: ARTIST,
            })
            counter += 1
        print(tabulate(artist_data, headers=[
            'S.NO', 'Name'], tablefmt='pretty'))
        print('\n')
        del artists
        del artist_data
        return counter - prev_total
    return 0


def process_playlist_input(playlists: list, data: list, prev_total: int) -> int:
    """Process the playlist input and prints the related result for user search"""
    counter = prev_total
    if len(playlists) > 0:
        print('###  PLAYLISTS  ###')
        playlist_data = []
        for playlist in playlists:
            playlist_data.append(
                [counter + 1, playlist[NAME], playlist[OWNER][DISPLAY_NAME]])
            data.append({
                ID: playlist[ID],
                NAME: playlist[NAME],
                TYPE: PLAYLIST,
            })
            counter += 1
        print(tabulate(playlist_data, headers=[
            'S.NO', 'Name', 'Owner'], tablefmt='pretty'))
        print('\n')
        del playlists
        del playlist_data
        return counter - prev_total
    return 0


def process_user_selection(selection, data):
    """Process the user selection and calls appropriate download method"""
    inputs = split_input(selection)
    for pos in inputs:
        position = int(pos)
        for dic in data:
            print_pos = data.index(dic) + 1
            if print_pos == position:
                if dic[TYPE] == TRACK:
                    download_track(dic[ID])
                elif dic[TYPE] == ALBUM:
                    download_album(dic[ID])
                elif dic[TYPE] == ARTIST:
                    download_artist_albums(dic[ID])
                else:
                    download_playlist(dic)
