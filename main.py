import os
import json
import xml.etree.ElementTree as ET
import fnmatch
import shutil
from pydub import AudioSegment
import pysrt

pb_script_location1 = "\\Data\\Input\\PB_script\\companion_location"
pb_script_location2 = "\\Data\\Input\\PB_script\\companions"
pb_script_needed = "\\Data\\Input\\PB_script\\needed"
pb_script_final = "\\Data\\Input\\PB_script\\final"

voice_meta_location = "Input\\VoiceMeta"
voice_location = "E:\\tmp\\bg3-modders-multitool\\UnpackedData\\Voice\\Mods\\Gustav\\Localization\\English\\Soundbanks"

tmp_voice_location = "\\Data\\Output\\tmp_wem"
output_dialog = "\\Data\\Output\\dialogs_final.txt"
output_content_json = "\\Data\\Output\\final.json"
output_audio_path = "\\Data\\Output\\result.wav"
output_srt_path = "\\Data\\Output\\result.srt"

output_voice_location = "\\Data\\Output\\wav"
dialog_srt_location = "\\Data\\Output\\srt"
output_voice_order_list = "\\Data\\Output\\file_list.json"
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
    "0de603c5-42e2-4811-9dad-f652de080eba": "Minsc",
    "73d49dc5-8b8b-45dc-a98c-927bb4e3169b": "Emporer"
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
    "0de603c5-42e2-4811-9dad-f652de080eba": "明斯克",
    "73d49dc5-8b8b-45dc-a98c-927bb4e3169b": "君主"
}  # LSString


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
    output_dialog_list = []
    for file_name in file_name_list:
        sentence_list = []
        # file_name = "PB_Minthara_PAD_GortashCeremony.lsj"
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

        sentence_list.append(filtered_data)
        # print(output_list(file_name, json_content_string))
        f.close()
        dialog_json = {
            "title": file_name[3:-4],
            "dialog": sentence_list[0]
        }
        output_dialog_list.append(dialog_json)
    output_json = {
        "pb": output_dialog_list
    }

    output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_dialog}"
    file = open(output_path, "w")
    file.write(output_string)
    file.close()

    output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_content_json}"
    with open(output_path, "w", encoding="utf-8") as file:
        # Write the JSON data to the file
        json.dump(output_json, file, ensure_ascii=False)


def generate_output_list(file_name, content_string):
    # print(content_string)
    content_ch = ""
    for item in content_string:
        if "ch" in item:
            content_ch += str(item["ch"]) + "\n"
        else:
            content_ch += str(item["eng"]) + "\n"
    # content_ch = [str(item["ch"]) for item in content_string]

    # Join the values with a newline character separator
    # dialog = "\n".join(content_ch)
    result = file_name[3:-4] + "\n" + content_ch + "\n" + "\n"
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
            if content_elem is not None:
                # Extract the content of the content element
                content_string = content_elem.text
                content['eng'] = f"{content['speaker']['speaker_name']}: {content_string}"
            else:
                content['eng'] = ""

            content_elem_ch = root_ch.find(f"./content[@contentuid='{content['contentuid']}']")
            if content_elem_ch is not None:
                # Extract the content of the content element
                content_string = content_elem_ch.text
                content['ch'] = f"{content['speaker']['speaker_name_ch']}: {content_string}"
            else:
                content['ch'] = ""
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
        if "TaggedText" in node_json["TaggedTexts"][0]:
            contentuid = node_json["TaggedTexts"][0]['TaggedText'][0]['TagTexts'][0]['TagText'][0]['TagText']['handle']
        else:
            contentuid = ""
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


def get_speaker_name(input_json, speaker_list):
    for speaker in speaker_list:
        if speaker['index'] == input_json['value']:
            return {
                "speaker_name": speaker['name'],
                "speaker_name_ch": speaker['ch_name']
            }


def output_wav_subtitle():
    """
    concatenate audios and generate subtitle
    :return:
    """
    full_file_name = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_content_json}"
    with open(full_file_name, 'r', encoding='utf-8') as f:
        json_content = json.loads(f.read())
        # wem_file_list = list_wem_filename(json_content)
        # print(wem_file_list)
        generate_wav(json_content)


def generate_wav(content_json):
    for dialog in content_json['pb']:
        skip_current_dialog = False

        # Initialize the output audio and subtitle variables
        output_audio = AudioSegment.empty()

        subs = pysrt.SubRipFile()
        # Initialize a time counter
        current_time = 0
        # Initialize an empty subtitle list to store the generated subtitles
        subtitles = pysrt.SubRipFile()
        order = 1

        for sentence in dialog['dialog']:
            if "wem_location" in sentence:
                # print(sentence['wem_location'])
                wem_path = sentence['wem_location']
                wav_path = f"{wem_path[:-4]}.wav"
                # wem_to_wav(wem_path, wav_path)
                audio_segment = AudioSegment.from_file(wav_path, format='wav')
                # Load the audio file
                output_audio += audio_segment + AudioSegment.silent(duration=500)

                # Calculate the duration of the audio clip in milliseconds
                duration = len(audio_segment)

                # Create a new subtitle item
                subtitle_item = pysrt.SubRipItem()

                # Set the start time for the subtitle item based on the current time
                subtitle_item.start = pysrt.SubRipTime(milliseconds=current_time)
                # Calculate the end time by adding the duration to the start time
                subtitle_item.end = subtitle_item.start + pysrt.SubRipTime(milliseconds=duration)
                subtitle_item.index = order
                # Set the text of the subtitle item
                subtitle_item.text = f"{sentence['ch']}\n{sentence['eng']}"

                # Append the subtitle item to the subtitles list
                subtitles.append(subtitle_item)

                # Update the current time counter
                current_time += duration + 500
                order += 1

                # subtitle_item.text = f"{sentence['ch']}\n{sentence['eng']}"

            else:
                skip_current_dialog = True
                break

        if skip_current_dialog:
            print(f"skip the dialog of {dialog['title']}")

            continue

        # Export the concatenated audio to a .wav file
        wav_destintion = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_location}\\{dialog['title']}.wav"
        output_audio.export(wav_destintion, format="wav")
        print(f"saved wav: {wav_destintion}")
        srt_destination = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_location}\\{dialog['title']}.srt"
        subtitles.save(srt_destination)
        print(f"saved srt: {srt_destination}")


def wem_to_wav(source_path, target_path):
    """
    manual conversion using vgmstream plugin
    :param source_path:
    :param target_path:
    :return:
    """
    pass


def list_wem_filename(content_json):
    wem_list = []
    for dialog in content_json['pb']:
        for sentence in dialog['dialog']:
            pattern = f"*{sentence['contentuid']}.wem"
            for root, dirs, files in os.walk(voice_location):
                for filename in fnmatch.filter(files, pattern):
                    # If the filename matches the pattern, print the full path of the file
                    print(os.path.join(root, filename))
                    wanted_file = os.path.join(root, filename)
                    destination_directory = f"{os.path.dirname(os.path.abspath(__file__))}\\{tmp_voice_location}"
                    copied_path = shutil.copy(wanted_file, destination_directory)
                    wem_list.append(copied_path)
                    sentence['wem_location'] = copied_path

    output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_content_json}"
    with open(output_path, "w", encoding="utf-8") as file:
        # Write the JSON data to the file
        json.dump(content_json, file, ensure_ascii=False)
    return wem_list


def generated_combined_audio():
    # generate_file_order()
    directory = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_order_list}"
    # Load the contents of the JSON file
    with open(directory, 'r') as file:
        file_list = json.load(file)

    output_audio = AudioSegment.empty()

    # Initialize an empty list to store the subtitles
    subtitles = []

    time_gap = 5000

    for file in file_list:
        wav_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_location}\\{file}"
        audio_segment = AudioSegment.from_file(wav_path, format='wav')
        # Load the audio file
        output_audio += audio_segment + AudioSegment.silent(duration=time_gap)
        #
        # # Calculate the duration of the audio clip in milliseconds
        # duration = len(audio_segment)
        # # Define the delay duration in milliseconds (e.g. 5 minutes = 300000 milliseconds)
        # delay_duration = pysrt.SubRipTime(milliseconds=time_gap)
        #
        # subtitle_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{dialog_srt_location}\\{file[:-4]}.srt"
        # # Open the subtitle file using pysrt
        # subtitle = pysrt.open(subtitle_path)
        #
        # # Iterate over each subtitle item and delay the start and end times
        # for item in subtitle:
        #     item.start =  pysrt.SubRipTime(milliseconds=item.start + duration)
        #     item.end += delay_duration
        #
        # # Append the subtitles to the list
        # subtitles.append(subtitle)

    # Export the concatenated audio to a .wav file
    wav_destintion = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_audio_path}"
    output_audio.export(wav_destintion, format="wav")
    print(f"saved wav: {wav_destintion}")

    # Calculate the total duration of the subtitles and the time to insert between them
    # total_duration = sum([(subtitle[-1].end.ordinal - subtitle[0].start.ordinal) / 1000 + (
    #         subtitle[0].start.hours * 3600) + (subtitle[0].start.minutes * 60) + subtitle[0].start.seconds for
    #                       subtitle in subtitles]) + (len(subtitles) - 1) * time_gap
    #
    # # Initialize an empty subtitle list to store the concatenated subtitles
    # concatenated_subtitle = pysrt.SubRipFile()

    # Concatenate the subtitles and adjust timestamps
    # current_time = 0  # Initialize the current time counter in seconds
    #
    # for i, subtitle in enumerate(subtitles):
    #     # Shift the subtitle timestamps
    #     subtitle.shift(seconds=current_time)
    #
    #     # Append the adjusted subtitle to the concatenated subtitle list
    #     concatenated_subtitle.extend(subtitle)
    #
    #     if i < len(subtitles) - 1:
    #         # Add a time gap between subtitle files
    #         current_time += time_gap
    #
    #     # Calculate the duration of the current subtitle
    #     start_time = subtitle[0].start
    #     end_time = subtitle[-1].end
    #     subtitle_duration = (end_time.ordinal - start_time.ordinal) / 1000 + (start_time.hours * 3600) + (
    #             start_time.minutes * 60) + start_time.seconds
    #
    #     # Update the current time counter
    #     current_time += subtitle_duration
    # # Save the final concatenated subtitle to a file
    # final_output_srt_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_srt_path}"
    # concatenated_subtitle.save(final_output_srt_path, encoding='utf-8')
    # print(f"saved srt: {final_output_srt_path}")


def generate_file_order():
    # Specify the directory path
    directory = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_location}"

    # Get the list of files in the directory
    file_list = os.listdir(directory)
    import random
    # Randomize the order of the file list
    random.shuffle(file_list)

    # Write the file list to a JSON file
    output_file_path = 'file_list.json'
    with open(output_file_path, 'w') as output_file:
        json.dump(file_list, output_file)


def generate_banter_files():
    # generate_script()
    # output_wav_subtitle()
    generated_combined_audio()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    generate_banter_files()
