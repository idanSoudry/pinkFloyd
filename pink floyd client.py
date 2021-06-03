import socket
HOST = '127.0.0.1'
PORT = 9090
MAX = 9


def menu():
    """
    This function prints the menu and verifies in
    :return: Ihe user choice
    :rtype: Int
    """
    flag = 0
    choice = 0

    while flag == 0:    # make a loop until the answer is ok
        choice = int(input("""Enter a number between 1-8
1.Print albums list
2.Print list of songs in album
3.Print the number for words in song 
4.Print a songs lyrics
5.What album is the song on?
6.Search for a song by name
7.Search a song by lyrics in a song
8.Print the stats
9.EXIT
"""))
        if 1 <= choice <= MAX:  # verifies the answer
            flag = 1
        else:
            flag = 0
    return choice   # returns the verified choice


def convert_to_request(choice):
    """
    This function convert the users choice into a request(by the protocol)
    :param choice: The answer from the func 'menu'
    :type: Int
    :return: The request that matches the user's choice, and the answer from the user
    :rtype: Str
    """
    request = ''
    ans = ""
    if choice == 1:
        request = '101#'

    elif choice == 2:
        album = str(input("Enter a album: "))
        request = '102#'
        ans = album

    elif choice == 3:
        song = str(input("Enter a song: "))
        request = '103#'
        ans = song

    elif choice == 4:
        song = str(input("Enter a song: "))
        request = '104#'
        ans = song

    elif choice == 5:
        song = str(input("Enter a song: "))
        ans = song
        request = '105#'

    elif choice == 6:
        string = str(input("Enter a string: "))
        ans = string
        request = '106#'

    elif choice == 7:
        string = str(input("Enter a string: "))
        ans = string
        request = '107#'

    elif choice == 8:
        request = '108#'

    elif choice == 9:
        request = '109#'

    return request, ans


def open_sock():
    """
    This function open socket to the server and send it a request from the protocol
    :return: None
    """
    choice = 0
    while choice != MAX:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli_sock:
            server_adder = (HOST, PORT)
            try:
                cli_sock.connect(server_adder)
            except ConnectionRefusedError:
                print("server doesnt connected")
                exit()

            with cli_sock as sock:
                welcome = sock.recv(1024).decode()
                print(welcome)
                choice = menu()
                req, ans = convert_to_request(choice)
                sock.sendall(req.encode())  # send to the server the request
                if req != "101#" and req != "108#":
                    sock.sendall(ans.encode())
                    answer = sock.recv(1024).decode()
                    print(answer, "\n")

                elif req == "108#":
                    times = sock.recv(1024).decode()
                    comm = sock.recv(1024).decode()
                    print("from the longest to the shortest albums list - \n"+times, "\nmost 50 common words - \n"+comm)

                else:
                    answer = sock.recv(1024).decode()
                    print(answer, "\n")


def main():
    open_sock()


if __name__ == "__main__":
    main()
