import requests
import string
from json import loads
from urllib.parse import quote
from argparse import ArgumentParser


def get_song_data(song_name):
    song_json_data = requests.get(f"http://slider.kz/vk_auth.php?q={quote(song_name)}")
    return loads(song_json_data.text)


def extract_first_five_songs(song_parsed_data):
    data_of_five_songs = []
    song_data_keys = list(song_parsed_data['audios'].keys())
    index_cover = song_data_keys[0]
    for song_index in range(5):
        data_of_five_songs.append(song_parsed_data['audios'][index_cover][song_index])
    return data_of_five_songs


def generate_url(song_to_be_downloaded):
    return f"http://slider.kz/download/" \
        f"{song_to_be_downloaded['id']}/" \
        f"{song_to_be_downloaded['duration']}/" \
        f"{song_to_be_downloaded['url']}/" \
        f"{quote(song_to_be_downloaded['tit_art'])}.mp3?extra={song_to_be_downloaded['extra']}"


def get_download_link_and_title_for_first_five_songs_from_name(song_name):
    song_data = get_song_data(song_name)
    five_songs = extract_first_five_songs(song_data)
    title_and_link_of_songs = []
    for current_song in five_songs:
        song_title = current_song['tit_art']
        duration = current_song['duration']
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        song_title = ''.join(c for c in song_title if c in valid_chars)
        title_and_link_of_songs.append({'title': song_title, 'url': generate_url(current_song), 'duration': duration})
    return title_and_link_of_songs


def display_song_options_to_download_from(songs_to_download):
    for index, song in enumerate(songs_to_download):
        print(f"{index} -> {song['title']} - {song['duration']}")
    print("Enter song number to download")


def download_song(name):
    songs_to_download = get_download_link_and_title_for_first_five_songs_from_name(name)
    display_song_options_to_download_from(songs_to_download)
    song_to_download = songs_to_download[int(input())]
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
