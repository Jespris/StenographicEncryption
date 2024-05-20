from bmp_file_parser import ImageParsEditor
from decrypter import Decrypter
from encrypter import Encrypter


def test_bmp_images() -> bool:
    test_images = ['blue', 'sample', 'sample2', 'sample3']
    try:
        for test_image in test_images:
            bmp_parser = ImageParsEditor(f"saved_images/{test_image}.bmp")
            assert bmp_parser.is_uncompressed is True
        return True
    except Exception as e:
        print("Sample images failed")
        print(e)
        return False


def test_individual_pixel_editing() -> bool:
    try:
        bmp_parser = ImageParsEditor('saved_images/sample.bmp')
        row = 142
        col = 132
        pixel_data = bmp_parser.read_pixel(row, col)
        rgb = bmp_parser.pixel_as_rgb(pixel_data)
        assert pixel_data == b'\x8cx\xb3'
        assert rgb == (179, 120, 140)

        bmp_parser.set_pixel(b'\x8cx\xb4', row, col)
        bmp_parser.save_edited_image('output/encrypted_sample.bmp')

        new_bmp = ImageParsEditor('output/encrypted_sample.bmp')
        new_pixel_data = new_bmp.read_pixel(row, col)
        new_rgb = new_bmp.pixel_as_rgb(new_pixel_data)
        assert new_pixel_data == b'\x8cx\xb4'
        assert new_rgb == (180, 120, 140)

        return True
    except Exception as e:
        print(e)
        return False


def test_encrypt_decrypt_consistency():
    try:
        test_words = ["test", "Hello", "1234", ",.!#googoogaagaa", "TESTING", "9e"]
        for word in test_words:
            reference_img = 'saved_images/sample.bmp'
            encrypt_path = 'output/encrypted_image.bmp'
            key = 1
            encrypter = Encrypter(reference_img,
                                  word,
                                  key)
            encrypter.save_encryption(encrypt_path)
            decrypter = Decrypter(reference_img,
                                  encrypt_path, key)
            assert decrypter.decrypted_data == word
        return True
    except Exception as e:
        print(e)
        return False


def test_suite() -> bool:
    print("="*20 + " TEST " + "="*20)
    try:
        assert test_bmp_images()
        assert test_individual_pixel_editing()
        # assert test_encrypt_decrypt_consistency()
        print("All tests passed!!!")
        return True
    except Exception as e:
        print(e)
        return False
