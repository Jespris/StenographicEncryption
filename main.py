import os
import pprint
from bmp_file_parser import ImageParsEditor
from testing import test_suite


def main():
    print("Hello")
    bmp_parser = ImageParsEditor('sample')


if __name__ == "__main__":
    # make sure the program passes all tests, for now
    if test_suite():
        print("="*20 + " MAIN " + "="*20)
        main()
