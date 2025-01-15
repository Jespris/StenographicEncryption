import math
import random

from binary_utils import convert_to_binary, binary_to_hex
from bmp_file_parser import ImageParser


class LSBEncrypter:
    def __init__(self, image_path, data, encrypt_bits=1):
        self.data_to_encrypt: str = data
        self.image_path = image_path
        self.encrypt_bits: int = encrypt_bits
        self.image_parser = ImageParser(image_path)
        self.data_as_binary = convert_to_binary(self.data_to_encrypt)
        # characters in data string are represented as 8 bits
        print(f"Data as binary: {self.data_as_binary}")
        print(f"Encrypting data: '{data}' into image")
        self.key = ""  # obfuscate_data() method creates the key
        self.obfuscate_data()
        print("Encryption complete!")
        print("Encryption key:")
        print(self.key)

    def obfuscate_data(self):
        # encrypt data as binary in LSB in random pixels, returns the encryption key
        # Step 1.
        #   Figure out how many pixels we need to encrypt,
        #   and get that amount of random pixel indexes
        key_length = math.ceil(len(self.data_as_binary) / (3 * self.encrypt_bits))
        key_indexes = []
        while len(key_indexes) < key_length:
            # Get a random pixel index in bounds
            key_int = random.randint(
                self.image_parser.pixel_data_offset,
                self.image_parser.get_end_index()
            )
            if key_int not in key_indexes and self.image_parser.is_valid_pixel_index(key_int): # Assure in bounds
                # There can't be duplicate indexes
                key_indexes.append(key_int)

        # Step 2.
        #   Go to each pixel index in the key and then
        #   edit the last bits to the corresponding bits in the data we want to hide
        for i, key_index in enumerate(key_indexes):
            row, col = self.image_parser.get_row_col(key_index)
            pixel_bytes = self.image_parser.read_pixel_at(key_index)
            print(f"Got bytes {pixel_bytes} at ({row}, {col})")
            index = i * (3*self.encrypt_bits)
            if i+(3*self.encrypt_bits) < len(self.data_as_binary):
                edited_bytes = self.edit_bytes(
                    pixel_bytes,
                    self.data_as_binary[index:index+3*self.encrypt_bits]
                )
            else: # We have less than 3 bits to encrypt,
                # so only encrypt the bits needed and leave the rest of the pixel bits as is
                edited_bytes = self.edit_bytes(pixel_bytes, self.data_as_binary[index:])

            # Save the edited bytes
            self.image_parser.set_pixel(edited_bytes, row, col)

        # Step 3.
        #   Save the key, it will look something like: 85|1|000013320000131300057136...
        self.key = (str(len(self.data_as_binary)) +
                    "|" + str(self.encrypt_bits) +
                    "|" + self.convert_key(key_indexes))

    @staticmethod
    def convert_key(integers) -> str:
        # Zero-pad each integer to a length of 8 and concatenate
        encoded_string = "".join(f"{number:08d}" for number in integers)
        return encoded_string

    def edit_bytes(self, pixel_bytes, new_bits):
        assert len(new_bits) <= 3 * self.encrypt_bits
        print(f"Editing pixel bytes: {pixel_bytes} with bits: {new_bits}")
        binary_strings = []
        for index, byte in enumerate(list(pixel_bytes)):
            # Convert each byte to an 8-bit binary string
            binary_str = format(byte, '08b')
            print(f"Byte in binary: {binary_str}")
            i = index * self.encrypt_bits
            if (index + 1) * self.encrypt_bits <= len(new_bits):
                # Replace the last bit with the corresponding bit from 'bits'
                binary_str = binary_str[:-self.encrypt_bits] + new_bits[i:i + self.encrypt_bits]
            else:
                # we have run out of bits to encrypt, leave the byte as is
                # or we have less than a full encrypt_bits length worth of bits to encrypt
                print("Encrypting the last remnants of bits into this byte")
                bits_left = len(new_bits) % self.encrypt_bits

                if bits_left > 0:
                    # binary_str = binary_str[:-(bits_left + 1)] + new_bits[i:] + binary_str[-1]
                    binary_str = binary_str[:-self.encrypt_bits] + new_bits[i:] + binary_str[-(self.encrypt_bits-bits_left):]
                else:
                    print("No bits left to encrypt, leaving this byte as is")

            binary_strings.append(binary_str)
            print(f"The new binary string: {binary_str}")
        # Convert back to bytes
        new_bytes = binary_to_hex(binary_strings)
        print(f"The new, edited bytes: {new_bytes}")
        return new_bytes

    def save_encryption(self, output_file_path):
        self.image_parser.save_edited_image(output_file_path)