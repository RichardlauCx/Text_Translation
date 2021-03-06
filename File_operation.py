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


def extraction_of_text(path_in, path_out, _output_purpose=sys.stdout):
    """
    实现对应文本的汉化功能
    :param _output_purpose:  标准输出地（进度条视图）
    :param path_in: 数据输入路径
    :param path_out: 数据输出路径
    :return: 翻译成功之后的json数据
    """
    pattern_i = r"^msgid \".+\""   # 在这里可以把加号"+"，改为所需查询的数字范围，format：{0,21}
    pattern_e = "[A-Za-z]+"
    last = 0  # 设置翻译起始的节点，文字索引位置
    # scale = 0  # 翻译进度比例

    # 1. 获取数据
    with open(path_in, "r") as f_obj:
        # line = "start"  # 对于存在单词的行进行获取
        lines = f_obj.readlines()
        num_line = len(lines)

        for scale in range(num_line):
            line = lines[scale]
            lists = re.findall(pattern_i, line)

            if len(lists) is not 0:
                string_initial = str(lists[0][7:-1])  # 包含特殊字符的字符串
                string_extraction = ""  # 待翻译的单词或句子
                string_temp = re.findall(pattern_e, string_initial)
                for str_part in string_temp:
                    string_extraction += " " + str_part

                # 2. 文本翻译
                string_after = translation(string_initial)  # 翻译成功之后的json
                result_dst = string_after['trans_result'][0]['dst']  # 翻译之后的汉语

                # 3. 写入文件
                f_1 = open(path_in, "r")
                text_1 = f_1.read()
                f_1.close()

                pattern_txt = re.compile(string_initial)  # 留一个模式

                try:
                    scale += 2

                    # 4. 实现进度条
                    percentage = int((scale / num_line) * 100)
                    a = "▮" * (percentage // 2)
                    b = "▯" * (50 - (percentage // 2))
                    _output_purpose.write('\r' + time.strftime("%Y-%m-%d-%H:%M:%S: ", time.localtime())
                                          + " StateOfTranslationTemplate: {}%: [{}{}]".format(percentage, a, b))  # 调整这里
                    _output_purpose.flush()
                    index = text_1.find(string_initial, last) + len(string_initial) + 10  # 解决输出，存入相同位置问题
                    # if text_1[index:index+2] != '"':  # 此跳过已有数据方法待完善
                    #     continue

                except AttributeError as e:
                    continue

                else:
                    last = index
                    text_updates = text_1[:index] + result_dst + text_1[index:]
                    f_2 = open(path_out, "w")
                    f_2.write(text_updates)

                    f_2.close()

                finally:
                    f_1.close()

    return string_after


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

        return result

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    path_words = "Wait_for_the_translation.txt"  # 获取数据来源文件
    path_deposit = path_words  # 文本翻译后的输出路径（和获取数据路径一直，即覆盖原数据）
    output_purpose = None  # 标准输出地（进度条视图）

    extraction_of_text(path_words, path_deposit)
