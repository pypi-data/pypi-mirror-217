# -*- coding: utf-8 -*-
# @Time : 2023/6/28 14:53
# @Author : sunshuanglong
# @File : task_elasticsearch.py
import os
from tqdm import tqdm
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
from collections import OrderedDict


class MngrElasticSearch(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__es = Elasticsearch([{"host": host, "port": port}])

    # 创建索引
    def idx_create(self, index_name):
        return self.__es.indices.create(index_name)

    # 删除索引
    def idx_delete(self, index_name):
        if index_name == "*":
            index_name = list(self.idx_show().keys())
            for _ in index_name:
                self.__es.indices.delete(index_name)
        else:
            self.__es.indices.delete(index_name)

    # 查看所有索引及detail
    def idx_show(self, index_name="*"):
        return self.__es.indices.get(index_name)

    # 查询所有索引数据
    def idx_search_all(self, index_name, size=1000):
        body = {
            "query": {
                "match_all": {}
            }
        }
        return self.__es.search(index=index_name, body=body, size=size)

    # 条件查询
    def idx_search(self, index_name, body, size=1000):
        return self.__es.search(index=index_name, body=body, size=size)

    # 批量读入数据，转换成map写入es
    def from_excel_to_db(self, path, index_name, doc_type="_doc", sheet_name="Sheet1", raise_on_error=True):
        res_list = list()
        df = pd.read_excel(path, sheet_name=sheet_name, index_col=0)
        row_list = df.values.tolist()[1:]
        title_list = df.keys().tolist()
        for row in row_list:
            tmp_dict = dict()
            for idx, elem in enumerate(row):
                # nan特殊处理
                if pd.isna(elem):
                    elem = ""
                tmp_dict[title_list[idx]] = elem
            res_list.append(tmp_dict)
        return helpers.bulk(self.__es, res_list, index=index_name,
                            raise_on_error=raise_on_error)

    # 获取es信息
    def get_info(self):
        return self.__es.info()

    # 获取索引下doc
    def get_doc(self, index_name, id):
        return self.__es.get(index=index_name, id=id)


if __name__ == "__main__":
    es_obj = MngrElasticSearch("192.168.190.80", 9200)
    # print(es_obj.idx_create("guide"))
    # print(es_obj.idx_delete("*"))
    # print(es_obj.idx_show())
    # es_obj.idx_delete("guide")
    print(es_obj.from_excel_to_db(path="origin_text.xlsx", index_name="guide"))
    # rint(es_obj.idx_search("guide", size=1))
    # print(es_obj.get_info())
    # print(es_obj.get_doc("guide", "R2dXBokBrhMr2ml9lczv"))
