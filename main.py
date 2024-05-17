import os
import pprint
from encrypter import Encrypter
from decrypter import Decrypter
from testing import test_suite


def main():
    print("Hello")
    encrypter = Encrypter('saved_images/sample.bmp', "Hi my name is Jesper Andersson and I'm the author of this code", 1)
    encrypter.save_encryption('output/encrypted_image.bmp')
    decrypter = Decrypter('saved_images/sample.bmp', 'output/encrypted_image.bmp', 1)


if __name__ == "__main__":
    # make sure the program passes all tests, for now
    if test_suite():
        print("="*20 + " MAIN " + "="*20)
        main()
