[English](README.en.md) | [Russian](README.ru.md)

# Difference Expansion (DE) steganography method

A program for hiding information in an image. The method uses the differences between pixels to embed the data. This implementation is a spatial version (i.e. embedding takes place in pixels), so any distortion (changing brightness/sharpness/contrast, etc.) is almost guaranteed to destroy the embedded information, and unlike the QIM method, this cannot be avoided (at least, I have never been able to). A feature of this method is the ability to restore the original image from a steganographic image using a location map.

The location map answers a question like "was the message embedded between these pixels?".  If so, the bit is extracted, otherwise the given pair of pixels is skipped. If you lose the location map, you won't be able to read the hidden message, so be careful with it.

## Honorable Mention

The program automatically converts other image formats to PNG because it is not a lossy format, and the encoded information will not be destroyed immediately after the program is terminated.

Also do not forget to put stegoimage path when you use reading argument.
## Installation
Clone the repository and download dependencies from requirements.txt

```bash
pip install -r requirements.txt
```


    
## Usage/Examples

```python
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

    DE_Method.py write -t "Hello world!" -i image.png
    Output path: image_de.png
    Location map saved to: image_de_map.txt
    Message length: 13 bytes

    WITH -r:
    DE_Method.py read -i image_de.png -m image_de_map.txt -r -l 13
    Decoded message: ('Hello world!', 'image_de_restored.png')

    WITHOUT -r:
    DE_Method.py read -i image_de.png -m image_de_map.txt -l 13   
    Decoded message: Hello world!
```
