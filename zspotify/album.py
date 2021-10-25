from tqdm import tqdm

from const import ITEMS, ARTISTS, NAME, ID
from track import download_track
from utils import sanitize_data
from zspotify import ZSpotify

ALBUM_URL = 'https://api.spotify.com/v1/albums'
ARTIST_URL = 'https://api.spotify.com/v1/artists'


def get_album_tracks(album_id):
    """ Returns album tracklist """
    songs = []
    offset = 0
    limit = 50

    while True:
        resp = ZSpotify.invoke_url_with_params(f'{ALBUM_URL}/{album_id}/tracks', limit=limit, offset=offset)
        offset += limit
        songs.extend(resp[ITEMS])
        if len(resp[ITEMS]) < limit:
            break

    return songs


def get_album_name(album_id):
    """ Returns album name """
    resp = ZSpotify.invoke_url(f'{ALBUM_URL}/{album_id}')
    return resp[ARTISTS][0][NAME], sanitize_data(resp[NAME])


def get_artist_albums(artist_id):
    """ Returns artist's albums """
    resp = ZSpotify.invoke_url(f'{ARTIST_URL}/{artist_id}/albums')
    # Return a list each album's id
    album_ids = [resp[ITEMS][i][ID] for i in range(len(resp[ITEMS]))]
    # Recursive requests to get all albums including singles an EPs
    while resp['next']:
        resp = ZSpotify.invoke_url(resp['next'])
        album_ids.extend([resp[ITEMS][i][ID] for i in range(len(resp[ITEMS]))])

    return album_ids


def download_album(album):
    """ Downloads songs from an album """
    artist, album_name = get_album_name(album)
    tracks = get_album_tracks(album)
    for n, track in tqdm(enumerate(tracks, start=1), unit_scale=True, unit='Song', total=len(tracks)):
        download_track(track[ID], f'{artist}/{album_name}',
                       prefix=True, prefix_value=str(n), disable_progressbar=True)


def download_artist_albums(artist):
    """ Downloads albums of an artist """
    albums = get_artist_albums(artist)
    for album_id in albums:
        download_album(album_id)
