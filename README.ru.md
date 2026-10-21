[English](README.md) | [Russian](README.ru.md)

# Difference Expansion (DE) steganography method

Программа для скрытия информации в изображении. Метод использует различия между пикселями для встраивания данных. Эта реализация является пространственной версией (т.е. встраивание происходит в пикселях), поэтому любое искажение (изменение яркости/резкости/контраста и т.д.) почти гарантированно уничтожит встроенную информацию, и, в отличие от метода QIM, этого избежать невозможно (по крайней мере, мне это никогда не удавалось). Особенностью этого метода является возможность восстановления исходного изображения по стеганографическому снимку с использованием карты местоположения.

Карта местоположения отвечает на вопрос типа "было ли сообщение встроено между этими пикселями?".  Если да, то бит извлекается, в противном случае данная пара пикселей пропускается. Если вы потеряете эту карту, вы не сможете прочитать скрытое сообщение, поэтому будьте осторожны с ней. 


## Достойно внимания

Программа автоматически преобразует другие графические форматы в PNG, поскольку это формат без потерь, и закодированная информация не будет уничтожена сразу после завершения работы программы.

Кроме того, не забудьте указать путь к стегоизображению при использовании аргумента reading.

## Установка

Склонируйте репозиторий и скачайте зависимости из requirements.txt

```bash
pip install -r requirements.txt
```
## Использование/Примеры

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
    Decoded message: Decoded message: ('Hello world!', 'image_de_restored.png')

    WITHOUT -r:
    DE_Method.py read -i image_de.png -m image_de_map.txt -l 13   
    Decoded message: Hello world!
```
