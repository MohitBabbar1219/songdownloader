import requests
import string
from json import loads
from urllib.parse import quote
from argparse import ArgumentParser


def get_song_data(song_name):
    song_json_data = requests.get(f"http://slider.kz/vk_auth.php?q={quote(song_name)}")
    return loads(song_json_data.text)


def extract_first_n_songs(song_parsed_data, number_of_songs):
    data_of_five_songs = []
    song_data_keys = list(song_parsed_data['audios'].keys())
    index_cover = song_data_keys[0]
    available_options = song_parsed_data['audios'][index_cover]
    number_of_available_options = len(available_options)
    length_of_songs = number_of_songs if number_of_available_options >= number_of_songs else number_of_available_options
    for song_index in range(length_of_songs):
        data_of_five_songs.append(available_options[song_index])
    return data_of_five_songs


def generate_url(song_to_be_downloaded):
    return f"http://slider.kz/download/" \
        f"{song_to_be_downloaded['id']}/" \
        f"{song_to_be_downloaded['duration']}/" \
        f"{song_to_be_downloaded['url']}/" \
        f"{quote(song_to_be_downloaded['tit_art'])}.mp3?extra={song_to_be_downloaded['extra']}"


def get_download_link_and_title_for_first_n_songs_from_name(song_name, number_of_songs):
    song_data = get_song_data(song_name)
    n_songs = extract_first_n_songs(song_data, number_of_songs)
    title_and_link_of_songs = []
    for current_song in n_songs:
        song_title = current_song['tit_art']
        duration = current_song['duration']
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        song_title = ''.join(c for c in song_title if c in valid_chars)
        title_and_link_of_songs.append({'title': song_title, 'url': generate_url(current_song), 'duration': duration})
    return title_and_link_of_songs


def display_song_options_to_download_from(songs_to_download):
    for index, song in enumerate(songs_to_download):
        print(f"{index} -> {song['title']} - {song['duration']}")
    print("Enter song numbers to download (separated by space): ")


def validate_value_of_indexes(indexes, length_of_options):
    is_valid = True
    for index in indexes:
        is_valid = is_valid and (index > length_of_options - 1)


def download_song(name, number_of_songs=10):
    songs_to_download = get_download_link_and_title_for_first_n_songs_from_name(name, number_of_songs)
    display_song_options_to_download_from(songs_to_download)
    indexes_of_song_to_be_downloaded = input()
    try:
        split_indexes = [int(index) for index in indexes_of_song_to_be_downloaded.split(' ')]
    except ValueError:
        print("enter a valid index next time :/")
        return

    if validate_value_of_indexes(split_indexes, len(songs_to_download)):
        print("enter a valid index next time :/")
        return

    options_selected = [songs_to_download[index] for index in split_indexes]
    for option in options_selected:
        print(f"Downloading - {option['title']}...")
        r = requests.get(option['url'], allow_redirects=True)
        open(f"{option['title']}.mp3", 'wb').write(r.content)
        print('Done :)')


def command_line_song_download():
    parser = ArgumentParser()
    parser.add_argument("-s", "--song-name", dest="song_name",
                        help="download song with name", metavar="FILE")
    parser.add_argument("-n", "--number-of-options", dest="number_of_options",
                        help="maximum number of options to display for a search")
    args = parser.parse_args()
    download_song(args.song_name, int(args.number_of_options) or 10)


command_line_song_download()
