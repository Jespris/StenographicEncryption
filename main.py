import os
from encrypter import Encrypter
from decrypter import Decrypter
from testing import test_suite

# Globals
SAMPLE_IMAGES = ['saved_images/blue.bmp',
                 'saved_images/sample.bmp',
                 'saved_images/sample2.bmp',
                 'saved_images/sample3.bmp']


def main():
    print("Hello")
    while True:
        encrypting = True if input("Do you want to encrypt? y/n > ") == "y" else False
        if encrypting:
            valid_path = False
            image_to_encrypt = ""
            while not valid_path:
                print(f"Please provide a valid path to the image you want to encrypt, "
                      f"or you can choose from this list of sample images: {SAMPLE_IMAGES}")
                image_to_encrypt = input("Path: ")
                if image_to_encrypt in SAMPLE_IMAGES:  # TODO: or using os check if file exists and is bmp
                    valid_path = True

            data = input("Provide the message you want to encrypt: ")
            print("Encrypting data...")
            encrypter = Encrypter(image_to_encrypt, data)
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
            reference_file = None
            print(f"{os.listdir('saved_images')=}")
            while reference_file is None:
                for file in os.listdir('saved_images'):
                    reference_file = f"saved_images/{file}" if input(f"Is this the reference file: {file}? y/n > ") == "y" else None
                    if reference_file is not None:
                        break
                # TODO: add alternative to give absolute path to a bmp image
            if file_to_decrypt is not None and reference_file is not None:
                decryption_key = input("Please provide the key > ")
                decrypter = Decrypter(file_to_decrypt, reference_file, decryption_key)
            print("DONE! Exiting program!")


if __name__ == "__main__":
    # make sure the program passes all tests, for now
    if test_suite():
        print("="*20 + " MAIN " + "="*20)
        main()
