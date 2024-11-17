from bmp_file_parser import ImageParsEditor


class LCBDecrypter:
    def __init__(self, encrypted_image, key):
        self.encrypted_img_path = encrypted_image
        self.key = key
        self.decrypted_data = ""
        self.img_parser = ImageParsEditor(self.encrypted_img_path)
        self.binary_length, self.key_ints = self.parse_key()
        # print(f"Got key integers: {self.key_ints}")
        # print("Decrypting data...")
        self.decrypt()
        print(f"Decryption complete! Decrypted data: {self.decrypted_data}")

    def decrypt(self):
        binary_data = []
        for i in self.key_ints:
            pixel_bytes = self.img_parser.read_pixel_at(i)
            # print(f"Bytes at {i}: {pixel_bytes}")
            for byte in list(pixel_bytes):
                binary_str = format(byte, '08b')
                # print(f"Binary string of byte: {binary_str}, encoded bit: {binary_str[-1]}")
                binary_data.append(binary_str[-1])
        # join all the data into a very long string in binary
        encrypted_in_binary = ''.join(binary_data)
        encrypted_in_binary = encrypted_in_binary[:self.binary_length]
        # split the binary string into chunks of 8
        binary_in_chunks = [encrypted_in_binary[i:i+8] for i in range(0, len(encrypted_in_binary), 8)]
        # convert the chunks into ASCII characters and join them together
        self.decrypted_data = ''.join([chr(int(binary, 2)) for binary in binary_in_chunks])

    def parse_key(self):
        # Split the key into the binary length and the remaining key
        binary_length, remaining_key = self.key.split("|", 1)
        binary_length = int(binary_length)  # Convert the binary length to an integer
        # print(f"Parsed binary message length: {binary_length}")

        # Split the remaining key into chunks of size 8 and convert to integers
        chunk_size = 8
        decoded_integers = [
            int(remaining_key[i:i + chunk_size])
            for i in range(0, len(remaining_key), chunk_size)
        ]
        # print(f"Decoded key integers: {decoded_integers}")
        return binary_length, decoded_integers

