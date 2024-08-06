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
from utils import *
from local_db import *

current_patch_version = "patch6"
current_patch_wem_path = f"{current_patch_version}_wem"
current_patch_report_path = f"{current_patch_version}_report"
current_patch_voicemeta_report_path = f"{current_patch_version}_voicemeta_report"
current_patch_report_impossible_flag_path = f"{current_patch_version}_flag_analysis_report"


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


def find_different_files(version1, version2, output_name):
    '''

    :param output_name:
    :param version1:
    :param version2:
    :return:
    '''

    comparison_report = compare_folders(version1, version2)

    output_file = rf"{base_path}\new_patch\{current_patch_version}\report_{output_name}.txt"
    with open(output_file, "w") as file:
        for line in comparison_report:
            file.write(line + "\n")


def difference_of_existing_files(curr_version):
    '''

    :param curr_version:
    :return:
    '''
    return


def compare_file_size(last_version, curr_version):
    # 指定之前记录文件大小的文件夹路径
    previous_file_sizes = {}

    # 遍历之前记录文件大小的文件夹结构
    for root, dirs, files in os.walk(last_version):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            previous_file_sizes[file_name] = file_size

    # 调用函数比较文件大小
    output_file_diff(curr_version, previous_file_sizes)


def output_file_diff(folder_path, previous_file_sizes):
    # 存储文件名和对应的大小
    file_sizes = {}

    # 遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            file_sizes[file_name] = file_size

    # 打开输出文件
    output_file_path = rf"{base_path}\new_patch\{current_patch_version}\report_size.txt"
    with open(output_file_path, "w") as output_file:
        # 遍历文件夹及其子文件夹
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                # 获取文件大小
                file_size = os.path.getsize(file_path)

                # 检查文件是否存在先前的记录
                if file_name not in previous_file_sizes:
                    continue

                # 检查文件大小是否有变化
                previous_size = previous_file_sizes[file_name]
                if file_size > previous_size:
                    difference = file_size - previous_size
                    output_file.write(f"文件 {file_name} 变大了 {difference} 字节\n")
                elif file_size < previous_size:
                    difference = previous_size - file_size
                    output_file.write(f"文件 {file_name} 变小了 {difference} 字节\n")


def copy_updated_file_by_ch(reference, ch_name, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    with open(reference, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    speaker = get_speakercode_by_ch(ch_name)
    if speaker is None:
        print(f" {ch_name} code not found, pls manually find it and add to const.")

    to_be_copied = []
    for line in lines:
        if speaker in line:
            if "Added" in line:
                to_be_copied.append(line.strip().replace("Added: ", ""))
            else:
                print(line)

    print(f"{len(to_be_copied)} to be copied")

    for item in to_be_copied:
        copied_path = shutil.copy(item, target_path)
        print(f"{copied_path} is copied")


def find_flag_by_word(key_string):
    flag_list = search_in_file(flag_meta_file_path, key_string, False)
    for flag_file in flag_list:
        with open(flag_file, 'r') as file:
            flag_json = json.load(file)
        print(f"{flag_json['save']['regions']['Flags']['Name']['value']}： "
              f"{flag_json['save']['regions']['Flags']['Description']['value']}")
        print()


def find_flagname_by_tag(tag_list):
    for tag in tag_list:
        find_flag_by_word(tag)


def find_flag_by_lsj(lsj_path):
    checkflag_list = []
    setflag_list = []

    with open(lsj_path, 'r') as file:
        lsj_json = json.load(file)

    for node in lsj_json["save"]["regions"]["dialog"]["nodes"][0]['node']:
        if "checkflags" in node:
            if "flaggroup" in node['checkflags'][0]:
                for flag in node['checkflags'][0]['flaggroup']:
                    checkflag_list.append(flag['flag'][0]['UUID']['value'])
        if "setflags" in node:
            if "flaggroup" in node['setflags'][0]:
                for flag in node['setflags'][0]['flaggroup']:
                    setflag_list.append(flag['flag'][0]['UUID']['value'])

    checkflag_list = list(set(checkflag_list))
    setflag_list = list(set(setflag_list))

    print(f"{len(checkflag_list)} flags to be checked")
    for checkflag in checkflag_list:
        flag_path = rf"{flag_meta_file_path}{checkflag}.lsf.lsj"
        try:
            with open(flag_path, 'r') as file:
                flag_json = json.load(file)
            print(f"{flag_json['save']['regions']['Flags']['Name']['value']}： "
                  f"{flag_json['save']['regions']['Flags']['Description']['value']}")
        except Exception as e:
            print(f"Error reading file {flag_path}: {e}")

    print(f"{len(setflag_list)} flags to be checked")
    for setflag in setflag_list:
        flag_path = rf"{flag_meta_file_path}{setflag}.lsf.lsj"
        try:
            with open(flag_path, 'r') as file:
                flag_json = json.load(file)
            print(f"{flag_json['save']['regions']['Flags']['Name']['value']}： "
                  f"{flag_json['save']['regions']['Flags']['Description']['value']}")
        except Exception as e:
            print(f"Error reading file {flag_path}: {e}")


def copy_wem_file_new_patch(ch_name):
    job_name = "voice"
    filename_list = rf"{base_path}\new_patch\{current_patch_version}\report_{job_name}.txt"
    target_path = rf"{base_path}{ch_name}\{current_patch_wem_path}\\"

    copy_updated_file_by_ch(filename_list, ch_name, target_path)


def compare_voicemeta_source(last_db_version, current_db_version):
    old_table = f"lookup_voicemeta_{last_db_version}"
    new_table = f"lookup_voicemeta_{current_db_version}"
    output_file_file = rf"{base_path}\new_patch\{current_patch_voicemeta_report_path}.json"

    # 创建数据库引擎
    engine = create_engine(mysql_url)

    # 创建会话工厂
    Session = sessionmaker(bind=engine)

    # 创建会话
    session = Session()

    # 查看新增的语音
    query = select(
        text('t2.*')
    ).select_from(
        text(f'{new_table} AS t2')
    ).join(
        text(f'{old_table} AS t1'),
        text('t2.contentuid = t1.contentuid'),
        isouter=True
    ).where(
        text('t1.source IS NULL')
    )
    result = session.execute(query)

    output_list = []
    for row in result:
        # 使用row来访问每个字段的值
        contentuid = row.contentuid
        source = row.source
        print(f"ContentUID: {contentuid}, wem_path: {source}")
        output_list.append({"contentuid": contentuid, "source": source})

    session.commit()
    session.close()

    with open(output_file_file, 'w') as output_file:
        json.dump(output_list, output_file)

    return


def generate_report_based_on_flags():
    with open(flag_report_path, 'r', encoding='utf-8') as f_in:
        # Load the complete JSON object from the input file
        json_data = json.load(f_in)

    merged_data = {}
    for item in json_data['RECORDS']:
        path = item["path"]
        if path in merged_data:
            merged_data[path]["data"].append({
                "contentuid": item["contentuid"],
                "ch": item["ch"],
                "eng": item["eng"]
            })
            merged_data[path]["count"] += 1
        else:
            merged_data[path] = {
                "path": path,
                "data": [{
                    "contentuid": item["contentuid"],
                    "ch": item["ch"],
                    "eng": item["eng"]
                }],
                "count": 1
            }

    result = list(merged_data.values())

    print(f"added {len(result)}")

    output_file_file = rf"{base_path}\new_patch\{current_patch_report_impossible_flag_path}.json"
    # output_file_file = rf"{base_path}\Astarion\BecameVampireLord.json"

    with open(output_file_file, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=4, ensure_ascii=False)

    # 按照 count 从大到小对列表进行排序
    sorted_list = sorted(result, key=lambda x: x["count"], reverse=True)

    # 提取 path 和 count 构建新的列表
    path_list = [{"path": item["path"], "count": item["count"]} for item in sorted_list]
    print(json.dumps(path_list, indent=4, ensure_ascii=False))


def generate_report_by_lsj(last_db_version, current_db_version):
    old_table = f"lookup_voicemeta_{last_db_version}"
    new_table = f"lookup_voicemeta_{current_db_version}"

    # 获取会话
    session = connection_pool.get_session()
    # 查看新增的语音
    query = select(
        text('nlsj.path AS lsj_path'),
        text('nvm.contentuid AS contentuid'),
        text('nct.content AS ch_content'),
        text('net.content AS eng_content'),
        text('nvm.source AS new_wem_path')
    ).select_from(
        text(f'{new_table} AS nvm')
    ).join(
        text(f'{old_table} AS ovm'),
        text('nvm.contentuid = ovm.contentuid'),
        isouter=True
    ).join(
        text(f'{ch_table} AS nct'),
        text('nct.contentuid = nvm.contentuid'),
        isouter=False
    ).join(
        text(f'{eng_table} AS net'),
        text('net.contentuid = nct.contentuid'),
        isouter=False
    ).join(
        text(f'lookup_script_node_{db_version} AS nnd'),
        text('nnd.tagtext = nvm.contentuid'),
        isouter=False
    ).join(
        text(f'lookup_script_{db_version} AS nlsj'),
        text('nlsj.uuid = nnd.script_uuid'),
        isouter=False
    ).where(
        text("ovm.source IS NULL")
    )
    result = session.execute(query)

    data_list = []
    for row in result:
        # 使用row来访问每个字段的值
        path = row.lsj_path
        contentuid = row.contentuid
        wem_path = row.new_wem_path
        ch = row.ch_content
        eng = row.eng_content
        # print(path, contentuid, wem_path, ch, eng)
        data_list.append({"contentuid": contentuid, "source": wem_path, "path": path, "ch": ch, "eng": eng})
    # 关闭会话并返回连接到连接池
    connection_pool.close_session(session)

    merged_data = {}

    for item in data_list:
        path = item["path"]
        if path in merged_data:
            merged_data[path]["data"].append({
                "contentuid": item["contentuid"],
                "source": item["source"],
                "ch": item["ch"],
                "eng": item["eng"],
                "speaker": get_speaker_by_wemname(item["source"])
            })
            merged_data[path]["count"] += 1
        else:
            merged_data[path] = {
                "path": path,
                "data": [{
                    "contentuid": item["contentuid"],
                    "source": item["source"],
                    "ch": item["ch"],
                    "eng": item["eng"],
                    "speaker": get_speaker_by_wemname(item["source"])
                }],
                "count": 1
            }

    result = list(merged_data.values())

    print(f"added {len(result)} in {current_db_version}")

    output_file_file = rf"{base_path}\new_patch\{current_patch_report_path}.json"
    with open(output_file_file, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=4, ensure_ascii=False)

    # 按照 count 从大到小对列表进行排序
    sorted_list = sorted(result, key=lambda x: x["count"], reverse=True)
    with open(output_file_file, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=4, ensure_ascii=False)

    # 提取 path 和 count 构建新的列表
    path_list = [{"path": item["path"], "count": item["count"]} for item in sorted_list]
    print(json.dumps(path_list, indent=4, ensure_ascii=False))


def get_speaker_by_wemname(filename):
    filename = filename[:-4]
    if "_" in filename:
        charactor = filename.split('_', 1)[0]
        if charactor in speaker_code_ch:
            speaker = speaker_code_ch[charactor]
        else:
            speaker = ""
    return speaker


def find_lsj_by_wem(char):
    wem_path = rf"{base_path}{char}\{current_patch_wem_path}\\"
    output_file_file = rf"{base_path}{char}\{current_patch_report_path}.json"
    tmp_report = {}
    report = {}

    for root, dirs, files in os.walk(wem_path):
        for wav_file in files:
            wem_path = f"{wav_file[:-3]}wem"
            contentuid = find_contentuid_by_wemfile(wem_path)
            # return
            # tmp = f"123_{contentuid}.wav"
            line = generate_line_srt_by_filename(wav_file, False, False, {})
            print(contentuid)
            lsj_file = search_in_file(all_lsj_path, contentuid, False)
            tmp_report[line] = lsj_file

    for line, lsj_list in tmp_report.items():
        for lsj in lsj_list:
            if lsj not in report:
                report[lsj] = [line]
            else:
                report[lsj].append(line)

    with open(output_file_file, 'w') as output_file:
        json.dump(report, output_file)


def find_contentuid_by_wemfile(wem_path):
    voice_meta_table = f"lookup_voicemeta_{db_version}"
    meta_file = locate_lsj(wem_path)
    print(meta_file)
    if not meta_file:
        return

    # 创建数据库引擎
    engine = create_engine(mysql_url)

    # 创建会话工厂
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(
        text('*'),
    ).select_from(
        text(f'{voice_meta_table}'),
    ).where(
        text('source = :source')
    )
    result = session.execute(query, {'source': wem_path})

    session.commit()

    session.close()
    rows = result.fetchall()
    row_count = len(rows)
    print(row_count)

    for row in rows:
        # print(row.contentuid, row.codec, row.duration, row.priority, row.source)
        return row.contentuid

    # with open(meta_file, 'r') as file:
    #     meta_json = json.load(file)
    #
    # for voiceSpeakerMetaData in meta_json['save']['regions']['VoiceMetaData']['VoiceSpeakerMetaData'][0]['MapValue'][0][
    #     'VoiceTextMetaData']:
    #     if voiceSpeakerMetaData['MapValue'][0]['Source']['value'] == wem_path:
    #         # print(voiceSpeakerMetaData)
    #         return voiceSpeakerMetaData['MapKey']['value']


def copy_lsj_to_script(char):
    report_json_path = rf"{base_path}{char}\{current_patch_report_path}.json"
    target_path = rf"{base_path}{char}\script\\"

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    with open(report_json_path, 'r') as file:
        report_json = json.load(file)

    for lsj_path, line_list in report_json.items():
        copied_path = shutil.copy(lsj_path, target_path)
        print(f"{copied_path} is copied")


def find_lsj_ch_keyword(char, keyword, job_name):
    output_json_path = rf"{report_location}{job_name}.json"
    output_line_path = rf"{report_location}{job_name}.txt"
    uid_list = find_content_with_string(keyword)
    print(uid_list)
    wem_meta = {}
    result = {}
    line_result = ""
    matches = []

    if matches is not None and len(matches) == 0:
        matches = find_through_metafile(uid_list, get_speakercode_by_ch(char))

    for uid in uid_list:
        pattern = f"{get_speakercode_by_ch(char)}_{uid}.wem*"
        for root, dirs, files in os.walk(voice_location):
            for filename in fnmatch.filter(files, pattern):
                matches.append(filename)

        if matches is not None and len(matches) != 0:
            matches = filter_strings_with_pattern(matches, pattern)

        if matches is not None and len(matches) != 0:
            line = generate_line_srt_by_filename(matches[0], False, True, {})
            print(f"find '{line}' with filename {matches[0]}")
            line_result += line + "\n"
            result[uid] = matches

    print(result)
    print(f"found {len(result)} lines ")
    with open(output_json_path, 'w') as output_file:
        json.dump(result, output_file)
    print(f"output report to {output_json_path}")
    with open(output_line_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(line_result)
    print(f"output line to {output_line_path}")


def parse_xml(file_path):
    current_tree = load_xml_file(file_path)
    root = current_tree.getroot()
    # Extract content uids and content
    content_data = {}
    for item in root.iter('content'):
        content = item.text
        content_uid = item.get('contentuid')
        content_data[content_uid] = content
    return content_data


def compare_xml(file1_path, file2_path):
    file1_data = parse_xml(file1_path)
    file2_data = parse_xml(file2_path)

    new_added_content = [uid for uid in file2_data if uid not in file1_data]

    different_content = [uid for uid in file1_data if uid in file2_data and file1_data[uid] != file2_data[uid]]

    # Generate the report
    print("New added content uids:")
    for uid in new_added_content:
        print(file2_data[uid])

    print("\nContent uids with different content:")
    for uid in different_content:
        print(f"from {file1_data[uid]} to {file2_data[uid]}")
