import math
import random

from bmp_file_parser import ImageParser
from key_utils import generate_unique_key


class Encrypter:
    def __init__(self, image_path: str, data: str):
        self.data_to_encrypt: str = data
        self.image_path = image_path
        self.image_editor = ImageParser(image_path)
        self.data_as_chars: [chr] = list(self.data_to_encrypt)
        self.data_as_bytes = self.convert_to_hex(data)
        # print(self.data_as_bytes)
        print(f"Encrypting data: '{data}' into image")
        self.data_start = None
        self.data_end = None
        self.key = self.generate_key()
        print(f"Your encryption key: {self.key}")
        self.obfuscate_data()
        print("Encryption complete!")
        # self.image_editor.save_edited_image('output/encrypted_image.bmp')

    def save_encryption(self, output_file_path):
        self.image_editor.save_edited_image(output_file_path)

    @staticmethod
    def convert_to_hex(data):
        # Encode the string to bytes using UTF-8 encoding
        utf8_bytes = data.encode('utf-8')

        # Convert each byte to its hexadecimal representation
        hex_values = [f'{byte:02x}' for byte in utf8_bytes]

        return hex_values

    def get_data_start(self):
        if self.data_start is None:
            print("Data start not defined")
            return None
        return self.data_start

    def get_data_end(self):
        if self.data_end is None:
            print("Data end not defined")
            return None
        return self.data_end

    def get_data_length(self) -> int:
        return len(self.data_to_encrypt)

    def obfuscate_data(self):
        # Space out the bytes evenly throughout the image in order (very simple),
        #       and add the byte to the pixel byte
        #       then replace the bytes with these new edited bytes
        # New idea: Use the generated key to evenly space out the bytes in the image
        #       and add the byte to the pixel byte
        #       then replace the bytes with these new edited bytes
        print(f"{self.data_as_bytes=}")
        pixels_space_size = math.floor(
            ((self.get_data_end() - self.get_data_start()) / self.get_data_length())
        )
        print(f"{pixels_space_size=}")
        current_index = self.get_data_start()
        for hex_string in self.data_as_bytes:
            # print(f"Byte {hex_string}")
            row, col = self.image_editor.get_row_col(current_index)
            pixel_bytes = self.image_editor.read_pixel(row, col)
            # print(f"Got bytes {pixel_bytes} at ({row}, {col})")
            edited_bytes = self.add_bytes(pixel_bytes, hex_string)
            # print(f"Setting bytes {edited_bytes} at ({row}, {col})")
            self.image_editor.set_pixel(edited_bytes, row, col)
            current_index += pixels_space_size


    @staticmethod
    def add_bytes(pixel_bytes: bytes, hex_string: str) -> bytes:
        # Concatenate the byte_to_add with existing_bytes
        mutable_bytes = bytearray(pixel_bytes)
        bytes_to_add = int(hex_string, 16)
        mutable_bytes[-1] = (mutable_bytes[-1] + bytes_to_add) % 256
        # When doing the reverse for decrypting, check if the value is less or more than the target value
        # Convert back to bytes
        new_bytes = bytes(mutable_bytes)
        # print(f"{new_bytes=}")
        return new_bytes

    def generate_key(self):
        pixel_offset = self.image_editor.pixel_data_offset
        print(f"Pixel indexes start at {pixel_offset=}")
        image_end = self.image_editor.get_end_index()
        midpoint = self.image_editor.get_midpoint()
        # choose a random start index between offset and midpoint
        start = random.randint(pixel_offset, midpoint - 1)
        print(f"{start=}")
        # choose a random end index between (start + length) and endpoint
        data_length = len(self.data_to_encrypt)
        end = random.randint(start + data_length, image_end - 1)
        print(f"{end=}")
        self.data_start = start
        self.data_end = end

        return generate_unique_key(start, end, data_length)


