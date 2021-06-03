import socket
import data
HOST = '127.0.0.1'
PORT = 9090
MAX = 9

protocol = {'101#': '201#<albums list>',
            '102#': '202#<songs list>',
            '103#': '203#<song length>',
            '104#': '204#<lyrics>',
            '105#': '205#<the_album>',
            '106#': '206#<songs list>',
            '107#': '207#<songs list>',
            '108#': '208#<stats>',
            '109#': '209#<good bay>'}


def choose_func(req, ans):
    """
    This function manege to what func to call based of the req
    :param req: the request (by the protocol)
    :param ans: if the is more details needed for a specific function to run
    :return: the vlues that returns from the called function
    """

    req = int(protocol[req][2])
    if req == 1:
        albums = data.album_list_for_user()
        return str(albums).encode()

    elif req == 2:
        songs = data.songs_list(ans)
        return str(songs).encode()

    elif req == 3:
        length = data.song_length(ans)
        return str(length).encode()

    elif req == 4:
        lyrics = data.song_lyrics(ans)
        return str(lyrics).encode()

    elif req == 5:
        album = data.song_album(ans)
        return str(album).encode()

    elif req == 6:
        songs = data.song_by_word(ans)
        return str(songs).encode()

    elif req == 7:
        songs = data.lyrics_by_word(ans)
        return str(songs).encode()
    elif req == 8:
        times, comm = data.organise(data.stats(), data.common())
        return str(times).encode(), str(comm).encode()

    elif req == MAX:
        exit()


def open_sock():
    """
    This function runs all of the connection details and make the connection work
    :return:
    """
    req = 0
    ans = 0
    welcome_massage = "welcome to pink floyd fans server!\n".encode()
    while req != MAX:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lst_sock:
            lst_sock.bind((HOST, PORT))
            lst_sock.listen(1)
            client_sock, client_adder = lst_sock.accept()
            with client_sock as sock:
                try:
                    sock.sendall(welcome_massage)
                    req = sock.recv(1024).decode()
                    if req != "101#" and req != "108#":
                        ans = sock.recv(1024).decode()
                        answer = choose_func(req, ans)
                        sock.sendall(answer)
                    elif req == "108#":
                        time, comm = choose_func(req, ans)
                        sock.sendall(time)
                        sock.sendall(comm)

                    else:
                        ans = 0
                        answer = choose_func(req, ans)
                        sock.sendall(answer)

                except ConnectionResetError:
                    print("client left")
                    exit()


def main():
    open_sock()


if __name__ == "__main__":
    main()
