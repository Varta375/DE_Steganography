"""
DE_Method.py

Usage:
    DE_Method.py [-h] write -t <text_input> -i <image_input>
    DE_Method.py [-h] read -i <stegoimage_input> -m <location_map> [-r <restore>] -l <message_length>

Options:
    -h, --help                      Show options
    -t, --text=<text_input>         Text input
    -i, --in=<image_input>          Image path of steganography container
    -m, --map=<location_map>        Location map (txt-file)
    -r, --restore                   Restore the original image
    -l, --length=<message_length>   Message length
    -v, --version                   Show the version
"""

from PIL import Image
import numpy as np
import math
from docopt import docopt

class DE_Exception(Exception):
    pass

class DE:
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("RGB")
        image_array = np.array(self.image)
        self.height, self.width, self.channels = image_array.shape

    @staticmethod
    def message_to_bits(message: str) -> list[int]:
        data = message.encode("utf-8")
        bits = []
        for byte in data:
            for shift in range(7, -1, -1):
                bits.append((byte >> shift) & 1)
        return bits

    @staticmethod
    def bits_to_message(bits) -> str:
        if len(bits) % 8 != 0:
            raise ValueError("The number of bits must be a multiple of 8")
        data = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for bit in bits[i:i + 8]:
                bit = int(bit)
                if bit not in (0, 1):
                    raise ValueError(f"Invalid bit value: {bit}")
                byte = (byte << 1) | bit
            data.append(byte)
        return data.decode("utf-8")

    def write(self, image_path, message):
        location_map = ""
        img = Image.open(image_path).convert("RGB")
        pixel_array = np.array(img)
        image_shape = pixel_array.shape
        pixel_list = pixel_array.flatten().astype(float)
        bits = self.message_to_bits(message)
        bits_index = 0

        for i in range(0, len(pixel_list) - 1, 2):
            if bits_index >= len(bits):
                break

            L = math.floor((pixel_list[i] + pixel_list[i + 1]) / 2)
            difference = pixel_list[i] - pixel_list[i + 1]

            if abs(2 * difference + bits[bits_index]) <= 2 * min(L, 255 - L):
                location_map += "1"
                difference_update = 2 * difference + bits[bits_index]
                pixel_list[i] = L + math.floor((difference_update + 1) / 2)
                pixel_list[i + 1] = L - math.floor(difference_update / 2)
                bits_index += 1
            else:
                location_map += "0"

        edited_array = pixel_list.reshape(image_shape).clip(0, 255).astype(np.uint8)
        edited_image = Image.fromarray(edited_array)
        output_path = image_path.rsplit(".", 1)[0] + "_de.png"
        edited_image.save(output_path, format="PNG")
        return location_map, bits, output_path

    def read(self, stegoimage_path, message_length, location_map, restore=False):
        img = Image.open(stegoimage_path).convert("RGB")
        pixel_array = np.array(img)
        image_shape = pixel_array.shape
        pixel_list = pixel_array.flatten().astype(int)
        bits_str = ""
        total_bits = message_length * 8
        pixel_index = 0

        for m_bit in location_map:
            if (pixel_index + 1) >= len(pixel_list):
                break

            p_i = pixel_list[pixel_index]
            p_i_1 = pixel_list[pixel_index + 1]

            L = math.floor((p_i + p_i_1) / 2)

            if m_bit == "1":
                d_sh = p_i - p_i_1

                if len(bits_str) < total_bits:
                    bit = abs(d_sh) % 2
                    bits_str += str(bit)

                if restore:
                    d_original = d_sh // 2
                    pixel_list[pixel_index] = L + math.floor((d_original + 1) / 2)
                    pixel_list[pixel_index + 1] = L - math.floor(d_original / 2)
            pixel_index += 2

        decoded_message = self.bits_to_message(bits_str)

        if restore:
            edited_array = pixel_list.reshape(image_shape).clip(0, 255).astype(np.uint8)
            edited_image = Image.fromarray(edited_array)
            output_path = stegoimage_path.rsplit(".", 1)[0] + "_restored.png"
            edited_image.save(output_path, format="PNG")
            return decoded_message, output_path

        return decoded_message


def main():
    args = docopt(__doc__ or "", version="de 1.0")
    try:
        image_path = args["--in"]
        steg = DE(image_path)

        if args["write"]:
            text = args["--text"]
            location_map, bits, output_path = steg.write(image_path, text)
            map_path = output_path.rsplit(".", 1)[0] + "_map.txt"
            with open(map_path, "w") as f:
                f.write(location_map)
            print(f"Output path: {output_path}")
            print(f"Location map saved to: {map_path}")
            print(f"Message length: {len(text.encode('utf-8'))} bytes")


        elif args["read"]:
            map_path = args["--map"]

            with open(map_path, "r") as f:
                location_map = f.read().strip()

            message_length = int(args["--length"])
            restore = args["--restore"]
            result = steg.read(image_path, message_length, location_map, restore)
            print(f"Decoded message: {result}")

    except:
        raise DE_Exception("Use --help to see usage and options")

if __name__ == "__main__":
    main()