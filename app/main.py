# -*- coding: utf-8
import glob
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


def exec_ocr_pallarel(images):
    with ProcessPoolExecutor(max_workers=5) as executor:
        # OCR実行
        results = executor.map(exec_ocr, images)
        print("タスクセット完了")
    return list(results)


def exec_ocr(image):
    tool = get_tool()
    builder = pyocr.builders.TextBuilder()
    txt = tool.image_to_string(image, lang="eng", builder=builder)
    return txt


def main():
    # 画像一覧取得
    file_paths = glob.glob(input_dir + "*.jpg")
    print("ファイル数: " + str(len(file_paths)))
    images = [Image.open(file_path) for file_path in file_paths]

    ocr_results = exec_ocr_pallarel(images)

    for i, result in enumerate(ocr_results):
        print("-----")
        print(str(i + 1) + "個目")
        print("-----")
        print(result)


if __name__ == "__main__":
    print("OCR start")
    main()
    print("OCR end")
