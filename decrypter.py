from bmp_file_parser import ImageParsEditor


class Decrypter:
    def __init__(self, encrypted_image_path, key):
        # self.reference_img_path = reference_image_path
        self.encrypted_img_path = encrypted_image_path
        self.key = key
        self.decrypted_data = ""
        # self.reference_img_parser = ImageParsEditor(self.reference_img_path)
        self.encrypted_img_parser = ImageParsEditor(self.encrypted_img_path)
        assert self.identical_headers()
        print("Decrypting data...")
        self.decrypt()
        print(f"Decryption complete! Decrypted data: {self.decrypted_data}")

    def decrypt(self):
        list_of_hexes = []
        pixel_data_start = self.encrypted_img_parser.pixel_data_offset
        assert pixel_data_start == self.encrypted_img_parser.pixel_data_offset
        cols = self.encrypted_img_parser.bmp_width
        rows = self.encrypted_img_parser.bmp_height

        datapieces = 0
        for row in range(rows):
            for col in range(cols):
                # TODO: This is a very slow method, optimize using the key
                # reference_data = self.reference_img_parser.read_pixel(row, col)
                encrypted_data = self.encrypted_img_parser.read_pixel(row, col)

        # print(f"{list_of_hexes=}")
        self.decrypted_data = self.hex_list_to_string(list_of_hexes)

    @staticmethod
    def hex_list_to_string(hex_list):
        # Convert each hex value to its UTF-8 equivalent character
        characters = [chr(int(hex_val, 16)) for hex_val in hex_list]
        # Join all characters to form the final string
        result_string = ''.join(characters)
        return result_string

    def identical_headers(self):
        # TODO: make sure the headers of the reference and encrypted images are the same
        return True

    @staticmethod
    def sub_bytes(new_bytes, pixel_bytes):
        # Convert both byte sequences to mutable bytearrays
        mutable_new_bytes = bytearray(new_bytes)
        mutable_pixel_bytes = bytearray(pixel_bytes)

        # Subtract the last byte of pixel_bytes from the last byte of new_bytes
        byte_to_subtract = (mutable_new_bytes[-1] - mutable_pixel_bytes[-1]) % 256

        # Convert the resulting byte to a hex string
        hex_string = f"{byte_to_subtract:02x}"

        return hex_string
