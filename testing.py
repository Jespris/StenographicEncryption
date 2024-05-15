from bmp_file_parser import ImageParsEditor


def test_bmp_images() -> bool:
    return True


def test_individual_pixel_editing() -> bool:
    try:
        bmp_parser = ImageParsEditor('sample')
        row = 142
        col = 132
        pixel_data = bmp_parser.read_pixel(row, col, bmp_parser.img_path)
        rgb = bmp_parser.pixel_as_rgb(pixel_data)
        assert pixel_data == b'\x8cx\xb3'
        assert rgb == (179, 120, 140)

        bmp_parser.set_pixel(b'\x8cx\xb4', row, col)
        bmp_parser.save_edited_image()

        new_pixel_data = bmp_parser.read_pixel(row, col, bmp_parser.img_out_path)
        new_rgb = bmp_parser.pixel_as_rgb(new_pixel_data)
        assert new_pixel_data == b'\x8cx\xb4'
        assert new_rgb == (180, 120, 140)

        return True
    except Exception as e:
        print(e)
        return False


def test_suite() -> bool:
    print("="*20 + " TEST " + "="*20)
    try:
        assert test_bmp_images()
        assert test_individual_pixel_editing()
        print("All tests passed!!!")
        return True
    except Exception as e:
        print(e)
        return False
