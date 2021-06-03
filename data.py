import collections
import datetime

PATH = r"Pink_Floyd_DB.txt"


def dbase():
    """
    This function organise the data base to a difficult build
    :return: the difficult build
    """
    albums_data = {}
    song_dict = {}
    songs_list = []
    with open(PATH, 'r') as f:
        data = f.read()
        temp = data.split("#")
        for album in temp[1:]:
            index = album.find("::")
            albums_data[album[:index]] = ""
        for album in temp[1:]:
            album = album.split("*")
            album_name = album[0][:-7]
            release_Date = album[0][-5:]
            del album[0]
            for song in album:
                info = song.split("::")
                song_name = info[0]
                del info[0]
                songs_list = info
                song_dict[song_name] = songs_list
            albums_data[album_name] = (song_dict.copy(), release_Date)
            song_dict.clear()
        return albums_data


def simple_songs_list(name_of_album):
    """
    this func is from using insde the data file
    :param name_of_album: the name of album
    :return: the songs in this album
    :rtype: str
    """
    songs = []
    data1 = dbase()
    data1 = data1[name_of_album][0]
    for song in data1.keys():
        songs += [song]
    return songs


def simple_album_list():
    """
    this func is from using insde the data file
    :return: list of all albums
    :rtype: list
    """
    album_list = []
    data = dbase()
    for album in data.keys():
        album_list += [album]
    return album_list


def album_list_for_user():
    """
    this func makes a list of all the album
    :return: list of all albums
    :rtype: str
    """
    answer = ""
    data = dbase()
    for album in data.keys():
        answer += album + ", "
    return answer[:-2]


def songs_list(name_of_album):
    """
    This function makes a list of all the songs in album
    :param name_of_album: the album
    :return: all the songs in the album
    :rtype: str
    """
    songs = ""
    data = dbase()
    data = data[name_of_album][0]
    for song in data.keys():
        songs += song
        songs += ", "
    return songs[:-2]


def get_len(song, album):
    """
    This func calc the number of words in one song
    :param song: the song
    :param album: in what album the song is
    :return: the length
    :rtype: str
    """
    length = 0
    words = dbase()[album][0][song]
    words = words[2]
    words = words.split()
    for word in words:
        length += 1
    return str(length)


def song_length(ans):
    """
    This func calc how many words there is in all of the songs, albums. using "get_len" function
    :param ans: the answer from the user
    :return: the length of all the songs
    :rtype: str
    """
    length = 0
    flag = 1
    albums = simple_album_list()
    for album in albums:
        songs = simple_songs_list(album)
        for song in songs:
            if ans == song:
                words = dbase()[album][0][song]
                words = words[2]
                words = words.split()
                for word in words:
                    length += 1
                    flag = 1
                return str(length)

            elif ans != song and flag == 0:
                return "song not found!"


def song_lyrics(ans):
    """
    This function returns the lyrics of specific song
    :param ans: the answer from the user
    :return: the lyrics of the song
    :rtype: str
    """
    albums = simple_album_list()
    for album in albums:
        songs = simple_songs_list(album)
        for song in songs:
            if ans == song:
                words = dbase()[album][0][song]
                words = words[2]
                return words


def song_album(ans):
    """
    This function finds what album the song in
    :param ans: the song
    :return: the album
    :rtype: str
    """
    albums = simple_album_list()
    for album in albums:
        songs = simple_songs_list(album)
        for song in songs:
            if ans == song:
                return album


def song_by_word(ans):
    """
    This func finds a song by a string from the user(by name)
    :param ans: the string from the user
    :return: list of the songs
    :rtype: str
    """
    songs_list = ""
    ans = ans.lower()
    albums = simple_album_list()
    for album in albums:
        songs = simple_songs_list(album)
        for song in songs:
            song = str(song)
            if ans in song.lower():
                songs_list += song + ", "
    return songs_list[:-2]


def lyrics_by_word(ans):
    """
    This func finds a song by a string from the user(by lyrics)
    :param ans: the string from the user
    :return: list of the songs
    :rtype: str
    """
    songs_list = ""
    ans = ans.lower()
    albums = simple_album_list()
    for album in albums:
        songs = simple_songs_list(album)
        for song in songs:
            x = song_lyrics(song)
            song = str(song)
            if ans in x:
                songs_list += song + ", "
    return songs_list[:-2]


def common():
    """
    This function makes list of the top 50 commonest words of all songs
    :return: the stats
    :rtype: str
    """
    full_song = ""
    albums = simple_album_list()
    for album in albums:
        songs = simple_songs_list(album)
        for song in songs:
            full_song += str(song_lyrics(song))
    split_lyrics = full_song.lower().split()
    counter = collections.Counter(split_lyrics)
    most_words = counter.most_common(50)
    return most_words


def stats():
    """
    This function makes list of the top 50 commonest words of all songs
    :return: list with the sorted length values
    :rtype: str
    """
    times_lst = []
    time_dict = {}
    for album, details in dbase().items():
        time_m = 0
        time_s = 0
        for songs, details_s in details[0].items():
            time = details_s[1].split(":")
            min = int(time[0])
            sec = int(time[1])
            time_m += min
            time_s += sec
        time_s = datetime.timedelta(seconds=time_s)
        time_m = datetime.timedelta(seconds=time_m)
        time = time_m + time_s
        time = str(time)
        times_lst.append(time)
        time_dict[album] = time

    time_dict = sorted(time_dict.items(), key=lambda x: x[1], reverse=True)
    return time_dict


def organise(times, words):
    """
    This function organise the two answer to one answers
    :param times: list with the sorted length values
    :param words: list of all of the commonest words of all songs
    :return: one organise answer
    :rtype: str
    """
    length_lst = ""
    comm_lst = ""
    for item in times:
        length_lst += str(item[0]) + " - " + str(item[1]) + "\n"
    for item in words:
        comm_lst += str(item[0]) + " - " + str(item[1]) + "\n"

    return length_lst, comm_lst


