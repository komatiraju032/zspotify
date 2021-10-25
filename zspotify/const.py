"""This module provides the commonly used strings as constants"""
SANITIZE = ('\\', '/', ':', '*', '?', '\'', '<', '>', '"')

SAVED_TRACKS_URL = 'https://api.spotify.com/v1/me/tracks'

TRACKS_URL = 'https://api.spotify.com/v1/tracks'

TRACKNUMBER = 'tracknumber'

DISCNUMBER = 'discnumber'

YEAR = 'year'

ALBUM = 'album'

TRACKTITLE = 'tracktitle'

ARTIST = 'artist'

ARTISTS = 'artists'

ARTWORK = 'artwork'

TRACKS = 'tracks'

TRACK = 'track'

ITEMS = 'items'

NAME = 'name'

ID = 'id'

URL = 'url'

RELEASE_DATE = 'release_date'

IMAGES = 'images'

LIMIT = 'limit'

OFFSET = 'offset'

AUTHORIZATION = 'Authorization'

IS_PLAYABLE = 'is_playable'

TRACK_NUMBER = 'track_number'

DISC_NUMBER = 'disc_number'

SHOW = 'show'

ERROR = 'error'

EXPLICIT = 'explicit'

PLAYLIST = 'playlist'

PLAYLISTS = 'playlists'

OWNER = 'owner'

DISPLAY_NAME = 'display_name'

ALBUMS = 'albums'

TYPE = 'type'

PREMIUM = 'premium'

USER_READ_EMAIL = 'user-read-email'

PLAYLIST_READ_PRIVATE = 'playlist-read-private'

WINDOWS_SYSTEM = 'Windows'

CREDENTIALS_JSON = 'credentials.json'

CONFIG_FILE_PATH = '../zs_config.json'

ROOT_PATH = 'ROOT_PATH'

ROOT_PODCAST_PATH = 'ROOT_PODCAST_PATH'

SKIP_EXISTING_FILES = 'SKIP_EXISTING_FILES'

DOWNLOAD_FORMAT = 'DOWNLOAD_FORMAT'

FORCE_PREMIUM = 'FORCE_PREMIUM'

ANTI_BAN_WAIT_TIME = 'ANTI_BAN_WAIT_TIME'

OVERRIDE_AUTO_WAIT = 'OVERRIDE_AUTO_WAIT'

CHUNK_SIZE = 'CHUNK_SIZE'

SPLIT_ALBUM_DISCS = 'SPLIT_ALBUM_DISCS'

DURATION_MS = 'duration_ms'

ARTIST_ID = 'ArtistID'

SHOW_ID = 'ShowID'

EPISODE_ID = 'EpisodeID'

PLAYLIST_ID = 'PlaylistID'

ALBUM_ID = 'AlbumID'

TRACK_ID = 'TrackID'

CONFIG_DEFAULT_SETTINGS = {
    'ROOT_PATH': '../ZSpotify Music/',
    'ROOT_PODCAST_PATH': '../ZSpotify Podcasts/',
    'SKIP_EXISTING_FILES': True,
    'DOWNLOAD_FORMAT': 'mp3',
    'FORCE_PREMIUM': False,
    'ANTI_BAN_WAIT_TIME': 1,
    'OVERRIDE_AUTO_WAIT': False,
    'CHUNK_SIZE': 50000,
    'SPLIT_ALBUM_DISCS': False
}
