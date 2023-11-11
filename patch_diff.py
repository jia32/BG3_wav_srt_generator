#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：BG3_party_banter 
@File    ：patch_diff.py
@Author  ：Jasmine
@Date    ：2023/11/9 13:57 
'''

import os
import filecmp
from constant import *


def compare_folders(folder1, folder2, depth=0):
    comparison = filecmp.dircmp(folder1, folder2)
    report = []

    # 遍历在folder2中独有的文件
    for file_only_in_folder2 in comparison.right_only:
        file_path = os.path.join(folder2, file_only_in_folder2)
        indentation = "  " * depth
        report.append(f"{indentation}Added: {file_path}")

    # 遍历在folder1中独有的文件
    for file_only_in_folder1 in comparison.left_only:
        file_path = os.path.join(folder1, file_only_in_folder1)
        indentation = "  " * depth
        report.append(f"{indentation}Removed: {file_path}")

    # 递归比较子文件夹
    for subfolder in comparison.common_dirs:
        subfolder1 = os.path.join(folder1, subfolder)
        subfolder2 = os.path.join(folder2, subfolder)
        indentation = "  " * depth
        report.append(f"{indentation}Subfolder: {subfolder}")
        subfolder_report = compare_folders(subfolder1, subfolder2, depth + 1)
        report.extend(subfolder_report)
    return report


def find_different_files(version1, version2):
    '''

    :param version1:
    :param version2:
    :return:
    '''

    comparison_report = compare_folders(version1, version2)

    output_file = rf"{base_path}\new_patch\report.txt"
    with open(output_file, "w") as file:
        for line in comparison_report:
            file.write(line + "\n")


def difference_of_existing_files(curr_version):
    '''

    :param curr_version:
    :return:
    '''
    return