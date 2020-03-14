# -*- coding: utf-8 -*-
#  @ Date   : 2020/3/9 10:36
#  @ Author : RichardLau_Cx
#  @ file   : File_operation.py
#  @ IDE    : PyCharm

import http.client
import hashlib
import urllib
import random
import json
import time
import sys
import re


def extraction_of_text(path_in, path_out):
    """
    实现对应文本的汉化功能
    :param path_in: 数据输入路径
    :param path_out: 数据输出路径
    :return: 翻译成功之后的json数据
    """
    pattern_i = r"^msgid \".+\""
    pattern_e = "[A-Za-z]+"
    last = 0  # 设置翻译起始的节点

    # 0. 获取文件信息
    with open(path_in, "r") as f_obj:
        # 获取文件总行数
        num_lines = len(f_obj.readlines())

    # 1. 获取数据
    with open(path_in, "r") as f_obj:
        line = "start"  # 对于存在单词的行进行获取
      
        while line is not '':
            line = f_obj.readline()
            lists = re.findall(pattern_i, line)  # 在这里可以把加号"+"，改为所需查询的数字范围，format：{0,21}
            # print(lists)

            if len(lists) is not 0:
                string_initial = str(lists[0][7:-1])  # 包含特殊字符的字符串
                string_extraction = ""  # 待翻译的单词或句子
                string_temp = re.findall(pattern_e, string_initial)
                for str_part in string_temp:
                    string_extraction += " " + str_part

                # 2. 文本翻译
                print(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))

                string_after = translation(string_initial)  # 翻译成功之后的json
                print(string_after)
                # result_dst = string_after['trans_result'][0]['dst']  # 翻译之后的汉语
                # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
                # print(time.time())

                # 3. 写入文件
                f_1 = open(path_in, "r")
                text_1 = f_1.read()
                f_1.close()

                pattern_txt = re.compile(string_initial)

                try:
                    # index = re.search(pattern_txt, text_1).span()[1]+10
                    index = text_1.find(string_initial, last) + len(string_initial) + 10  # 解决输出，存入相同位置问题
                    # if text_1[index:index+2] != '"':  # 此跳过已有数据方法待完善
                    #     continue

                except AttributeError as e:
                    continue

                else:
                    last = index
                    # time.sleep(0.5)
                    # print(result_dst)
                    # text_updates = text_1[:index] + result_dst + text_1[index:]
                    # f_2 = open(path_out, "w")
                    # f_2.write(text_updates)
                    # # print(result_dst)
                    #
                    # f_2.close()
                finally:
                    f_1.close()

    # return string_after


def translation(sentence):
    appid = ''  # 填写你的appid
    secretKey = ''  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = 'auto'  # 原文语种
    toLang = 'zh'  # 译文语种
    salt = random.randint(32768, 65536)
    q = sentence + "\n"
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()  # 变成16进制
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        # result_all = response.read().decode('gbk')
        result = json.loads(result_all)

        # print(result)
        return result

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

# 进度条
def progress_bar_1(num):
    for i in range(1, 101):
        print("\r", end="")
        print("StateOfTranslationTemplate: {}%: ".format(i), "▋" * (i // 2), end="")
        sys.stdout.flush()
        time.sleep(0.5)


if __name__ == '__main__':
    # path_words = "Wait_for_the_translation_pre.txt"  # 可以改为对应的网址路径
    # path_words = "Ext_after_translation.txt"
    # path_deposit = "Ext_after_translation.txt"  # 文本翻译后的输出路径（和获取数据路径一直，即覆盖原数据）
    
    path_words = "Wait_for_the_translation.txt"
    path_deposit = path_words
    extraction_of_text(path_words, path_deposit)

