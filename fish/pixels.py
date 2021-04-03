#!/usr/bin/python3

from PIL import Image

org = Image.open("fish.png")
new = Image.new("RGBA", org.size, 0xFFFFFF)

width, height = org.size
for y in range(height):
    for x in range(width):
        r,g,b,a = org.getpixel((x, y))
        new.putpixel((x, y), (r, g, b, 255))

new.save("living-fish.png")
