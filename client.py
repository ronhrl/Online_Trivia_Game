import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    msg = chatlib.build_message(code, data)
    print("The message is: " + msg)
    print(conn)
    conn.send(msg.encode())


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # Implement Code
    # ..
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(error_msg):
    # Implement code
    print(error_msg)
    exit()


def login(conn):
    username = input("Please enter username: \n")
    password = input("Please enter password: \n")
    user_pass = username + "#" + password
    # Implement code
    while True:
        print(57)
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], user_pass)
        cmd, data = recv_message_and_parse(conn)
        print(cmd, data)
        if cmd is not None and data is not None:
            print("Logged in")
            return
        else:
            print("Login failed. Please try again")
            username = input("Please enter username: \n")
            password = input("Please enter password: \n")
            user_pass = username + "#" + password

    # Implement code


def logout(conn):
    # Implement code
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    pass


def build_send_recv_parse(conn, cmd, data):
    build_and_send_message(conn, cmd, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data


def get_score(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["my_score_msg"], "")
    if "YOUR SCORE" not in msg_code:
        print("Error")
    else:
        print(data)


def get_highscore(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["high_score_msg"], "")
    if "HIGHSCORE" not in msg_code:
        print("Error")
    else:
        print(data)


def play_question(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question_msg"], "")
    if "NO_QUESTION" in msg_code:
        print("There is no more questions. the game is over")
    else:
        print(data)
        answer = input("Please enter your answer:\n")
        msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer_msg"], answer)
        if "CORRECT_ANSWER" in msg_code:
            print("Your are right\n the answer is: " + answer)
            return
        elif "WRONG_ANSWER" in msg_code:
            print("Nope, correct answer is: " + data)
            return
        else:
            print("Error")
            return


def get_logged_users(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["logged_msg"], "")
    if "LOGGED_ANSWER" not in msg_code:
        print("Error")
    else:
        print(data)


def main():
    # Implement code
    client_socket = connect()
    login(client_socket)
    while True:
        user_choose = input("p \t\tPlay a trivia question\n s \t\tget your score\n h \t\tget high scores\n "
                            "l \t\tGet logged users\n q \t\tQuit")
        if user_choose == 'p':
            play_question(client_socket)
        elif user_choose == 's':
            get_score(client_socket)
        elif user_choose == 'h':
            get_highscore(client_socket)
        elif user_choose == 'l':
            get_logged_users(client_socket)
        elif user_choose == 'q':
            break
    logout(client_socket)
    pass


if __name__ == '__main__':
    main()
