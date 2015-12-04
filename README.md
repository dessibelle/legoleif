# Instructions

## Installation

1. `brew install imagemagick`
2. `mkdir venv`
3. `virtualenv --python python3 venv`
4. `source venv/bin/activate`

## Usage

1. Convert large image into small bitmap

    ```
    convert leif.jpg -resize 32 -remap color_map.gif +dither leif-color-32x32.png
    convert leif.jpg -resize 32 +dither -colors 4 leif-32x32.png
    ```

2. Generate build instructions

    ```
    python instructions.py leif-32x32.png
    ```
