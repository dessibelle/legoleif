#!/bin/bash

convert leif.jpg -resize 32 -remap color_map.gif +dither leif-color-32x32.png
convert leif.jpg -resize 32 +dither -colors 4 leif-32x32.png
