##############################################################################
# server.py
##############################################################################

import socket
import chatlib

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    # copy from client
    full_msg = chatlib.build_message(code, msg)
    print("[SERVER] ", full_msg)  # Debug print
    conn.send(msg.encode())


def recv_message_and_parse(conn):
    # copy from client
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    print("[CLIENT] ", full_msg)  # Debug print
    return cmd, data


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
               "correct": 3}
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
        "test": {"password": "test", "score": 0, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []}
    }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    # Implement code ...
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()
    return sock


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    # Implement code ...
    msg = ERROR_MSG + error_msg
    conn.send(msg.encode())


##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    # Implement this in later chapters


def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users

    # Implement code ...
    conn.close()


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later

    # Implement code ...
    # To check later
    list_of_words = chatlib.split_data(data, 2)
    user_name = list_of_words[0]
    user_password = list_of_words[1]
    if user_name not in users:
        build_and_send_message(conn, ERROR_MSG, "The username doesn't exist. Try another username")
    else:
        dict_password = users.get(user_name).split(",")[0].split(" ")[0]
        if user_password != dict_password:
            build_and_send_message(conn, ERROR_MSG, "The password is wrong. Try another password")
        else:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users  # To be used later

    # Implement code ...
    if cmd == "LOGIN":
        handle_login_message(conn, data)
    elif cmd == "LOGOUT":
        handle_logout_message(conn)
    elif cmd == "GET_SCORE":
        handle_getscore_message(conn, data)
    else:
        build_and_send_message(conn, ERROR_MSG, "The command didn't found. Please choose another command.")


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")

    # Implement code ...


if __name__ == '__main__':
    main()