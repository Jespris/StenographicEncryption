

def generate_unique_key(pixels_start: int, pixels_end: int, msg_length: int):
    # 8 Digits representing Start index
    start_index_str = f"{hex(pixels_start)[2:].zfill(8)}"

    # 4 Digits representing msg length
    msg_length_str = f"{hex(msg_length)[2:].zfill(4)}"

    # 8 Digits representing End index
    end_index_str = f"{hex(pixels_end)[2:].zfill(8)}"

    # Combine all parts into a 20-digit number
    key_str = f"{start_index_str}{msg_length_str}{end_index_str}"

    print(f"Generated key: {key_str}")
    return key_str


def generate_binary_key(pixels_start: int, pixels_end: int):
    # 8 Digits representing Start index
    start_index_str = f"{hex(pixels_start)[2:].zfill(8)}"
    # 8 Digits representing End index
    end_index_str = f"{hex(pixels_end)[2:].zfill(8)}"
    # Combine all parts into a 20-digit number
    key_str = f"{start_index_str}{end_index_str}"

    print(f"Generated key: {key_str}")
    return key_str


def parse_key(key_hex):
    # Extract each part of the key
    start_index_str = key_hex[:8]
    # print(f"{start_index_str}")
    msg_length = key_hex[8:12]
    # print(f"{msg_length}")
    end_index_str = key_hex[12:]
    # print(f"{end_index_str}")

    # Convert each part back to its original form
    start_index = int(start_index_str, 16)
    msg_length = int(msg_length, 16)
    end_index = int(end_index_str, 16)

    # Return the parsed information as a dictionary
    parsed_info = {
        "start": start_index,
        "end": end_index,
        "msg_length": msg_length
    }

    return parsed_info


def parse_binary_key(key_hex):
    # Extract each part of the key
    start_index_str = key_hex[:8]
    # print(f"{start_index_str}")
    end_index_str = key_hex[8:]
    # print(f"{end_index_str}")

    # Convert each part back to its original form
    start_index = int(start_index_str, 16)
    end_index = int(end_index_str, 16)

    # Return the parsed information as a dictionary
    parsed_info = {
        "start": start_index,
        "end": end_index
    }

    return parsed_info

