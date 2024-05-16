import os
import pprint
from encrypter import Encrypter
from testing import test_suite


def main():
    print("Hello")
    encrypter = Encrypter('saved_images/sample.bmp', "Hello World!")


if __name__ == "__main__":
    # make sure the program passes all tests, for now
    if test_suite():
        print("="*20 + " MAIN " + "="*20)
        main()
