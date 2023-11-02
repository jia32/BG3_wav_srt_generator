from constant import death
import json
from utils import get_speaker_list, generate_new_node, filled_string, generate_output_list


def generate_other_script(filename):
    '''
    根据lsj文件，打印文本内容
    （功能不完善，可以直接使用html的文件进行对比，已废弃）
    :return:
    '''
    # Get the directory path of the current file
    output_string = ""
    output_json = {}
    sentence_list = []
    f = open(filename, 'r')
    content = json.loads(f.read())
    # generate content json

    json_content_list = []
    nodes_map = {}
    root_node = None
    speaker_list = get_speaker_list(content["save"]["regions"]["dialog"]["speakerlist"][0]['speaker'])
    # print(len(ori_json["save"]["regions"]["dialog"]["nodes"][0]['node']))

    for node in content["save"]["regions"]["dialog"]["nodes"][0]['node']:
        json_content_list.append(generate_new_node(node, speaker_list))
    # print(nodes_map)

    for node in content["save"]["regions"]["dialog"]["nodes"][0]['node']:
        if "Root" in node and node["Root"]['value'] is True:
            json_content_list.append(generate_new_node(node, speaker_list))
            break

    # Remove dictionaries with "contentuid" equal to ""
    filtered_data = [item for item in json_content_list if item["contentuid"] != ""]

    # print(filtered_data)

    # filled in with real content
    json_content_string = filled_string(filtered_data)

    output_string += generate_output_list("HAG_HagLair_EntranceDouble.lsj", json_content_string)

    # print(output_list(file_name, json_content_string))
    f.close()

    print(output_string)
