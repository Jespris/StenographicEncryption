import os
from lsb_decrypter import LSBDecrypter
from lsb_encrypter import LSBEncrypter


# Globals
SAMPLE_IMAGES = ['saved_images/blue.bmp',
                 'saved_images/sample.bmp',
                 'saved_images/sample2.bmp',
                 'saved_images/sample3.bmp',
                 'saved_images/10x10.bmp',
                 'saved_images/10x10corner.bmp',]


def main():
    test_bmp = 'saved_images/10x10.bmp'
    test_message = 'Hello, world!'
    print("Hello")
    while True:
        encrypting = True if input("Do you want to LSB encrypt? y/n > ") == "y" else False
        if encrypting:
            if test_bmp and test_message:
                print("Encrypting with test parameters...")
            valid_path = False
            image_to_encrypt = test_bmp
            while not valid_path:
                if image_to_encrypt in SAMPLE_IMAGES:  # TODO: or using os check if file exists and is bmp
                    valid_path = True
                else:
                    print(f"Please provide a valid path to the image you want to encrypt, "
                          f"or you can choose from this list of sample images: {SAMPLE_IMAGES}")
                    image_to_encrypt = input("Path: ")

            if not test_message:
                data = input("Provide the message you want to encrypt: ")
            else:
                data = test_message
            # print("Encrypting data...")
            encrypt_bits = 1
            try:
                encrypt_bits = int(input("How many bits per byte do you want to encrypt? (Suggested amount: 1 or 2. Max Amount = 8) \n> "))
                if encrypt_bits > 8:
                    print("Invalid input. Setting encryption bits per byte to 1")
            except Exception as e:
                print("Invalid input. Setting encryption bits per byte to 1")
                encrypt_bits = 1
            encrypter = LSBEncrypter(image_to_encrypt, data, encrypt_bits)
            output_path = f"output/{input('Please provide a name for the encrypted file > ')}"
            print(f"Done! Saved encrypted image to {output_path}")
            encrypter.save_encryption(output_path)
        else:
            # Decrypting
            file_to_decrypt = None
            while file_to_decrypt is None:
                for file in os.listdir('output'):
                    file_to_decrypt = f"output/{file}" if input(f"Do you want to decrypt {file}? y/n > ") == "y" else None
                    if file_to_decrypt is not None:
                        break
                # TODO: add alternative to give absolute path to a bmp image
            if file_to_decrypt is not None:
                decryption_key = input("Please provide the key > ")
                decrypter = LSBDecrypter(file_to_decrypt, decryption_key)
            print("DONE! Exiting program!")
            break


if __name__ == "__main__":
    # make sure the program passes all tests, for now
    # if test_suite():
    print("="*20 + " MAIN " + "="*20)
    main()
