# -*- coding: utf-8 -*-
# @Time : 2023/6/26 11:21
# @Author : sunshuanglong
# @File : sun_idea_utils.py
import tqdm
import json
from torchkeras.data import download_baidu_pictures


def parse_jsonls_to_map_list(data_list):
    res_list = list()
    for item in tqdm(data_list, desc="to_json..."):
        res_list.append(json.loads(item))
    return res_list


def parse_jsonls_to_map_list_from_file(file_path):
    res_list = list()
    data_list = open(file_path, "r", encoding="utf-8").read().strip().split("\n")
    for item in data_list:
        res_list.append(json.loads(item))
    return res_list


# 一行代码根据关键词抓取百度图片
def get_picture_from_baidu(keyword="夏目友人帐表情包", needed_pics_num=10, save_dir="cats_xiamu"):
    download_baidu_pictures(keyword=keyword, needed_pics_num=needed_pics_num, save_dir=save_dir)


if __name__ == "__main__":
    print(get_picture_from_baidu())
