from bmp_file_parser import ImageParser


class LSBDecrypter:
    def __init__(self, encrypted_image, key):
        self.encrypted_img_path = encrypted_image
        self.key = key
        self.binary_length, self.encrypted_bits, self.key_indexes = self.parse_key()
        self.img_parser = ImageParser(self.encrypted_img_path)
        self.decrypted_data = ""
        self.decrypt()

    def decrypt(self):
        binary_data = []
        for i in self.key_indexes:
            pixel_bytes = self.img_parser.read_pixel_at(i)
            print(f"Bytes at pixel index [{i}]: {pixel_bytes}")
            for byte in list(pixel_bytes):
                binary_str = format(byte, '08b')
                print(f"Binary string of byte: {binary_str}, "
                      f"encoded bit: {binary_str[-self.encrypted_bits:]}")
                binary_data.append(binary_str[-self.encrypted_bits:])
        # join all the data into a very long string in binary
        encrypted_in_binary = ''.join(binary_data)
        # truncate the length to match the expected length
        encrypted_in_binary = encrypted_in_binary[:self.binary_length]
        print(f"Encrypted binary string: {encrypted_in_binary}")
        # split the binary string into chunks of 8 (a byte)
        binary_in_chunks = [
            encrypted_in_binary[i:i+8]
            for i in range(0, len(encrypted_in_binary), 8)
        ]
        # convert the bytes into ASCII characters and join them together
        self.decrypted_data = ''.join([chr(int(byte, 2)) for byte in binary_in_chunks])
        print(f"Decryption complete! Decrypted data: {self.decrypted_data}")

    def parse_key(self):
        # Split the key into the binary length and the remaining index string
        binary_length, encrypted_bits, index_string = self.key.split("|", 2)
        binary_length = int(binary_length)  # Convert the binary length to an integer
        encrypted_bits = int(encrypted_bits)  # also convert this to an integer

        # Split the remaining key into chunks of size 8 (bits) and convert that to integers
        chunk_size = 8
        # using python's in place for loop
        pixel_indexes = [
            int(index_string[i:i + chunk_size])
            for i in range(0, len(index_string), chunk_size)
        ]
        return binary_length, encrypted_bits, pixel_indexes

