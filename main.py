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
    encrypting = True if input("Do you want to encrypt? y/n >") == "y" else False
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
        encrypter = Encrypter(image_to_encrypt, data, 1)
        print("Done! Saving encrypted image to output/encrypted_image.bmp")
        encrypter.save_encryption('output/encrypted_image.bmp')
    else:
        # Decrypting
        file_to_decrypt = ""
        for file in os.listdir('output'):  # TODO: fix
            file_to_decrypt = f"output/{file}" if input(f"Do you want to decrypt {file}? y/n >") == "y" else ""
            if file_to_decrypt != "":
                break
        if file_to_decrypt != "":
            decryption_key = input("Please provide the key >")
            decrypter = Decrypter(file_to_decrypt, decryption_key)
        print("DONE! Exiting program!")


if __name__ == "__main__":
    # make sure the program passes all tests, for now
    if test_suite():
        print("="*20 + " MAIN " + "="*20)
        main()
