import math

from bmp_file_parser import ImageParsEditor
from key_utils import parse_key


class Decrypter:
    def __init__(self, encrypted_image_path, reference_image_path, key):
        self.reference_img_path = reference_image_path
        self.encrypted_img_path = encrypted_image_path
        self.key = key
        self.decrypted_data = ""
        self.encrypted_img_parser = ImageParsEditor(self.encrypted_img_path)
        self.reference_img_parser = ImageParsEditor(self.reference_img_path)
        self.key_info = parse_key(self.key)
        print("Decrypting data...")
        self.decrypt()
        print(f"Decryption complete! Decrypted data: {self.decrypted_data}")

    def decrypt(self):
        list_of_hexes = []
        assert self.identical_headers()
        space = math.floor(
            ((self.key_info['end'] - self.key_info['start']) / self.key_info['msg_length'])
        )
        print(f"Pixel space size (parsed): {space}")
        for i in range(self.key_info['msg_length']):
            current_index = self.key_info['start'] + i * space
            new_bytes = self.encrypted_img_parser.read_pixel_at(current_index)
            reference_bytes = self.reference_img_parser.read_pixel_at(current_index)
            decrypted_hex = self.sub_bytes(new_bytes, reference_bytes)
            list_of_hexes.append(decrypted_hex)
        # print(f"{list_of_hexes=}")
        self.decrypted_data = self.hex_list_to_string(list_of_hexes)

    @staticmethod
    def hex_list_to_string(hex_list):
        print(f"Converting {hex_list} to readable string")
        # Convert each hex value to its UTF-8 equivalent character
        characters = [chr(int(hex_val, 16)) for hex_val in hex_list if hex_val is not None]
        # Join all characters to form the final string
        result_string = ''.join(characters)
        return result_string

    def identical_headers(self):
        for key, value in self.reference_img_parser.bmp_info.items():
            assert value == self.encrypted_img_parser.bmp_info[key]
        return True

    @staticmethod
    def sub_bytes(new_bytes, pixel_bytes):
        # Convert both byte sequences to mutable bytearrays
        new_bytearray = bytearray(new_bytes)
        ref_bytearray = bytearray(pixel_bytes)

        # Subtract the last byte of pixel_bytes from the last byte of new_bytes
        # TODO: check if new bytes is more or less than the reference bytes and subtract or add accordingly
        new_byte = new_bytearray[-1]
        old_byte = ref_bytearray[-1]
        if new_byte > old_byte:
            result = (new_byte - old_byte) % 256
        else:
            result = (new_byte + 256 - old_byte) % 256

        # Convert the resulting byte to a hex string
        hex_string = f"{result:02x}"

        return hex_string
