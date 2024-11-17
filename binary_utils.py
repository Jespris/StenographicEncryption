
def binary_to_hex(binary_strings):
    new_bytes = bytearray()
    for binary_str in binary_strings:
        # Convert the binary string back to a byte
        new_byte = int(binary_str, 2)
        new_bytes.append(new_byte)

    return bytes(new_bytes)


def convert_to_binary(data: str) -> str:
    return ''.join(format(ord(char), '08b') for char in data)
