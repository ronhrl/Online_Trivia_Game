# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message
# LOGIN_MSG = "LOGIN           "
# LOGOUT_MSG = "LOGOUT          "
# LOGGED_MSG = "LOGGED          "
# GET_QUESTION_MSG = "GET_QUESTION    "
# SEND_ANSWER_MSG = "SEND_ANSWER     "
# MY_SCORE_MSG = "MY_SCORE        "
# HIGH_SCORE_MSG = "HIGHSCORE       "

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "logged_msg": "LOGGED",
    "get_question_msg": "GET_QUESTION",
    "send_answer_msg": "SED_ANSWER",
    "my_score_msg": "MY_SCORE",
    "high_score_msg": "HIGHSCORE",
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "logged_answer_msg": "LOGGED_ANSWER",
    "your_question_msg": "YOUR_QUESTION",
    "correct_answer_msg": "CORRECT_ANSWER",
    "wrong_answer_msg": "WRONG_ANSWER",
    "your_score_msg": "YOUR_SCORE",
    "all_score_msg": "ALL_SCORE",
    "no_question_msg": "NO_QUESTION"
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """

    data_len_in = len(data)
    cmd_len = len(cmd)
    data_len_out = ""
    full_msg = ""
    if 10 > data_len_in >= 0:
        data_len_out += "000"
        data_len_out += str(data_len_in)
    elif 100 > data_len_in > 9:
        data_len_out += "00"
        data_len_out += str(data_len_in)
    elif 1000 > data_len_in > 99:
        data_len_out += "0"
        data_len_out += str(data_len_in)
    elif 10000 > data_len_in > 999:
        data_len_out = str(data_len_in)
    else:
        return ERROR_RETURN
    if cmd != "LOGIN" and cmd != "LOGOUT" and cmd != "LOGGED" and cmd != "GET_QUESTION" \
            and cmd != "SEND_ANSWER" and cmd != "MY_SCORE" and cmd != "HIGHSCORE":
        return ERROR_RETURN
    else:
        full_msg += cmd
        for i in range(0, 16 - cmd_len):
            full_msg += " "
        full_msg += DELIMITER
        full_msg += data_len_out
        full_msg += DELIMITER
        full_msg += data
        return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    # Implement code ...
    list_data = data.split("|")
    if len(list_data) < 3:
        cmd = ERROR_RETURN
        msg = ERROR_RETURN
        return cmd, msg
    list_cmd_length = list_data[1].split(" ")
    for word in list_cmd_length:
        if word.lstrip('-').isdigit():
            num = word
    if "LOGIN" not in list_data[0] and "LOGOUT" not in list_data[0] and "LOGGED" not in list_data[0] \
            and "GET_QUESTION" not in list_data[0] and "SEND_ANSWER" not in list_data[0] \
            and "MY_SCORE" not in list_data[0] and "HYSCORE" not in list_data[0]:
        cmd = ERROR_RETURN
        msg = ERROR_RETURN
        return cmd, msg
    elif list_cmd_length[-1].isalpha():
        cmd = ERROR_RETURN
        msg = ERROR_RETURN
        return cmd, msg
    elif int(num) < 0:
        cmd = ERROR_RETURN
        msg = ERROR_RETURN
        return cmd, msg
    else:
        list_cmd = list_data[0].split(" ")
        for word in list_cmd:
            if word != "":
                cmd = word
                break
        msg = list_data[2]
    # The function should return 2 values
    return cmd, msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    # Implement code ...
    list_of_words = msg.split(DATA_DELIMITER)
    error_list = list()
    if len(list_of_words) > expected_fields:
        error_list.append(ERROR_RETURN)
    else:
        return list_of_words


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    # Implement code ...
    join_list = list()
    for i in range(0, len(msg_fields) - 1):
        join_list.append(msg_fields[i])
        join_list.append(DATA_DELIMITER)
    join_list.append(msg_fields[len(msg_fields) - 1])
    return join_list


def check_parse(msg_str, expected_output):
    print("Input: ", msg_str, "\nExpected output: ", expected_output)

    try:
        output = parse_message(msg_str)
    except Exception as e:
        output = "Exception raised: " + str(e)

    if output == expected_output:
        print(".....\t SUCCESS")
    else:
        print(".....\t FAILED, output: ", output)


def main():
    check_parse("LOGIN           |9   |aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    check_parse("LOGIN           |9   | aaa#bbbb", ("LOGIN", " aaa#bbbb"))
    check_parse("LOGIN           |	 -4|data", (None, None))
    # check_parse("", (None, None))
    # check_parse("LOGIN           x	  4|data", (None, None))
    # check_parse("LOGIN           |	  4xdata", (None, None))
    # check_parse("LOGIN           |	 -4|data", (None, None))
    # check_parse("LOGIN           |	  z|data", (None, None))
    # check_parse("LOGIN           |	  5|data", (None, None))


if __name__ == '__main__':
    main()
