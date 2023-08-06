# -*- coding: utf-8 -*-
# @Time : 2023/6/14 14:37
# @Author : sunshuanglong
# @File : multi_task.py
from concurrent.futures import ProcessPoolExecutor, wait
from ..sun_config import sun_idea_config
from tqdm import tqdm
import json


class MultiTask(object):
    def __init__(self, process_num=None):
        self.config = sun_idea_config.config_all["multi_task"]
        if process_num is None:
            self.process_num = self.config["process_num"]
        else:
            self.process_num = process_num
        self.__executor = ProcessPoolExecutor(max_workers=self.process_num)

    def multi_task_processing(self, data_list, fun_job, **kwargs):
        process_list = list()
        res_list = list()
        data_sub_sum = len(data_list) // self.process_num
        for idx in range(0, len(data_list), data_sub_sum):
            item = data_list[idx: idx + data_sub_sum]
            process_list.append(self.__executor.submit(fun_job, item, **kwargs))
        wait(process_list)
        for _ in process_list:
            res_list.extend(_.result())
        return res_list

    def load_jsonl(self, file_path):
        data_list = open(file_path, "r", encoding="utf-8").read().strip().split("\n")
        data_args = dict()
        return self.multi_task_processing(data_list, self.parse_jsonls_to_str_list, **data_args)

    @staticmethod
    def parse_jsonls_to_str_list(data_list, **kwargs):
        res_list = list()
        for item in tqdm(data_list, desc="to_json..."):
            res_list.append(json.loads(item))
        return res_list

    def close(self):
        self.__executor.shutdown()


def fun_job(data_list, **kwargs):
    a = kwargs
    for item in tqdm(data_list, desc="processing..."):
        for i in range(1000):
            item[f"add_{i}"] = "made by sunxiaowu"

    return data_list


if __name__ == "__main__":
    task_obj = MultiTask(process_num=32)
    # data_list = task_obj.load_jsonl("test.jsonl")
    data_list = {"key1": "你好", "key2": "好的"}
    res_list = task_obj.multi_task_processing(data_list, fun_job, **data_list)
    print(len(res_list))
    print(res_list[0])
