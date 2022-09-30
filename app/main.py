# -*- coding: utf-8
import sys

import pyocr
import pyocr.builders
from PIL import Image


def main():
    # img = Image.open("./data/full_image.jpg")
    img = Image.open("./data/sample01.jpg")
    # img = Image.open("./data/short.jpg")

    tool = get_tool()
    print("OCR start")
    txt = tool.image_to_string(
        img, lang="eng", builder=pyocr.builders.TextBuilder()
    )
    print(txt)


def get_tool():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("error")
        sys.exit(1)
    tool = tools[0]
    return tool


if __name__ == "__main__":
    main()
