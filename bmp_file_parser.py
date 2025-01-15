import shutil
import struct


class ImageParser:
    def __init__(self, image_path):
        self.img_path = image_path
        self.bmp_info = self.read_bmp_header()
        print(f"{self.bmp_info=}")
        self.pixel_data_offset: int = self.bmp_info["pixel_data_offset"] #
        self.bmp_width: int = self.bmp_info["width"]
        self.bmp_height: int = self.bmp_info["height"]
        self.bits_per_pixel: int = self.bmp_info["bits_per_pixel"]
        self.bytes_per_pixel: int = self.bits_per_pixel // 8
        self.is_uncompressed: bool = self.bmp_info["is_uncompressed"]
        self.dib_header_size: int = self.bmp_info["dib_header_size"]
        self.total_bytes: int = self.bmp_info["total_bytes"]

        self.row_size: int = (self.bmp_width * self.bytes_per_pixel + 3) & ~3
        # Row size (including padding to the nearest 4 bytes)

        self.edited_bytearray = self.copy_bytes()

    def read_bmp_header(self):
        with open(self.img_path, 'rb') as f:
            # Read the BMP file header (14 bytes)
            bmp_file_header = f.read(14)
            # print(f"{bmp_file_header=}")
            # Parse the BMP file header
            file_type = bmp_file_header[0:2].decode('ascii')  # First 2 bytes
            file_size = int.from_bytes(bmp_file_header[2:6], byteorder='little')  # Next 4 bytes
            reserved1 = int.from_bytes(bmp_file_header[6:8], byteorder='little')  # Next 2 bytes, not used
            reserved2 = int.from_bytes(bmp_file_header[8:10], byteorder='little')  # Next 2 bytes, not used
            pixel_data_offset = int.from_bytes(bmp_file_header[10:14], byteorder='little')  # Next 4 bytes

            if file_type != 'BM':
                raise ValueError("Not a BMP file")

            # Read the DIB header (the first 4 bytes tell us its size)
            dib_header_size = int.from_bytes(f.read(4), byteorder='little')

            # Go back to the beginning of the DIB header
            f.seek(14)
            dib_header = f.read(dib_header_size)

            # Extract information from the DIB header
            if dib_header_size == 40 or dib_header_size == 124:
                # BITMAPINFOHEADER format
                width = int.from_bytes(dib_header[4:8], byteorder='little')
                height = int.from_bytes(dib_header[8:12], byteorder='little')
                color_planes = int.from_bytes(dib_header[12:14], byteorder='little') # not used
                bits_per_pixel = int.from_bytes(dib_header[14:16], byteorder='little')
                compression_method = int.from_bytes(dib_header[16:20], byteorder='little')

                # Additional fields for BITMAPV5HEADER below, which are not used in this program
                if dib_header_size == 124:

                    red_mask = int.from_bytes(dib_header[40:44], byteorder='little')
                    green_mask = int.from_bytes(dib_header[44:48], byteorder='little')
                    blue_mask = int.from_bytes(dib_header[48:52], byteorder='little')
                    alpha_mask = int.from_bytes(dib_header[52:56], byteorder='little')
                    color_space_type = int.from_bytes(dib_header[56:60], byteorder='little')
            else:
                print(f"{dib_header_size=}")
                raise ValueError("Unsupported DIB header size")

            # Determine if the BMP uses uncompressed data
            is_uncompressed = compression_method == 0

            if not is_uncompressed or bits_per_pixel != 24:
                raise ValueError("Unsupported BMP file, try another sample")

            return {
                "pixel_data_offset": pixel_data_offset,
                "width": width,
                "height": height,
                "bits_per_pixel": bits_per_pixel,
                "is_uncompressed": is_uncompressed,
                "dib_header_size": dib_header_size // 2,  # the header size is in pairs of 4 bits, not bytes
                "total_bytes": file_size
            }

    def get_total_pixel_bytes(self):
        return self.bmp_height * self.bmp_width * self.bytes_per_pixel

    def get_end_index(self):
        end = self.dib_header_size + self.get_total_pixel_bytes() + self.pixel_data_offset - 1
        if end != self.total_bytes - 1:
            print(f"Calculated end index is wrong?!? {end=} != {self.total_bytes=}-1")
        # print(f"End index: {end}")
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
                # Set pointer to pixel
                f.seek(pixel_offset)
                # Read pixel data
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
        # Helper method
        row, col = self.get_row_col(index)
        return self.read_pixel(row, col)

    def is_valid_pixel_index(self, index):
        row, col = self.get_row_col(index)
        if 0 <= row < self.bmp_height and 0 <= col < self.bmp_width:
            return True
        else:
            print(f"Pixel index {index} = ({row}, {col}) is not a pixel in bounds")
            return False


