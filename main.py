import os
import pprint
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
    encrypting = True  # TODO: implement decrypt later
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
    # decrypter = Decrypter('saved_images/sample.bmp', 'output/encrypted_image.bmp', 1)


if __name__ == "__main__":
    # make sure the program passes all tests, for now
    if test_suite():
        print("="*20 + " MAIN " + "="*20)
        main()
