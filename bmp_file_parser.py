import os
import shutil
import struct


class ImageParsEditor:
    def __init__(self, image_path):
        self.img_path = image_path
        self.bmp_info = self.read_bmp_header()
        # print(f"{self.bmp_info=}")
        self.pixel_data_offset: int = self.bmp_info["pixel_data_offset"]
        self.bmp_width: int = self.bmp_info["width"]
        self.bmp_height: int = self.bmp_info["height"]
        self.bits_per_pixel: int = self.bmp_info["bits_per_pixel"]
        self.bytes_per_pixel: int = self.bits_per_pixel // 8
        self.is_uncompressed: bool = self.bmp_info["is_uncompressed"]
        self.row_size = (self.bmp_width * self.bytes_per_pixel + 3) & ~3
        # Row size (including padding to the nearest 4 bytes)

        self.edited_bytearray = self.copy_bytes()

    def read_bmp_header(self):
        with open(self.img_path, 'rb') as f:
            # Read the BMP file header (14 bytes)
            bmp_file_header = f.read(14)
            # print(f"{bmp_file_header=}")
            # Unpack the BMP file header
            file_type, file_size, reserved1, reserved2, pixel_data_offset = struct.unpack('<2sI2HI', bmp_file_header)

            if file_type != b'BM':
                raise ValueError("Not a BMP file")

            # Read the DIB header (the first 4 bytes tell us its size)
            dib_header_size = struct.unpack('<I', f.read(4))[0]
            # print(f"{dib_header_size=}")

            # Go back to the beginning of the DIB header
            f.seek(14)

            # Read the entire DIB header based on its size
            dib_header = f.read(dib_header_size)
            # print(f"{dib_header=}")

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

    def get_total_pixel_bytes(self):
        return self.bmp_height * self.bmp_width * self.bytes_per_pixel

    def get_end_index(self):
        end = self.get_total_pixel_bytes() + self.pixel_data_offset - 1
        print(f"End index: {end}")
        return end

    def get_midpoint(self):
        return self.get_total_pixel_bytes() // 2 + self.pixel_data_offset

    def get_row_col(self, index: int):
        row = (index - self.pixel_data_offset) // self.row_size
        col = ((index - self.pixel_data_offset) % self.row_size) // self.bytes_per_pixel
        return row, col

    def read_pixel(self, row: int, col: int) -> bytes:
        # Calculate the position of the pixel in the file
        # BMP files store rows bottom-to-top
        try:
            assert 0 <= row < self.bmp_height
            assert 0 <= col < self.bmp_width
        except AssertionError as e:
            print("Trying to read pixel at invalid coordinates...")
            print(f"{row=} of max {self.bmp_height}")
            print(f"{col=} of max {self.bmp_width}")
            print(e)

        pixel_offset = self.pixel_data_offset + (self.bmp_height - 1 - row) * self.row_size + col * self.bytes_per_pixel
        try:
            with open(self.img_path, 'rb') as f:
                f.seek(pixel_offset)
                pixel_data = f.read(self.bytes_per_pixel)
                return pixel_data
        except (FileExistsError, IndexError) as e:
            print(f"Error reading pixel ({row}, {col}) in {self.img_path}")
            print(e)

    def set_pixel(self, pixel_data: bytes, row: int, col: int):
        # Calculate the position of the pixel in the file
        # BMP files store rows bottom-to-top
        byte_index = self.pixel_data_offset + (self.bmp_height - 1 - row) * self.row_size + col * self.bytes_per_pixel
        assert len(pixel_data) == self.bytes_per_pixel

        # make sure the replacement doesn't exceed the file length
        assert byte_index + len(pixel_data) <= len(self.edited_bytearray)

        # Replace the bytes
        self.edited_bytearray[byte_index:byte_index + len(pixel_data)] = pixel_data

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

    def copy_bytes(self) -> bytearray:
        with open(self.img_path, 'rb') as f:
            return bytearray(f.read())

    def save_edited_image(self, output_path):
        # copy the file to output
        shutil.copy2(self.img_path, output_path)

        with open(output_path, 'rb+') as f:
            # Move to the beginning of the file and write the modified data
            f.seek(0)
            f.write(self.edited_bytearray)
            # f.truncate()  # Adjust the file size if needed

    def read_pixel_at(self, index):
        row, col = self.get_row_col(index)
        return self.read_pixel(row, col)


