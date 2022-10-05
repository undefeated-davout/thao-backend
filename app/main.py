# -*- coding: utf-8
import glob
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import pyocr
import pyocr.builders
import requests
from PIL import Image

INPUT_DIR = "./data/"
MAX_WORKERS = 5


def get_tool():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("error")
        sys.exit(1)
    tool = tools[0]
    return tool


def exec_ocr_pallarel(images):
    builder = pyocr.builders.TextBuilder()
    image_count = len(images)
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # OCR実行
        results = executor.map(exec_ocr, [builder] * image_count, images)
        print("タスクセット完了")
    return list(results)


def exec_ocr(builder, image):
    tool = get_tool()
    txt = tool.image_to_string(image, lang="eng", builder=builder)
    return txt


def call_translate_api(org_texts):
    payload = {
        "auth_key": os.environ["TRANSLATE_API_KEY"],
        "text": org_texts,
        "target_lang": "JA",
    }

    try:
        res = requests.post(os.environ["TRANSLATE_API_URL"], data=payload)
        result = res.json()
        return result
    # エラーハンドリング
    except:
        return "error"


def conv_translate_api_response(translate_api_response):
    texts = [row["text"] for row in translate_api_response["translations"]]
    return texts


def main():
    # 画像一覧取得
    file_paths = glob.glob(INPUT_DIR + "*.jpg")
    print("ファイル数: " + str(len(file_paths)))
    images = [Image.open(file_path) for file_path in file_paths]

    # OCR実行
    ocr_texts = exec_ocr_pallarel(images)

    translate_api_res = call_translate_api(ocr_texts)
    translate_results = conv_translate_api_response(translate_api_res)

    for i, result in enumerate(translate_results):
        print("-----")
        print(str(i + 1) + "個目")
        print("-----")
        print(result)


if __name__ == "__main__":
    print("OCR start")
    main()
    print("OCR end")
