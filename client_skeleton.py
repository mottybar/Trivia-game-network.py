import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data


def get_score(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["score_msg"], "")
    if msg_code != chatlib.PROTOCOL_SERVER["your_score_msg"]:
        error_and_exit("ERROR")
    print("your score is " + data)


def get_highscore(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["high_score_msg"], "")
    if msg_code != chatlib.PROTOCOL_SERVER["all_score_msg"]:
        error_and_exit("ERROR")
    print("High-Score table:\n" + data)


def play_question(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["question_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["no_questions_msg"] or msg_code != chatlib.PROTOCOL_SERVER["question_message"]:
        # print(data)
        return
    parsed_data = chatlib.split_data(data, 6)
    print("Q: " + parsed_data[1] + ":\n" + "\t1. " + parsed_data[2] + "\n" + "\t2. " + parsed_data[3] + "\n" + "\t3. " +
          parsed_data[4] + "\n" + "\t4. " + parsed_data[5])
    question_id = parsed_data[0]
    answer = input("please choose an answer [1-4]: ")
    question_answer = [question_id, answer]
    joined_data = chatlib.join_data(question_answer)
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["answer_msg"], joined_data)
    if msg_code == chatlib.PROTOCOL_SERVER["correct_answer_msg"]:
        print("YES!!!")
    elif msg_code == chatlib.PROTOCOL_SERVER["wrong_answer_msg"]:
        print("Nope, correct answer is " + chatlib.DATA_DELIMITER + data)
    else:
        error_and_exit("ERROR")


def get_logged_users(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["logged_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["logged_msg"]:
        print(data)
    else:
        error_and_exit("ERROR")


def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    msg = chatlib.build_message(code, data)
    # print(msg)
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
    # print(data)
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
    # Implement code
    cmd = ""
    while cmd != chatlib.PROTOCOL_SERVER["login_ok_msg"]:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        msg_data = chatlib.join_data([username, password])
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], msg_data)
        cmd, data = recv_message_and_parse(conn)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Logged in!")
            return
        else:
            print(data)

    # Implement code


def logout(conn):
    # Implement code
    print("Goodbye!")
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    conn.close()


def main():
    # Implement code
    conn = connect()
    login(conn)
    while True:
        print("p   Play a trivia question\ns   Get my score\nh   Get high score\nl   Get logged users\nq   Quit")
        choice = input("Please enter your choice: ")
        if choice == "p":
            play_question(conn)
        elif choice == "s":
            get_score(conn)
        elif choice == "h":
            get_highscore(conn)
        elif choice == "l":
            get_logged_users(conn)
        elif choice == "q":
            break
        else:
            print("wrong choice")
    logout(conn)


if __name__ == '__main__':
    main()
