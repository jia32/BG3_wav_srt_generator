import os
import json
import xml.etree.ElementTree as ET
import re
import csv
import fnmatch
import shutil
from constant import speaker_name, speaker_name_ch, output_dialog, tmp_content_json, speaker_code, speaker_code_ch, \
    spell_gen, spell_json, spell_out_csv, voice_location


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
    file_name = "/Data/Input/english_content.xml"
    file_name_ch = "/Data/Input/chinese_content.xml"
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


def load_text_from_lsj(content):
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
        # print(f"{other_value}")
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


def generate_line_srt_by_filename(filename):
    minsc_ch = {}
    filename = filename[:-4]
    # print(filename)
    # Parse the XML string to a tree structure
    file_name = "/Data/Input/english_content.xml"
    file_name_ch = "/Data/Input/chinese_content.xml"
    # Get the directory path of the current file
    xml_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{file_name}"
    xml_path_ch = f"{os.path.dirname(os.path.abspath(__file__))}\\{file_name_ch}"

    # Parse the XML file
    tree = ET.parse(xml_path)
    tree_ch = ET.parse(xml_path_ch)

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
                result_en = f"{content_string}"
            else:
                result_en = f"{speaker}: {content_string}"
                result_en = f"{content_string}"

        else:
            result_en = ""

        content_elem_ch = root_ch.find(f"./content[@contentuid='{contentuid}']")
        if content_elem_ch is not None:
            content_string = content_elem_ch.text
            content_string = content_string.replace("<i>", "").replace("</i>", "").replace("<br>", "").replace("<b>",
                                                                                                               "").replace(
                "</b>", "")
            if speaker_ch == "":
                result_ch = f"{content_string}"
            else:
                result_ch = f"{speaker_ch}: {content_string}"
                result_ch = f"{content_string}"
        else:
            result_ch = ""
        if result_en in minsc_ch:
            result_ch = minsc_ch[result_en]
        if result_ch == "":
            return f"{result_en}"
        else:
            return f"{result_ch}\n{result_en}"


def find_through_metafile(contentuid, wem_meta):
    ###
    # TODO: need to refine logic for meta file in order to locate all the voice with text
    ###
    voice_meta = look_for_meta(contentuid)
    voice_meta = rf"E:\tmp\converted\voiceMeta"
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
                    #     look_for_meta(contentuid)
                    return matches


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


def content_exist(contentuid):
    # check if content id could match exists wem file
    pattern = f"*{contentuid}.wem"
    # print(f"looking for {contentuid}, pattern is {pattern}")

    for root, dirs, files in os.walk(voice_location):
        for filename in fnmatch.filter(files, pattern):
            print(f"found {filename}")
            return True
    return False


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
