##############################################################################
# server.py
##############################################################################
import random
import socket
import select
import chatlib

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
messages_to_send = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    ## copy from client
    full_msg = chatlib.build_message(code, msg)
    messages_to_send.append((conn, full_msg))

    print("[SERVER] ", full_msg)  # Debug print


def recv_message_and_parse(conn):
    ## copy from client
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    # print(data)
    print("[CLIENT] ", full_msg)  # Debug print
    return cmd, data


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


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
    print("setting up server...")
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
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_score_msg"], str(users[username]["score"]))


# Implement this in later chapters


def handle_highscore_message(conn):
    global users
    sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)
    # print(sorted_users)
    highscore_table = ""
    for element in sorted_users:
        highscore_table += element[0] + ":" + str(element[1]["score"]) + "\n"
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["all_score_msg"], highscore_table)


def handle_logged_message(conn):
    global logged_users
    logged_users_str = ",".join(logged_users.values())
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["logged_msg"], logged_users_str)


def create_random_question():
    global questions
    random_entry = random.choice(list(questions.items()))
    question_id = random_entry[0]
    question = random_entry[1]['question']
    answer1 = random_entry[1]['answers'][0]
    answer2 = random_entry[1]['answers'][1]
    answer3 = random_entry[1]['answers'][2]
    answer4 = random_entry[1]['answers'][3]
    data = [question_id, question, answer1, answer2, answer3, answer4]
    joined_data = chatlib.join_data(data)
    return joined_data


def handle_question_message(conn):
    question = create_random_question()
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["question_message"], question)


def handle_answer_message(conn, username, data):
    global users
    global questions
    parsed_data = chatlib.split_data(data, 2)
    question_id = int(parsed_data[0])
    user_answer = int(parsed_data[1])
    if questions[question_id]["correct"] == user_answer:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_answer_msg"], "")
        users[username]["score"] += 5
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_answer_msg"],
                               str(questions[question_id]["correct"]))


def handle_logout_message(conn):
    """
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
    global logged_users
    address = conn.getpeername()
    del logged_users[address]
    print("closing client socket now...")
    conn.close()


# Implement code ...


def handle_login_message(conn, data):
    """
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later
    parsed_data = chatlib.split_data(data, 2)
    username = parsed_data[0]
    password = parsed_data[1]
    if username in users:
        if password == users[username]["password"]:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
            address = conn.getpeername()
            logged_users[address] = username
        else:
            send_error(conn, "Error! Password does not match!")
    else:
        send_error(conn, "Error! Username does not exist")


# Implement code ...


def handle_client_message(conn, cmd, data):
    """
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
    global logged_users  # To be used later
    address = conn.getpeername()
    if address not in logged_users:
        if cmd != chatlib.PROTOCOL_CLIENT["login_msg"]:
            send_error(conn, "Error! illegal command")

    # Implement code ...
    if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)
    elif cmd == chatlib.PROTOCOL_CLIENT["score_msg"]:
        handle_getscore_message(conn, logged_users[address])
    elif cmd == chatlib.PROTOCOL_CLIENT["high_score_msg"]:
        handle_highscore_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["logged_msg"]:
        handle_logged_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["question_msg"]:
        handle_question_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["answer_msg"]:
        handle_answer_message(conn, logged_users[address], data)
    else:
        send_error(conn, "Error! unknown command")


def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global messages_to_send
    global users
    users = load_user_database()
    global questions
    questions = load_questions()
    client_sockets = []
    server_socket = setup_socket()
    print("Welcome to Trivia Server!")
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("New data from client")
                cmd, data = recv_message_and_parse(current_socket)
                if cmd is None or cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
                    client_sockets.remove(current_socket)
                    print_client_sockets(client_sockets)
                    handle_logout_message(current_socket)
                else:
                    handle_client_message(current_socket, cmd, data)
                    for message in messages_to_send:
                        current_socket, data = message
                        if current_socket in ready_to_write:
                            current_socket.send(data.encode())
                            messages_to_send.remove(message)


# Implement code ...


if __name__ == '__main__':
    main()
