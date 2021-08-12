# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "logged_msg": "LOGGED",
    "question_msg": "GET_QUESTION",
    "answer_msg": "SEND_ANSWER",
    "score_msg": "MY_SCORE",
    "high_score_msg": "HIGHSCORE"

}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "logged_msg": "LOGGED_ANSWER",
    "question_message": "YOUR_QUESTION",
    "correct_answer_msg": "CORRECT_ANSWER",
    "wrong_answer_msg": "WRONG_ANSWER",
    "your_score_msg": "YOUR_SCORE",
    "all_score_msg": "ALL_SCORE",
    "error_msg": "ERROR",
    "no_questions_msg": "NO_QUESTIONS"

}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    # Implement code ...
    legal_cmd = ["LOGIN", "LOGOUT", "LOGGED", "GET_QUESTION", "SEND_ANSWER", "MY_SCORE", "HIGHSCORE", "LOGIN_OK",
                 "LOGGED_ANSWER", "YOUR_QUESTION", "CORRECT_ANSWER", "WRONG_ANSWER", "YOUR_SCORE", "ALL_SCORE", "ERROR",
                 "NO_QUESTIONS"]
    if cmd not in legal_cmd:
        return None
    num_of_space = CMD_FIELD_LENGTH - len(cmd)
    length = str(len(data)).zfill(LENGTH_FIELD_LENGTH)
    full_msg = cmd + (" " * num_of_space) + DELIMITER + length + DELIMITER + data
    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    # Implement code ...
    count = data.count(DELIMITER)
    if count != 2:
        return (None, None)
    lst = data.split(DELIMITER)
    lst[0] = lst[0].rstrip().lstrip()
    lst[1] = lst[1].lstrip().rstrip()
    if not lst[1].isdigit():
        return (None, None)
    if int(lst[1]) != len(lst[2]):
        return (None, None)

    cmd = lst[0]
    msg = lst[2]
    # The function should return 2 values
    return cmd, msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    # Implement code ..
    lst = msg.split(DATA_DELIMITER)
    if len(lst) == expected_fields:
        return lst
    return None


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    # Implement code ...
    lst = DATA_DELIMITER.join(str(field) for field in msg_fields)
    return lst


# c = build_message("0123456789ABCDEFG", "")
# print(c)
# r =  split_data("4122#What is the capital of France?#Lion#Marseille#Paris#Montpellier",6)
# print(r)
# x = join_data(["question" , "ans1" , "ans2" , "ans3" , "ans4" , "correct"])
# print (x)
# c = build_message("LOGIN","sdfsd#dfsfsd")
# print(c)
# p = parse_message("LOGIN_OK        |0010|aaaaaaaaaa")
# print(p)
