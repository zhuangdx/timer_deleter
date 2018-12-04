#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 16:32
# @Author  : duoxuan·zhuang
# @File    : handle.py
"""
从配置文件读取指定路径，删除超过时间的过期指定类型文件 （适用于linux）
逻辑：
1.读取配置文件---多个路径
2.遍历路径，读取类型，时间
3.获取过期文件数量-删除文件
4.获取空文件夹数量-删除空文件夹
"""
import datetime
import json
import logging
import logging.config

import os
import sys

from utils import os_tools

logging.config.fileConfig("./conf/log.conf")


# 获取文件数量
check_file_count = ' | wc -l'
day_find = ' -mtime +%s '
# 获取7天前的文件
get_file_s = "find %s"
# 指定文件类型
filter_type = ' -name "%s" '
# 筛选空文件夹
empty_folder = " -maxdepth 1 -type d -empty "
# 删除
delete_cmd = " -exec rm -rf {} \;"


class CosSyncConfig(object):
    """从本地json文件读取配置"""

    def __init__(self, config_path=u'config.json'):
        if not os.path.isfile(config_path):
            self.init_config_err = u'配置文件 %s 不存在' % config_path
            self.init_config_flag = False
            return

        config_file = open(config_path, 'r', encoding="utf-8")
        try:
            config_str = config_file.read()
            self.config_json = json.loads(config_str)
        except json.decoder.JSONDecodeError:
            self.init_config_err = u'配置文件格式无法识别'
            self.init_config_flag = False
            return
        finally:
            config_file.close()

        valid_config_key_arr = ['路径', '文件类型', '过期时间']

        for json1 in self.config_json:
            for config_key in valid_config_key_arr:
                if config_key not in json1.keys():
                    self.init_config_err = u'没有配置key %s' % config_key
                    self.init_config_flag = False
                    return

        self.init_config_flag = True
        self.init_config_err = u''

    def is_valid_config(self):
        return self.init_config_flag

    def get_err_msg(self):
        return self.init_config_err


def run_shell_8_result(shell_str):
    """
    运行命令行，返回运行结果
    :param shell_str:
    :return:
    """
    return os_tools.run_cmd_block(shell_str)


def get_cmd_count(cmd_str):
    """
    获取该命令的结果行数--int
    :param cmd_str:
    :return:
    """
    cmd_str_count = cmd_str + check_file_count
    rr = run_shell_8_result(cmd_str_count)
    rr_list = rr.split()
    return int(rr_list[0])


def get_file_7_day(path, _type='', day='7'):
    """
    筛选过期文件，1.先获取文件并删除 2.查找空文件夹并删除
    :param path:
    :param _type:
    :param day:
    :return:
    """
    if day == '0':
        cmd_str = get_file_s % path + filter_type % _type
    else:
        cmd_str = get_file_s % path + day_find % day + filter_type % _type
    logging.info(cmd_str)
    count_f = get_cmd_count(cmd_str)
    if count_f:
        logging.info('文件数量：%d', count_f)
        logging.info('过期文件：')
        logging.info('\n' + run_shell_8_result(cmd_str))
        logging.info('\n' + run_shell_8_result(cmd_str + delete_cmd))

    # 删除空文件夹
    cmd_str_empty = get_file_s % path + empty_folder
    count_f = get_cmd_count(cmd_str_empty)
    if len(os.listdir(path)) > 0 and count_f:
        logging.info('空文件夹数量：%d', count_f)
        logging.info('具体文件夹：')
        logging.info('\n' + run_shell_8_result(cmd_str_empty))
        logging.info('\n' + run_shell_8_result(cmd_str_empty + delete_cmd))


def main(conf_file="conf/config.json"):
    logging.info('**  %s', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    config = CosSyncConfig(conf_file)

    if not config.is_valid_config():
        logging.error('wrong config: ' + config.get_err_msg())
        logging.info("\n\n")
        sys.exit(1)

    for onejson in config.config_json:
        folder_path = onejson['路径']
        file_type = onejson['文件类型']
        file_time = onejson['过期时间']
        if os.path.exists(folder_path):
            get_file_7_day(path=folder_path, _type=file_type, day=file_time)
        else:
            logging.warning("不存在 %s", folder_path)
    logging.info("\n\n")


if __name__ == "__main__":
    main()
