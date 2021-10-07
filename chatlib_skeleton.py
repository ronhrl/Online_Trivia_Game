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
    "logout_msg": "LOGOUT"
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR"
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error

    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
def build_message(cmd, data):
    data_len_in = len(data)
    cmd_len = len(cmd)
    data_len_out = ""
    full_msg = ""
    if 10 > data_len_in >= 0:
        data_len_out += "000"
        data_len_out += data_len_in
    elif 100 > data_len_in > 9:
        data_len_out += "00"
        data_len_out += data_len_in
    elif 1000 > data_len_in > 99:
        data_len_out += "0"
        data_len_out += data_len_in
    elif 10000 > data_len_in > 999:
        data_len_out = data_len_in
    else:
       return ERROR_RETURN
    if cmd != "LOGIN" or cmd != "LOGOUT" or cmd != "LOGGED" or cmd != "GET_QUESTION" \
            or cmd != "SEND_ANSWER" or cmd != "MY_SCORE" or cmd != "HIGHSCORE":
        return ERROR_RETURN
    else:
        full_msg += cmd
        for i in range(0, 17 - cmd_len):
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
    list_to_return = list()
    if list_data[0] != "LOGIN" or list_data[0] != "LOGOUT" or list_data[0] != "LOGGED" or list_data[0] != "GET_QUESTION" \
            or list_data[0] != "SEND_ANSWER" or list_data[0] != "MY_SCORE" or list_data[0] != "HIGHSCORE":
        cmd = ERROR_RETURN
        msg = ERROR_RETURN
    else:
        
    # The function should return 2 values
    return cmd, msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    # Implement code ...
    list_of_words = list()
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
