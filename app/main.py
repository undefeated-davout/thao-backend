# -*- coding: utf-8
import glob
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import pyocr
import pyocr.builders
from PIL import Image

input_dir = "./data/"


def get_tool():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("error")
        sys.exit(1)
    tool = tools[0]
    return tool


def exec_ocr(file_path):
    img = Image.open(file_path)
    tool = get_tool()
    builder = pyocr.builders.TextBuilder()
    txt = tool.image_to_string(img, lang="eng", builder=builder)
    return txt


def main():
    file_paths = glob.glob(input_dir + "*.jpg")
    print("ファイル数: " + str(len(file_paths)))

    with ProcessPoolExecutor(max_workers=5) as executor:
        results = executor.map(exec_ocr, file_paths)
        print("タスクセット完了")
    # print(list(results))
    for i, result in enumerate(list(results)):
        print("-----")
        print(str(i + 1) + "個目")
        print("-----")
        print(result)


if __name__ == "__main__":
    print("OCR start")
    main()
    print("OCR end")
