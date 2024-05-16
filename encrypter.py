import math

from bmp_file_parser import ImageParsEditor


class Encrypter:
    def __init__(self, image_path: str, data: str):
        self.data_to_encrypt: str = data
        self.image_path = image_path
        self.image_editor = ImageParsEditor(image_path)
        self.data_as_chars: [chr] = list(self.data_to_encrypt)
        self.data_as_bytes = self.convert_to_hex(data)
        print(self.data_as_bytes)
        self.obfuscate_data()
        self.image_editor.save_edited_image('output/encrypted_image.bmp')

    @staticmethod
    def convert_to_hex(data):
        # Encode the string to bytes using UTF-8 encoding
        utf8_bytes = data.encode('utf-8')

        # Convert each byte to its hexadecimal representation
        hex_values = [f'{byte:02x}' for byte in utf8_bytes]

        return hex_values

    def obfuscate_data(self):
        # TODO: incorporate a key into calculations somehow
        # IDEA:
        # 1. Space out the bytes evenly throughout the image in order (very simple),
        #   and add the byte to the pixel byte
        #   then replace the bytes with these new edited bytes
        pixels_space_size = math.floor((self.image_editor.bmp_width * self.image_editor.bmp_height) / len(self.data_as_bytes))
        row = 0
        col = 0
        for hex_string in self.data_as_bytes:
            print(f"Byte {hex_string}")
            pixel_bytes = self.image_editor.read_pixel(row, col)
            print(f"Got bytes {pixel_bytes} at ({row}, {col})")
            edited_bytes = self.add_bytes(pixel_bytes, hex_string)
            print(f"Setting bytes {edited_bytes} at ({row}, {col})")
            self.image_editor.set_pixel(edited_bytes, row, col)
            col += pixels_space_size
            while col >= self.image_editor.bmp_width:
                row += 1
                col -= self.image_editor.bmp_width

    @staticmethod
    def add_bytes(pixel_bytes: bytes, hex_string: str) -> bytes:
        # Concatenate the byte_to_add with existing_bytes
        mutable_bytes = bytearray(pixel_bytes)
        bytes_to_add = int(hex_string, 16)
        mutable_bytes[-1] = (mutable_bytes[-1] + bytes_to_add) % 256
        # When doing the reverse for decrypting, check if the value is less or more than the target value
        # Convert back to bytes if needed
        new_bytes = bytes(mutable_bytes)
        # Print the combined bytes
        print(f"{new_bytes=}")
        return new_bytes


