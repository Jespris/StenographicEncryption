import random

from binary_utils import binary_to_hex, convert_to_binary
from bmp_file_parser import ImageParser
from key_utils import generate_binary_key


class BinaryEncrypter:
    def __init__(self, image_path, data):
        self.data_to_encrypt: str = data
        self.image_path = image_path
        self.image_editor = ImageParser(image_path)
        self.data_as_binary = convert_to_binary(self.data_to_encrypt)  # characters in data string are represented as 8 bits
        # print(self.data_as_bytes)
        print(f"Encrypting data: '{data}' into image")
        self.data_start = self.set_data_start()
        self.data_end = self.obfuscate_data()
        # data start and end is set in obfuscate data function
        self.key = generate_binary_key(self.data_start, self.data_end)
        print("Encryption complete!")

    def save_encryption(self, output_file_path):
        self.image_editor.save_edited_image(output_file_path)

    def set_data_start(self):
        # set a random startpoint where the encryption still fits
        allow_length = len(self.data_as_binary) + len(self.data_as_binary) % self.image_editor.bytes_per_pixel
        max_end = self.image_editor.get_end_index() - allow_length
        start = random.randint(
            self.image_editor.pixel_data_offset,
            max_end
        )
        return start

    def obfuscate_data(self) -> int:
        # returns the ending index
        # IDEA:
        #   pick a random startpoint,
        #   then look at each pixels rgb values as binary
        #   and change the last bit according to our data string in binary
        current_index = self.data_start
        i = 0
        while i < len(self.data_as_binary):
            # print(f"Byte {hex_string}")
            row, col = self.image_editor.get_row_col(current_index)
            pixel_bytes = self.image_editor.read_pixel(row, col)
            # print(f"Got bytes {pixel_bytes} at ({row}, {col})")
            edited_bytes = self.edit_bytes(pixel_bytes, i)
            # print(f"Setting bytes {edited_bytes} at ({row}, {col})")
            self.image_editor.set_pixel(edited_bytes, row, col)
            current_index += self.image_editor.bytes_per_pixel
            i += self.image_editor.bytes_per_pixel
        return current_index

    def edit_bytes(self, pixel_bytes, i: int):
        # print(f"Got pixel bytes: {pixel_bytes}")
        binary_strings = []
        for index, byte in enumerate(list(pixel_bytes)):
            # Convert each byte to an 8-bit binary string
            binary_str = format(byte, '08b')
            # Set the last bit to 0
            if i + index < len(self.data_as_binary):
                binary_str = binary_str[:-1] + self.data_as_binary[i + index]
            binary_strings.append(binary_str)
        # print(f"This is {binary_strings} in binary")
        # Convert back to bytes
        new_bytes = binary_to_hex(binary_strings)
        # print(f"The new, edited bytes: {new_bytes}")
        # print(f"{new_bytes=}")
        return new_bytes



