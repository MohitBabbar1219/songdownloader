import requests
import string
from json import loads
from urllib.parse import quote
from argparse import ArgumentParser


def get_song_data(song_name):
    song_json_data = requests.get(f"http://slider.kz/vk_auth.php?q={quote(song_name)}")
    return loads(song_json_data.text)


def extract_first_song(song_parsed_data):
    index_cover = list(song_parsed_data['audios'].keys())[0]
    return song_parsed_data['audios'][index_cover][0]


def generate_url(song_to_be_downloaded):
    return f"http://slider.kz/download/" \
        f"{song_to_be_downloaded['id']}/" \
        f"{song_to_be_downloaded['duration']}/" \
        f"{song_to_be_downloaded['url']}/" \
        f"{quote(song_to_be_downloaded['tit_art'])}.mp3?extra={song_to_be_downloaded['extra']}"


def get_download_link_and_title_from_name(song_name):
    song_data = get_song_data(song_name)
    first_song = extract_first_song(song_data)
    song_title = first_song['tit_art']
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    song_title = ''.join(c for c in song_title if c in valid_chars)
    return {'title': song_title, 'url': generate_url(first_song)}


def download_song(name):
    song_to_download = get_download_link_and_title_from_name(name)
    print('Downloading...')
    r = requests.get(song_to_download['url'], allow_redirects=True)
    open(f"{song_to_download['title']}.mp3", 'wb').write(r.content)
    print('Done :)')


def command_line_song_download():
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", dest="song_name",
                        help="download song with name", metavar="FILE")
    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")
    args = parser.parse_args()
    download_song(args.song_name)


command_line_song_download()

# with open('songs.txt', 'r') as songs_file:
#     for song in songs_file.readlines():
#         print(song[:-1])
#         download_song(song[:-1])
