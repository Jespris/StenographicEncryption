import math
import random

from binary_utils import convert_to_binary, binary_to_hex
from bmp_file_parser import ImageParsEditor


class LCBEncrypter:
    def __init__(self, image_path, data):
        self.data_to_encrypt: str = data
        self.image_path = image_path
        self.image_editor = ImageParsEditor(image_path)
        self.data_as_binary = convert_to_binary(self.data_to_encrypt)  # characters in data string are represented as 8 bits
        # print(f"Data as binary: {self.data_as_binary}")
        # print(f"Encrypting data: '{data}' into image")
        self.key = self.obfuscate_data()
        # print("Encryption complete!")
        print("Encryption key:")
        print(self.key)

    def obfuscate_data(self) -> str:
        # returns the encryption key
        # IDEA:
        #   generate random indexes for the key
        #   change the last bit of the pixel bytes to be the encrypted message in binary
        #   convert the key indexes to ASCII, 2 ASCII characters per index
        key_length = math.ceil(len(self.data_as_binary) / 3)
        key_indexes = []
        while len(key_indexes) < key_length:
            key_int = random.randint(self.image_editor.pixel_data_offset, self.image_editor.get_end_index())
            if key_int not in key_indexes:
                key_indexes.append(key_int)

        # print(f"Key indexes: {key_indexes}")

        for i, integer_value in enumerate(key_indexes):
            row, col = self.image_editor.get_row_col(integer_value)
            pixel_bytes = self.image_editor.read_pixel(row, col)
            # print(f"Got bytes {pixel_bytes} at ({row}, {col})")
            if i+3 < len(self.data_as_binary):
                edited_bytes = self.edit_bytes(pixel_bytes, self.data_as_binary[i*3:i*3+3])
            else:
                edited_bytes = self.edit_bytes(pixel_bytes, self.data_as_binary[i:])
            # print(f"Setting bytes {edited_bytes} at ({row}, {col})")
            self.image_editor.set_pixel(edited_bytes, row, col)

        key_as_text = str(len(self.data_as_binary)) + "|" + self.convert_key(key_indexes)
        return key_as_text

    @staticmethod
    def convert_key(integers) -> str:
        # Zero-pad each integer to a length of 8 and concatenate
        encoded_string = "".join(f"{number:08d}" for number in integers)
        return encoded_string

    @staticmethod
    def edit_bytes(pixel_bytes, bits):
        assert len(bits) <= 3
        # print(f"Editing pixel bytes: {pixel_bytes}")
        # print(f"With bits: {bits}")
        binary_strings = []
        for index, byte in enumerate(list(pixel_bytes)):
            # Convert each byte to an 8-bit binary string
            binary_str = format(byte, '08b')
            # print(f"Byte in binary: {binary_str}")
            if index < len(bits):
                # Replace the last bit with the corresponding bit from 'bits'
                binary_str = binary_str[:-1] + bits[index]
            binary_strings.append(binary_str)
            # print(f"The new binary string: {binary_str}")
        # Convert back to bytes
        new_bytes = binary_to_hex(binary_strings)
        # print(f"The new, edited bytes: {new_bytes}")
        # print(f"{new_bytes=}")
        return new_bytes

    def save_encryption(self, output_file_path):
        self.image_editor.save_edited_image(output_file_path)