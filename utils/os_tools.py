# -*- coding: utf-8 -*-

import subprocess


def run_cmd_block(cmd):
    """
    运行命令行，并堵塞线程，返回运行结果
    :param cmd:
    :return:
    """
    re = run_cmd_async(cmd)
    return get_running_cmd_return(re)


def run_cmd_async(shell_str):
    """非堵塞，调用命令行, 返回类变量，需自行获取运行结果"""
    shell_result = subprocess.Popen(shell_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return shell_result


def get_running_cmd_return(sub_obj):
    """获取命令行运行结果"""
    bytes_data = sub_obj.stdout.read()
    return bytes_data.decode("utf8", "ignore")
