import struct


class ImageParser:
    def __init__(self, image_name):
        self.img_path = f'saved_images/{image_name}.bmp'
        self.bmp_info = self.read_bmp_header()
        print(f"{self.bmp_info=}")
        self.pixel_data_offset: int = self.bmp_info["pixel_data_offset"]
        self.bmp_width: int = self.bmp_info["width"]
        self.bmp_height: int = self.bmp_info["height"]
        self.bits_per_pixel: int = self.bmp_info["bits_per_pixel"]
        self.bytes_per_pixel: int = self.bits_per_pixel // 8
        self.is_uncompressed: bool = self.bmp_info["is_uncompressed"]

        pixel_data = self.read_pixel(142, 132)
        rgb = self.pixel_as_rgb(pixel_data)
        print(f"{pixel_data}")
        print(f"{rgb}")

    def read_bmp_header(self):
        with open(self.img_path, 'rb') as f:
            # Read the BMP file header (14 bytes)
            bmp_file_header = f.read(14)
            print(f"{bmp_file_header=}")
            # Unpack the BMP file header
            file_type, file_size, reserved1, reserved2, pixel_data_offset = struct.unpack('<2sI2HI', bmp_file_header)

            if file_type != b'BM':
                raise ValueError("Not a BMP file")

            # Read the DIB header (the first 4 bytes tell us its size)
            dib_header_size = struct.unpack('<I', f.read(4))[0]
            print(f"{dib_header_size=}")

            # Go back to the beginning of the DIB header
            f.seek(14)

            # Read the entire DIB header based on its size
            dib_header = f.read(dib_header_size)
            print(f"{dib_header=}")

            # Extract information from the DIB header
            if dib_header_size == 40:
                # BITMAPINFOHEADER format
                header_info = struct.unpack('<IIIHHIIIIII', dib_header)
                width, height, color_planes, bits_per_pixel, compression_method = header_info[1:6]
            elif dib_header_size == 108:
                # BITMAPV4HEADER format (108 bytes)
                header_info = struct.unpack('<IIIHHIIIIII36xIIIIIIII', dib_header)
                width, height, color_planes, bits_per_pixel, compression_method = header_info[1:6]
            elif dib_header_size == 124:
                # BITMAPV5HEADER format (124 bytes)
                header_info = struct.unpack('<IIIHHIIIIII52xIIIIIIII', dib_header)
                width, height, color_planes, bits_per_pixel, compression_method = header_info[1:6]
            else:
                raise ValueError("Unsupported DIB header size")

            # Determine if the BMP uses uncompressed data
            is_uncompressed = compression_method == 0

            return {
                "pixel_data_offset": pixel_data_offset,
                "width": width,
                "height": height,
                "bits_per_pixel": bits_per_pixel,
                "is_uncompressed": is_uncompressed
            }

    def read_pixel(self, row: int, col: int) -> bytes:
        row_size = (self.bmp_width * self.bytes_per_pixel + 3) & ~3
        # Row size (including padding to the nearest 4 bytes)

        # Calculate the position of the pixel in the file
        # BMP files store rows bottom-to-top
        pixel_offset = self.pixel_data_offset + (self.bmp_height - 1 - row) * row_size + col * self.bytes_per_pixel

        with open(self.img_path, 'rb') as f:
            f.seek(pixel_offset)
            pixel_data = f.read(self.bytes_per_pixel)

        return pixel_data

    def set_pixel(self, pixel_data: bytes, row: int, col: int):
        pass

    def pixel_as_rgb(self, pixel_data):
        if self.bytes_per_pixel == 3:
            # 24-bit BMP: BGR format
            b, g, r = struct.unpack('BBB', pixel_data)
            return (r, g, b)
        elif self.bytes_per_pixel == 4:
            # 32-bit BMP: BGRA format
            b, g, r, a = struct.unpack('BBBB', pixel_data)
            return (r, g, b, a)
        else:
            raise ValueError("Unsupported bits per pixel")
