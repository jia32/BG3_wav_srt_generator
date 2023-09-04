import os
import json
import xml.etree.ElementTree as ET

pb_script_location1 = "\\Data\\Input\\PB_script\\companion_location"
pb_script_location2 = "\\Data\\Input\\PB_script\\companions"
pb_script_needed = "\\Data\\Input\\PB_script\\needed"

voice_meta_location = "Input\\VoiceMeta"
voice_location = "E:\\tmp\\bg3-modders-multitool\\UnpackedData\\Voice\\Mods\\Gustav\\Localization\\English\\Soundbanks"

output_dialog = "\\Data\\Output\\dialogs_2.txt"
output_content_json = "\\Data\\Output\\needed.json"
speaker_name = {
    "ad9af97d-75da-406a-ae13-7071c563f604": "Gale",
    "58a69333-40bf-8358-1d17-fff240d7fb12": "Laezel",
    "c774d764-4a17-48dc-b470-32ace9ce447d": "Wyll",
    "c7c13742-bacd-460a-8f65-f864fe41f255": "Astarion",
    "3ed74f06-3c60-42dc-83f6-f034cb47c679": "Shadowheart",
    "7628bc0e-52b8-42a7-856a-13a6fd413323": "Halsin",
    "25721313-0c15-4935-8176-9f134385451b": "Minthara",
    "91b6b200-7d00-4d62-8dc9-99e8339dfa1a": "Jaheira",
    "2c76687d-93a2-477b-8b18-8a14b549304c": "Karlach",
    "0de603c5-42e2-4811-9dad-f652de080eba": "Minsc"
}  # LSString

speaker_name_ch = {
    "ad9af97d-75da-406a-ae13-7071c563f604": "盖尔",
    "58a69333-40bf-8358-1d17-fff240d7fb12": "莱埃泽尔",
    "c774d764-4a17-48dc-b470-32ace9ce447d": "威尔",
    "c7c13742-bacd-460a-8f65-f864fe41f255": "阿斯代伦",
    "3ed74f06-3c60-42dc-83f6-f034cb47c679": "影心",
    "7628bc0e-52b8-42a7-856a-13a6fd413323": "哈尔辛",
    "25721313-0c15-4935-8176-9f134385451b": "明萨拉",
    "91b6b200-7d00-4d62-8dc9-99e8339dfa1a": "贾希拉",
    "2c76687d-93a2-477b-8b18-8a14b549304c": "卡菈克",
    "0de603c5-42e2-4811-9dad-f652de080eba": "明斯克"
}  # LSString


def init_directory():
    """
    create a folder for each banter
    :return: list of banter name
    """
    pass


def generate_script():
    """
    create script for each banter, include content uid, .wem file name, uuid, children node info, speaker
    :return:
    """
    # Get the directory path of the current file
    current_directory = f"{os.path.dirname(os.path.abspath(__file__))}\\{pb_script_needed}"
    file_name_list = os.listdir(current_directory)
    output_string = ""
    output_json = {}
    output_list = []
    for file_name in file_name_list:
        # file_name = "PB_Astarion_Laezel_Sunlight.lsj"
        full_file_name = f"{current_directory}\\{file_name}"
        f = open(full_file_name, 'r')
        content = json.loads(f.read())
        # generate content json
        json_content_list = render_json(content)
        # print(json_content_list)

        # Remove dictionaries with "contentuid" equal to ""
        filtered_data = [item for item in json_content_list if item["contentuid"] != ""]

        # print(filtered_data)

        # filled in with real content
        json_content_string = filled_string(filtered_data)

        output_string += generate_output_list(file_name, json_content_string)
        output_list.append(filtered_data)
        # print(output_list(file_name, json_content_string))
        f.close()
    # printq(content)
    output_json = {
        "pb": output_list
    }

    # output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_dialog}"
    # file = open(output_path, "w")
    # file.write(output_string)
    # file.close()

    output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_content_json}"
    with open(output_path, "w", encoding="utf-8") as file:
        # Write the JSON data to the file
        json.dump(output_json, file, ensure_ascii=False)


def generate_output_list(file_name, content_string):
    # Extract the values of the "taste" key from each dictionary
    content_ch = [str(item["ch"]) for item in content_string]

    # Join the values with a newline character separator
    dialog = "\n".join(content_ch)
    result = file_name[3:-4] + "\n" + dialog + "\n" + "\n"
    print(result)
    return result


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
            # Extract the content of the content element
            content_string = content_elem.text
            content['eng'] = f"{content['speaker']['speaker_name']}: {content_string}"

            content_elem_ch = root_ch.find(f"./content[@contentuid='{content['contentuid']}']")
            # Extract the content of the content element
            content_string = content_elem_ch.text
            content['ch'] = f"{content['speaker']['speaker_name_ch']}: {content_string}"

        # Print the content
    # print(content_list)
    return content_list


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


def generate_new_node(node_json, speaker_list):
    # print(node_json)
    if "TaggedTexts" in node_json:
        contentuid = node_json["TaggedTexts"][0]['TaggedText'][0]['TagTexts'][0]['TagText'][0]['TagText']['handle']
    else:
        contentuid = ""

    new_node = {
        "UUID": node_json["UUID"]['value'],
        "speaker": get_speaker_name(node_json["speaker"], speaker_list),
        "contentuid": contentuid,
        "children": node_json['children']
    }
    return new_node


def get_speaker_list(speaker_list):
    result = []
    for speaker in speaker_list:
        out_speaker = {
            "index": int(speaker['index']['value']),
            "name": speaker_name[speaker['list']['value']],
            "ch_name": speaker_name_ch[speaker['list']['value']]
        }
        result.append(out_speaker)
    return result


def get_speaker_name(input_json, speaker_list):
    for speaker in speaker_list:
        if speaker['index'] == input_json['value']:
            return {
                "speaker_name": speaker['name'],
                "speaker_name_ch": speaker['ch_name']
            }


def copy_wem():
    """
    copy .wem file into its banter directory
    :return:
    """
    pass


def output_wav_subtitle():
    """
    concatenate audios and generate subtitle
    :return:
    """
    pass


def generate_banter_files():
    init_directory()
    generate_script()
    copy_wem()
    output_wav_subtitle()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    generate_banter_files()
