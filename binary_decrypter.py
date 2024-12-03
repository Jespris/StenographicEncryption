from bmp_file_parser import ImageParser
from key_utils import parse_binary_key


class BinaryDecrypter:
    def __init__(self, encrypted_image, key):
        self.encrypted_img_path = encrypted_image
        self.key = key
        self.decrypted_data = ""
        self.img_parser = ImageParser(self.encrypted_img_path)
        self.key_info = parse_binary_key(self.key)
        print("Decrypting data...")
        self.decrypt()
        print(f"Decryption complete! Decrypted data: {self.decrypted_data}")

    def decrypt(self):
        start = self.key_info['start']
        end = self.key_info['end']
        pixel_size = self.img_parser.bytes_per_pixel
        binary_data = []
        for i in range(start, end, pixel_size):
            pixel_bytes = self.img_parser.read_pixel_at(i)
            for byte in list(pixel_bytes):
                binary_str = format(byte, '08b')
                binary_data.append(binary_str[-1])
        # join all the data into a very long string in binary
        encrypted_in_binary = ''.join(binary_data)
        # split the binary string into chunks of 8
        binary_in_chunks = [encrypted_in_binary[i:i+8] for i in range(0, len(encrypted_in_binary), 8)]
        # convert the chunks into ASCII characters and join them together
        self.decrypted_data = ''.join([chr(int(binary, 2)) for binary in binary_in_chunks])

