import re
import csv
import fnmatch
import shutil
from constant import *
from local_db import *
import wave


def get_wav_duration(file_path):
    with wave.open(file_path, "rb") as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        rounded_duration = round(duration, 6)
        return rounded_duration



def output_dialog_txt_file(output_string):
    output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_dialog}"
    file = open(output_path, "w", encoding='utf-8')
    file.write(output_string)
    print(f"writing dialog txt to {output_path}")
    file.close()


def output_json_file(output_json):
    output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{tmp_content_json}"
    with open(output_path, "w", encoding="utf-8") as file:
        # Write the JSON data to the file
        json.dump(output_json, file, ensure_ascii=False)


def generate_output_list(file_name, content_string):
    # print(file_name)
    content_ch = ""
    for item in content_string:
        if "ch" in item:
            content_ch += str(item["ch"]) + "\n"
            content_ch += str(item["eng"]) + "\n"
        else:
            content_ch += str(item["eng"]) + "\n"
    # content_ch = [str(item["ch"]) for item in content_string]

    # Join the values with a newline character separator
    # dialog = "\n".join(content_ch)
    result = file_name[3:-4] + "\n" + content_ch + "\n" + "\n"
    print(result)
    return result


def render_json(ori_json):
    nodes_map = {}
    root_node = None
    speaker_list = get_speaker_list(ori_json["save"]["regions"]["dialog"]["speakerlist"][0]['speaker'])
    # print(len(ori_json["save"]["regions"]["dialog"]["nodes"][0]['node']))

    for node in ori_json["save"]["regions"]["dialog"]["nodes"][0]['node']:
        nodes_map[node["UUID"]['value']] = generate_new_node(node, speaker_list)
    # print(nodes_map)

    for node in ori_json["save"]["regions"]["dialog"]["nodes"][0]['node']:
        if "Root" in node and node["Root"]['value'] is True:
            root_node = generate_new_node(node, speaker_list)
            break
    # print(root_node)

    new_list = []
    visited = set()

    def dfs(node_uuid):
        nonlocal new_list, visited

        if node_uuid in visited:
            return

        visited.add(node_uuid)
        tmp_node = nodes_map[node_uuid]

        for child_info in reversed(tmp_node["children"]):
            if 'child' in child_info:
                child_uuid = child_info["child"][0]["UUID"]["value"]
                dfs(child_uuid)

        new_list.append(tmp_node)

    dfs(root_node['UUID'])

    # for node in new_list:
    #     print(node['contentuid'])

    new_list.reverse()

    return new_list


def get_speaker_list(speaker_list):
    result = []
    for speaker in speaker_list:
        if speaker['list']['value'] in speaker_name:
            name = speaker_name[speaker['list']['value']]
        else:
            name = "unknown"
        if speaker['list']['value'] in speaker_name_ch:
            ch_name = speaker_name_ch[speaker['list']['value']]
        else:
            ch_name = "unknown"

        out_speaker = {
            "index": int(speaker['index']['value']),
            "name": name,
            "ch_name": ch_name
        }
        result.append(out_speaker)
    return result


def generate_new_node(node_json, speaker_list):
    # print(node_json)
    if "TaggedTexts" in node_json:
        if "TaggedText" in node_json["TaggedTexts"][0]:
            contentuid = node_json["TaggedTexts"][0]['TaggedText'][0]['TagTexts'][0]['TagText'][0]['TagText']['handle']
        else:
            contentuid = ""
    else:
        contentuid = ""
    if "speaker" in node_json:
        speaker = node_json["speaker"]
    else:
        speaker = "default"

    new_node = {
        "UUID": node_json["UUID"]['value'],
        "speaker": get_speaker_name(speaker, speaker_list),
        "contentuid": contentuid,
        "children": node_json['children']
    }
    return new_node


def get_speaker_name(input_json, speaker_list):
    for speaker in speaker_list:
        if "value" in input_json:
            if speaker['index'] == input_json['value']:
                return {
                    "speaker_name": speaker['name'],
                    "speaker_name_ch": speaker['ch_name']
                }
        else:
            return {
                "speaker_name": "unknown",
                "speaker_name_ch": "unknown"
            }


def filled_string(content_list):
    """
    add string to content list, look it up with contentuid in xml file
    :param content_list:
    :return:
    """
    # Parse the XML string to a tree structure
    file_name = "/Data/Input/english_patch6.xml"
    file_name_ch = "/Data/Input/chinese_patch6.xml"
    # Get the directory path of the current file
    xml_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{file_name}"
    xml_path_ch = f"{os.path.dirname(os.path.abspath(__file__))}\\{file_name_ch}"

    # Parse the XML file
    tree = ET.parse(xml_path)
    tree_ch = ET.parse(xml_path_ch)

    # Get the root element
    root = tree.getroot()
    root_ch = tree_ch.getroot()

    for content in content_list:
        if content['contentuid'] != "":

            content_elem = root.find(f"./content[@contentuid='{content['contentuid']}']")
            if content_elem is not None:
                # Extract the content of the content element
                content_string = content_elem.text
                if "speaker" in content and content['speaker'] is not None:
                    content['eng'] = f"{content['speaker']['speaker_name']}: {content_string} "

                else:
                    content['eng'] = f"{content_string}"  # \n{content['contentuid']}"
            else:
                content['eng'] = ""

            content_elem_ch = root_ch.find(f"./content[@contentuid='{content['contentuid']}']")
            if content_elem_ch is not None:
                # Extract the content of the content element
                content_string = content_elem_ch.text
                if "speaker" in content and content['speaker'] is not None:
                    content['ch'] = f"{content['speaker']['speaker_name_ch']}: {content_string}"
                else:
                    content['ch'] = f"{content_string}"
            else:
                content['ch'] = ""
        # Print the content
    # print(content_list)
    return content_list


def write_output_json(input_file, output_file):
    # Open the input file with the correct encoding (e.g., UTF-8) for reading and output file for writing
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        # Load the complete JSON object from the input file
        json_data = json.load(f_in)

        # Define a function to recursively process and modify JSON objects
        def process(obj):
            if isinstance(obj, dict):
                # Process key-value pairs in dicts
                for key, value in obj.items():
                    if isinstance(value, str) and '"' in value:
                        # Check if the value contains double quotes
                        if value.startswith('"') and value.endswith('"'):
                            # Replace quotes only within double quotes
                            obj[key] = re.sub(r'(?<!\\)"(.*?)(?<!\\)"', r'\\"\1\\"', value)
                    elif isinstance(value, dict) or isinstance(value, list):
                        # Recursively process nested dicts or lists
                        process(value)
            elif isinstance(obj, list):
                # Process elements in lists
                for index, value in enumerate(obj):
                    if isinstance(value, str) and '"' in value:
                        # Check if the value contains double quotes
                        if value.startswith('"') and value.endswith('"'):
                            # Replace quotes only within double quotes
                            obj[index] = re.sub(r'(?<!\\)"(.*?)(?<!\\)"', r'\\"\1\\"', value)
                    elif isinstance(value, dict) or isinstance(value, list):
                        # Recursively process nested dicts or lists
                        process(value)

        # Process the loaded JSON object recursively to modify values
        process(json_data)

        # Write the modified JSON object as a valid JSON to the output file
        json.dump(json_data, f_out, ensure_ascii=False)


def load_text_from_lsj(content, need_note):
    json_content_list = []
    current_node = {}
    for node in content["save"]["regions"]["dialog"]["nodes"][0]['node']:
        line_list = []
        if "TaggedTexts" in node:
            # print(node)
            for dialog in node["TaggedTexts"]:
                # print(dialog)
                if "TaggedText" in dialog:
                    for tagtext in dialog['TaggedText']:
                        # print(tagtext)
                        for line in tagtext['TagTexts'][0]['TagText']:
                            # if 'OldText' in line:
                            #     contentuid =f"{line['OldText']['handle']}/{line['TagText']['handle']}"
                            # else:
                            contentuid = line['TagText']['handle']
                            line_list.append({
                                "contentuid": contentuid,
                            })
                            # print(line_list)
                        if need_note:
                            if "editorData" in node:
                                for data in node['editorData'][0]['data']:
                                    if "key" in data and "value" in data['key']:
                                        if data['key']['value'] == "NodeContext" and data['val']['value'] != "":
                                            current_node = {
                                                "content_list": line_list,
                                                "note": data['val']['value']
                                            }
                            else:
                                current_node = {
                                    "content_list": line_list,
                                }
                        else:
                            current_node = {
                                "content_list": line_list,
                            }
                        print(current_node)
                    else:
                        contentuid = ""

                    json_content_list.append(current_node)
    return json_content_list


def load_text_from_lsj_tmp_not_working(content, need_note):
    json_content_list = []
    for root_node in content["save"]["regions"]["dialog"]["nodes"][0]['RootNodes']:

        for node in content["save"]["regions"]["dialog"]["nodes"][0]['node']:
            if node['UUID'] == root_node['value']:
                line_list = []
                json_content_list = load_contentuid_in_node(node, need_note, json_content_list)
                while node['children'] != [{}]:
                    for child_node in node['children']:
                        child_node['']
                    for current_node in content["save"]["regions"]["dialog"]["nodes"][0]['node']:
                        if current_node['UUID'] == node['value']:
                            return

    return json_content_list


def load_contentuid_in_node(node, need_note, json_content_list):
    line_list = []
    if "TaggedTexts" in node:
        # print(node)
        for dialog in node["TaggedTexts"]:
            # print(dialog)
            if "TaggedText" in dialog:
                for tagtext in dialog['TaggedText']:
                    # print(tagtext)
                    for line in tagtext['TagTexts'][0]['TagText']:
                        # if 'OldText' in line:
                        #     contentuid =f"{line['OldText']['handle']}/{line['TagText']['handle']}"
                        # else:
                        contentuid = line['TagText']['handle']
                        line_list.append({
                            "contentuid": contentuid,
                        })
                        # print(line_list)
                    if need_note:
                        if "editorData" in node:
                            for data in node['editorData'][0]['data']:
                                if "key" in data and "value" in data['key']:
                                    if data['key']['value'] == "NodeContext" and data['val']['value'] != "":
                                        current_node = {
                                            "content_list": line_list,
                                            "note": data['val']['value']
                                        }
                        else:
                            current_node = {
                                "content_list": line_list,
                            }
                    else:
                        current_node = {
                            "content_list": line_list,
                        }
                    print(current_node)
                else:
                    contentuid = ""

                json_content_list.append(current_node)
    return json_content_list


def print_text_from_lsj(json_content_list, other_value):
    out_string = ""
    unique_list = []
    for d in json_content_list:
        if d['content_list'] not in unique_list:
            unique_list.append(d)

    for line in unique_list:
        json_content_string = filled_string(line['content_list'])
        # print(json_content_string)
        # if "negative" in line['note']:
        if "note" in line:
            print(line['note'])
        for sentence in json_content_string:
            latin = sentence['eng'].split('<br>')[0]
            for ending in [" v3", " v2", " v1"]:
                if latin.endswith(ending):
                    latin = latin[:-len(ending)]

            print(f"{latin}")
            print(f"{sentence['contentuid']}")
            out_string += f"{latin}\n{sentence['contentuid']}\n"
        print()
    return out_string
    # output_string += generate_output_list("txt: ", json_content_string)
    #
    # print(output_list(file_name, json_content_string))


def write_multi_text_from_lsj(json_content_list, out_path):
    '''
    Output one lst into different intermediate txt with different note
    :param json_content_list:
    :param out_path:
    :return:
    '''
    file_count = 0
    note_count_dict = []

    unique_list = []
    for d in json_content_list:
        if d['content_list'] not in unique_list:
            unique_list.append(d)

    for line in unique_list:
        json_content_string = filled_string(line['content_list'])
        note = line['note'].strip()
        out_string = ""

        for sentence in json_content_string:
            latin = sentence['eng'].split('<br>')[0]
            for ending in [" v3", " v2", " v1"]:
                if latin.endswith(ending):
                    latin = latin[:-len(ending)]
            print(f"{latin}")
            print(f"{sentence['contentuid']}")
            out_string += f"{latin}\n{sentence['contentuid']}\n"
        print()
        file_count += 1
        file_name = f"{file_count}.txt"
        print(note_count_dict)
        # 检查 note_count_dict 中是否存在特定的键
        item = next((item for item in note_count_dict if note in item), None)

        if item:
            # 键已存在，执行相应操作
            item[note].append(file_name)
        else:
            # 键不存在，创建新的键值对
            note_count_dict.append({note: [file_name]})

        out_string = out_string.rstrip("\n")
        target_path = f"{out_path}{file_name}"
        with open(target_path, "w", encoding="utf-8") as output_txt:
            output_txt.write(out_string)
        print(f"writing to {target_path}")

    target_path = f"{out_path}file_name_dict.json"
    with open(target_path, "w", encoding="utf-8") as output_txt:
        json.dump(note_count_dict, output_txt, ensure_ascii=False)
    print(f"writing to {target_path}")
    return target_path


def generate_file_order(out_path):
    input_path = f"{out_path}file_name_dict.json"
    with open(input_path, 'r', encoding='utf-8') as f_in:
        note_count_dict = json.load(f_in)

    keys_list = []

    for item in note_count_dict:
        for key in item.keys():
            # if "Narrative Arc Start" not in key and "stuck" in key:
            keys_list.append(key)

    target_path = f"{out_path}file_oder.txt"
    with open(target_path, "w") as file:
        for key in keys_list:
            file.write(key + "\n")
    print(keys_list)


def generate_partial_final_txt(out_path, key_word):
    out_file = f"{out_path}{key_word}.json"
    filename_dict = f"{out_path}final_order.json"

    with open(filename_dict, 'r', encoding='utf-8') as filename_f_in:
        final_order_json = json.load(filename_f_in)

    # out_list = find_dicts_with_key(job_name, final_order_json)
    out_list = find_dicts_with_value_in_list(key_word, final_order_json)

    # print(out_list)
    print(len(out_list))
    with open(out_file, "w", encoding="utf-8") as f_out:
        json.dump(out_list, f_out, ensure_ascii=False)
        print(f"writing {key_word} to {out_file}")


def rename_file(source_path, destination_path, new_name):
    suffix = 2  # Start suffix from 2
    base_name, extension = os.path.splitext(new_name)
    new_path = os.path.join(destination_path, new_name)

    while os.path.exists(new_path):
        new_name = f"{base_name}_{suffix}{extension}"
        new_path = os.path.join(destination_path, new_name)
        suffix += 1

    shutil.copy(source_path, destination_path)
    new_file_path = os.path.join(destination_path, new_name)
    os.rename(os.path.join(destination_path, os.path.basename(source_path)), new_file_path)

    return new_file_path


def remove_special_characters(file_name):
    cleaned_name = re.sub(r"[^\w\s.-]", "", file_name)
    cleaned_name = re.sub(r"\s+", "_", cleaned_name)
    # Remove <i>, </i>, <br>, and </br> tags
    cleaned_name = re.sub(r"<(/?i|br)>", "", cleaned_name)

    # Split the cleaned name into base name and extension
    base_name, *extensions = cleaned_name.rsplit(".", 1)

    # Remove any dots from the base name except the last one
    base_name = base_name.replace(".", "")
    if extensions:
        base_name += "."

    # Combine the modified base name and extension
    cleaned_name = base_name + ".".join(extensions)

    return cleaned_name


def find_dicts_with_key(string, dict_list):
    matching_dicts = []
    for dictionary in dict_list:
        for key in dictionary.keys():
            if string.lower() == key.lower() or f"{string}.".lower() == key.lower() or f"{string},".lower() == key.lower():
                matching_dicts.append(dictionary)
                break  # 跳出当前循环，继续下一个字典的遍历
    return matching_dicts


def find_dicts_with_value_in_list(input_string, dict_list):
    lowercase_dict_list = []

    for d in dict_list:
        lowercase_dict = {}
        for key, value in d.items():
            if isinstance(value, str):
                lowercase_dict[key] = value.lower()
            elif isinstance(value, list):
                lowercase_dict[key] = [v.lower() for v in value]
        lowercase_dict_list.append(lowercase_dict)

    filtered_list = []

    for d in lowercase_dict_list:
        matching_values = []
        for value in d.values():
            matching_values.extend([v for v in value if input_string.lower() in v.lower()])
        if matching_values:
            filtered_dict = {key: matching_values for key in d.keys()}
            filtered_list.append(filtered_dict)

    return filtered_list


def double_check_file_order(out_path):
    # Step 1: check if total condition matches
    all_file = f"{out_path}file_oder.txt"
    manual_order_file = f"{out_path}final_order.json"
    filename_dict = f"{out_path}file_name_dict.json"

    with open(all_file, 'r', encoding='utf-8') as all_f_in:
        lines = all_f_in.readlines()
    with open(manual_order_file, 'r', encoding='utf-8') as manual_f_in:
        final_order = json.load(manual_f_in)
    with open(filename_dict, 'r', encoding='utf-8') as filename_f_in:
        filename_dict_json = json.load(filename_f_in)

    final_order_count = 0
    for item in final_order:
        for value in item.values():
            final_order_count += len(value)

    print(
        f"No. of scenario matches=={final_order_count == len(lines)}, scenario in final={final_order_count}, scenario "
        f"from input={len(lines)}")
    if final_order_count != len(lines):
        check_dict_mismatch(final_order, filename_dict_json)

    # Step 2: check if no of files matches
    no_lines_in_final = 0
    no_lines_from_dict = 0
    final_with_count = []

    for item in final_order:
        for list_scenarios in item.values():
            for scenario in list_scenarios:
                scenario_count = 0
                for filename_dict_node in filename_dict_json:
                    if scenario in filename_dict_node:
                        for tmp_filename in filename_dict_node[scenario]:
                            txt_path = f"{out_path}{tmp_filename}"
                            with open(txt_path, 'r', encoding='utf-8') as tmp_txt:
                                current_txt = tmp_txt.readlines()
                            no_lines_in_final += len(current_txt)
                            scenario_count += len(current_txt)
                print({scenario: scenario_count})

    for item in filename_dict_json:
        for value in item.values():
            for tmp_filename in value:
                txt_path = f"{out_path}{tmp_filename}"
                with open(txt_path, 'r', encoding='utf-8') as tmp_txt:
                    current_txt = tmp_txt.readlines()
                no_lines_from_dict += len(current_txt)

    print(
        f"No. of voicefile matches=={no_lines_in_final == no_lines_from_dict}, scenario in final={no_lines_in_final}, scenario from input={no_lines_from_dict}")


def check_dict_mismatch(file1_data, file2_data):
    # 遍历文件1中的字典列表
    for file1_dict in file1_data:
        for case, subcases in file1_dict.items():
            # 检查文件1的子案例是否在文件2中有对应
            for subcase in subcases:
                found = False
                for file2_dict in file2_data:
                    if subcase in file2_dict:
                        found = True
                        break
                if not found:
                    print(f"File 1: Case {case}, Subcase {subcase} has no corresponding match in File 2")

    # 遍历文件2中的字典列表
    for file2_dict in file2_data:
        for subcase, paths in file2_dict.items():
            # 检查文件2的子案例是否在文件1中有对应
            found = False
            for file1_dict in file1_data:
                for subcases in file1_dict.values():
                    if subcase in subcases:
                        found = True
                        break
                if found:
                    break
            if not found:
                print(f"File 2: Subcase {subcase}, Path {paths} has no corresponding match in File 1")


def find_content_with_string_old(search_string):
    root = tree.getroot()

    uid_list = []

    for content in root.iter('content'):
        content_text = content.text
        if content_text and search_string.lower() in content_text.lower():
            uid = content.get('contentuid')
            uid_list.append(uid)
    return uid_list


def generate_line_srt_by_filename_old(filename, with_name, with_ch, translation_json):
    filename = filename[:-4]
    # print(filename)

    # Get the root element
    root = tree.getroot()
    root_ch = tree_ch.getroot()

    # filename = filename[:-4]
    if "_" in filename:
        charactor = filename.split('_', 1)[0]
        contentuid = filename.split('_', 1)[1]
        # print(charactor)
        # print(contentuid)
        if charactor in speaker_code:
            speaker = speaker_code[charactor]
        else:
            speaker = ""
        if charactor in speaker_code_ch:
            speaker_ch = speaker_code_ch[charactor]
        else:
            speaker_ch = ""

        content_elem = root.find(f"./content[@contentuid='{contentuid}']")
        if content_elem is not None:
            # Extract the content of the content element
            content_string = content_elem.text
            content_string = content_string.replace("<i>", "").replace("</i>", "").replace("<br>", "").replace("<b>",
                                                                                                               "").replace(
                "</b>", "")
            if speaker == "":
                result_en = f"{content_string}".strip()
            else:
                if with_name:
                    result_en = f"{speaker}: {content_string}".strip()
                else:
                    result_en = f"{content_string}".strip()

        else:
            result_en = ""

        if not with_ch:
            if translation_json != {}:
                result_ch = translation_json[result_en]
                return f"{result_ch}\n{result_en}"

            return f"{result_en}"

        content_elem_ch = root_ch.find(f"./content[@contentuid='{contentuid}']")
        if content_elem_ch is not None:
            content_string = content_elem_ch.text
            content_string = content_string.replace("<i>", "").replace("</i>", "").replace("<br>", "").replace("<b>",
                                                                                                               "").replace(
                "</b>", "")
            if speaker_ch == "":
                result_ch = f"{content_string}"
            else:
                if with_name:
                    result_ch = f"{speaker_ch}: {content_string}"
                else:
                    result_ch = f"{content_string}"
        else:
            result_ch = ""
        if result_ch == "":
            return f"{result_en}"
        else:
            return f"{result_ch}\n{result_en}"


def find_through_metafile_old(contentuid, wem_meta, lsj_path):
    # voice_meta = look_for_meta(contentuid, lsj_path)
    voice_meta = voice_meta_file_path
    matches = []

    for root, dirs, files in os.walk(voice_meta):
        for filename in files:
            # matches = []
            meta_lsj = os.path.join(root, filename)
            with open(meta_lsj, 'r', encoding='utf-8') as f_in:
                # Load the complete JSON object from the input file
                json_meta = json.load(f_in)
            for node in json_meta['save']['regions']['VoiceMetaData']['VoiceSpeakerMetaData'][0]['MapValue'][0][
                'VoiceTextMetaData']:
                if node['MapKey']['value'] == contentuid:
                    matches.append(node['MapValue'][0]['Source']['value'])
                    wem_meta[node['MapValue'][0]['Source']['value'][:-4]] = contentuid
                    # if (len(matches) == 0):
                    #     look_for_meta(contentuid, lsj_path)
                    return matches


def filter_strings_with_pattern(string_list, pattern):
    filtered_list = []

    for string in string_list:
        if re.match(pattern, string):
            filtered_list.append(string)

    return filtered_list


def look_for_meta(contentuid):
    lsj_path = rf"E:\tmp\bg3-modders-multitool\UnpackedData\Gustav\Mods\GustavDev\Story\Dialogs\Act3\EndGame\END_BrainBattle_CombatOver_Nested_WhatNext.lsj"
    with open(lsj_path, 'r', encoding='utf-8') as f_in:
        content = json.load(f_in)
        found_speaker = ""
        for node in content["save"]["regions"]["dialog"]["nodes"][0]['node']:
            line_list = []
            if "TaggedTexts" in node:
                # print(node)
                for dialog in node["TaggedTexts"]:
                    # print(dialog)
                    if "TaggedText" in dialog:
                        for tagtext in dialog['TaggedText']:
                            # print(tagtext)
                            for line in tagtext['TagTexts'][0]['TagText']:
                                if line['TagText']['handle'] == contentuid:
                                    found_speaker = node['speaker']['value']
                                    break
        # print(found_speaker)
        if found_speaker != "":
            for speaker in content["save"]["regions"]['dialog']["speakerlist"][0]['speaker']:
                # print(speaker)
                if speaker['index']['value'] == f"{found_speaker}":
                    output = f"{speaker['list']['value'].replace('-', '')}.lsf"
                    print(output)
                    return output
        else:
            print("not found")
            return None


def collect_spell_files():
    f = open(spell_gen, 'r')
    content = json.loads(f.read())
    node_list = content['save']['regions']['dialog']['nodes'][0]['node']
    json_content_list = []

    for node in node_list:
        noteContext = ""
        logicalname = ""
        line_list = []
        current_node = {}
        for line in node["TaggedTexts"][0]['TaggedText'][0]['TagTexts'][0]['TagText']:
            contentuid = line['TagText']['handle']
            line_list.append({
                "contentuid": contentuid,
            })

        if "editorData" in node:
            for data in node['editorData'][0]['data']:
                if "key" in data and "value" in data['key']:
                    if data['key']['value'] == "NodeContext":
                        noteContext = data['val']['value']
                    if data['key']['value'] == "logicalname":
                        logicalname = data['val']['value']

        current_node = {
            "content_list": line_list,
            "context": noteContext,
            "logic": logicalname
        }
        json_content_list.append(current_node)

    print(json_content_list)
    with open(spell_json, "w", encoding="utf-8") as file:
        # Write the JSON data to the file
        json.dump(json_content_list, file, ensure_ascii=False)


def print_spell():
    f = open(spell_json, 'r')
    content = json.loads(f.read())
    with open(spell_out_csv, "w", newline='') as file:
        # Write the JSON data to the file
        writer = csv.writer(file)
        headers = ["latin", "english", "label"]
        writer.writerow(headers)
        for spell in content:
            spell_text = filled_string(spell['content_list'])
            # for sentence in spell_text:
            string_without_br = spell_text[0]['eng'].replace("<br>", "")
            spell['line'] = string_without_br
            print(f"{string_without_br}")
            print(spell['context'])
            print(spell['logic'])
            # print()
            writer.writerow([f"{string_without_br}", spell['context'], spell['logic']])

    print(content)
    with open(spell_json, "w", encoding="utf-8") as file:
        # Write the JSON data to the file
        json.dump(content, file, ensure_ascii=False)


def csv_to_json(csv_file_path, json_file_path):
    encodings = ['utf-8-sig', 'gbk', 'utf-16']

    # Try different encodings until successful
    for encoding in encodings:
        try:
            with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                csv_data = csv.DictReader(csv_file)

                # Convert CSV data to JSON format
                json_data = json.dumps(list(csv_data), ensure_ascii=False, indent=4)

            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json_file.write(json_data)

            print("CSV file successfully converted to JSON.")
            return

        except UnicodeDecodeError:
            pass

    print("Unable to decode the CSV file using the available encodings.")


def content_exist(contentuid):
    # check if content id could match exists wem file
    pattern = f"*{contentuid}.wem"
    # print(f"looking for {contentuid}, pattern is {pattern}")

    for root, dirs, files in os.walk(voice_location):
        for filename in fnmatch.filter(files, pattern):
            print(f"found {filename}")
            return True
    return False


def if_content_exist(pattern, path):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, pattern):
            print(f"found {filename}")
            return filename
    return


def sort_by_number(filename):
    if "-" in filename:
        # 提取文件名中的数字部分（例如 "100-" 提取为 100）
        number = int(filename.split("-", 1)[0])
    elif "." in filename:
        number = int(filename.split(".", 1)[0])
    return number


def get_specific_line(file_path, line_number):
    with open(file_path, 'r', encoding='utf-8') as file:
        for index, line in enumerate(file, start=1):
            if index == line_number:
                return line.rstrip('\n')
    return None


def move_wav_with_txt(txt_path, wav_path, target_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        vm_cast = f.readlines()
    count = 0
    print(vm_cast)
    for i in range(0, len(vm_cast), 2):
        line2 = vm_cast[i + 1].strip()
        pattern = f"*{line2}.wav"
        # print(pattern)
        for root, dirs, files in os.walk(wav_path):
            for matched_wav in fnmatch.filter(files, pattern):
                source_wav = os.path.join(root, matched_wav)
                shutil.move(source_wav, target_path)
                print(f"moved {matched_wav} to {target_path}")
                count += 1
    print(f"moved {count} files")


def locate_specific_line(wav_filename):
    lsj_path = locate_lsj(wav_filename)
    if lsj_path is None:
        return ""
    contetnt_list = find_contentuid_within_lsj(wav_filename, lsj_path)
    return find_text_by_uid(contetnt_list)


def locate_lsj(wav_filename):
    wem_filename = f"{wav_filename[:-4]}.wem"
    return search_in_file(voice_meta_file_path, wem_filename, True)


def find_contentuid_within_lsj(wav_filename, lsj_path):
    wem_filename = f"{wav_filename[:-4]}.wem"
    value_list = []
    with open(lsj_path, 'r', encoding='utf-8') as f:
        json_meta = json.load(f)

    for metaData in json_meta['save']['regions']['VoiceMetaData']['VoiceSpeakerMetaData']:
        for mapNode in metaData['MapValue']:
            for voiceMetaNode in mapNode['VoiceTextMetaData']:
                for voiceMetaNodeValue in voiceMetaNode['MapValue']:
                    if voiceMetaNodeValue['Source']['value'] == wem_filename:
                        value_list.append(voiceMetaNode['MapKey']['value'])
    # print(value_list)
    return value_list


def find_text_by_uid(contentuid_list):
    for contentuid in contentuid_list:
        result = generate_line_srt_by_filename(f"123_{contentuid}.wav", False, True, {})
        if result != "":
            return result


def search_in_file(directory, search_string, limited):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            # if ".lsj" in filename:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if re.search(search_string, content, re.IGNORECASE):
                        print(f"Found '{search_string}' in: {file_path}")
                        file_list.append(file_path)
                        if limited:
                            return file_path
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    if limited:
        print(f'{search_string} not found in {directory}')
    return file_list


def get_speakercode_by_ch(ch):
    for key, value in speaker_code.items():
        if ch in value:
            return key
    return None


def copy_all_wem(ch_name):
    speaker = get_speakercode_by_ch(ch_name)
    if speaker is None:
        print(f" {ch_name} code not found, pls manually find it and add to const.")

    to_be_copied = []
    for filename in os.listdir(voice_location):
        if filename.startswith(speaker) and filename.endswith(".wem"):
            to_be_copied.append(filename)

    if len(to_be_copied) == 0:
        print("no matched files")
        return

    target_path = rf"{base_path}{ch_name}\wem\\"
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    for wem_filename in to_be_copied:
        source_wav = os.path.join(voice_location, wem_filename)
        copy_file = shutil.copy(source_wav, target_path)
        print(f"copied {source_wav} to {copy_file}")

    print(f"copied {len(to_be_copied)} files")


def from_srt_to_txt(srt_path, txt_path):
    out_txt = ""
    with open(srt_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

        for i in range(0, len(lines), 5):
            line1 = lines[i].strip()  # 去除行末尾的换行符和空格
            line2 = lines[i + 1].strip()
            line3 = lines[i + 2].strip()  # 去除行末尾的换行符和空格
            line4 = lines[i + 3].strip()
            out_txt += f"{line3}\n{line4}\n\n"
            print(line3)
            print(line4)

    with open(txt_path, 'w', encoding="utf-8") as out_file:
        out_file.write(out_txt)
