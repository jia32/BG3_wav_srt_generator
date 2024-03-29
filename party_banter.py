from utils import output_dialog_txt_file, output_json_file, generate_output_list, render_json, filled_string
from constant import pb_script_needed, tmp_content_json, voice_location, tmp_voice_location, \
    output_voice_order_list, final_content_json, output_audio_path, output_srt_path
import json
import os
import shutil
import fnmatch
from pydub import AudioSegment
import pysrt


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

    output_dialog_txt_file(output_string)
    output_json_file(output_json)


def output_dialog_order(step):
    """
    concatenate audios and generate subtitle
    :return:
    """
    full_file_name = f"{os.path.dirname(os.path.abspath(__file__))}\\{tmp_content_json}"
    print(full_file_name)
    with open(full_file_name, 'r', encoding='utf-8') as f:
        json_content = json.loads(f.read())
        if step == 1:
            wem_file_list = list_wem_filename(json_content)
            print(wem_file_list)
        elif step == 2:
            random_order(json_content)
        # 这一步可以手动调整前后顺序
        elif step == 3:
            generate_final_json(json_content)
        elif step == 4:
            print_dialog_output(json_content)
        elif step == 5:
            compare_dialog()


def compare_dialog():
    file_list_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_order_list}"
    with open(file_list_path, "r", encoding="utf-8") as file:
        file_list = json.load(file)
    current_list = [
        "Shadowheart_Gale_Refugees",
        "Wyll_Astarion_WyrmsRock",
        "Wyll_Jaheira_BasiliskGate",
        "Laezel_Wyll_FlamingFist",
        "Gale_Astarion_Tabernacle",
        "Gale_Wyll_BaldursMouth",
        "Karlach_Shadowheart_BaldursMouth",
        "Minthara_Shadowheart_FelogyrsFireworks",
        "Halsin_Karlach_SorcerousSundries",
        "Minthara_Shadowheart_SorcerousSundries",
        "Gale_Karlach_SorcerousSundries",
        "Minsc_Wyll_Bonecloaks",
        "Karlach_Laezel_HouseOfHope",
        "Shadowheart_Gale_BlushingMermaid",
        "Halsin_Karlach_BlushingMermaid",
        "Astarion_Laezel_BlushingMermaid",
        "Minthara_Astarion_CazadorsPalace",
        "Minsc_Jaheira_CazadorsPalace",
        "Gale_Laezel_CazadorsPalace",
        "Minsc_Karlach_UndercityRuins",
        "Wyll_Jaheira_UndercityRuins",
        "Minsc_Jaheira_GeneralSewers",
        "Astarion_Gale_GeneralSewers",
        "Gale_Jaheira_BhaalTemple",
        "Astarion_Laezel_BhaalTemple",
        "Karlach_Minsc_BhaalTemple",
        "Shadowheart_Wyll_BhaalTemple",
        "Halsin_Laezel_CountingHouse",
        "Karlach_Wyll_CountingHouse",
        "Karlach_Wyll_NorthAlleys",
        "Wyll_Jaheira_GuildhallEntrance",
        "Laezel_Minthara_Guildhall",
        "Jaheira_Minsc_Guildhall",
        "Astarion_Shadowheart_Guildhall",
        "Wyll_Gale_Guildhall",
        "Laezel_Wyll_Dangers",
        "Wyll_Karlach_SouthDocks",
        "Karlach_Shadowheart_BloombridgePark",
        "Astarion_Wyll_BloomridgePark",
        "Karlach_Jaheira_WaterqueensHouse",
        "Laezel_Karlach_OskarsBeloved",
        "Astarion_Jaheira_OskarsBeloved",
        "Laezel_Gale_BloomridgePark",
        "Minsc_Jaheira_BloomridgePark",
        "Gale_Shadowheart_SteelWatch",
        "Minthara_Wyll_ROM_Act3_001",
        "Minthara_Wyll_ROM_Act3_002",
        "Astarion_Wyll_ROM_Act3",
        "Minsc_Wyll_ROM_Act3",
        "Wyll_Minthara_ROM_Act3_001",
        "Astarion_Minthara_ROM_Act3",
        "Gale_Minthara_ROM_Act3",
        "Minthara_Astarion_ROM_Act3",
        "Wyll_Astarion_ROM_Act3_001",
        "Halsin_Astarion_ROM_Act3_Spawn",
        "Minthara_Astarion_ROM_Act3_001",
        "Gale_Astarion_ROM_Act3_Ascendant",
        "Astarion_Karlach_ROM_Act3",
        "Minthara_Karlach_ROM_Act3_002",
        "Gale_Karlach_ROM_Act3",
        "Wyll_Karlach_ROM_Act3_001",
        "Minthara_Laezel_ROM_Act3",
        "Minthara_Laezel_ROM_Act3_001",
        "Gale_Laezel_ROM_Act3",
        "Wyll_Shadowheart_ROM_Act3_001",
        "Minthara_Shadowheart_ROM_Act3_002",
        "Gale_Shadowheart_ROM_Act3_Shar",
        "Wyll_Gale_ROM_Act3_001",
        "Wyll_Minsc_MorphicPool",
        "Shadowheart_Gale_MorphicPool",
        "Gale_Wyll_MorphicPool",
        "Halsin_Karlach_MorphicPool",
        "Jaheira_Shadowheart_MorphicPool",
        "Karlach_Shadowheart_MorphicPool",
        "Laezel_Shadowheart_MorphicPool",
        "Minsc_Karlach_MorphicPool",
        "Minthara_Laezel_MorphicPool"
    ]

    # 使用列表推导式找出list1中存在而list2中不存在的元素
    not_in_list2 = [x for x in file_list if x not in current_list]

    # 打印结果
    print(not_in_list2)
    print(len(not_in_list2))
    not_in_list = f"{os.path.dirname(os.path.abspath(__file__))}\\Data\\Output\\all\\Act3\\need_to_check.json"
    with open(not_in_list, 'w') as output_file:
        json.dump(not_in_list2, output_file)


def print_dialog_output(json_content):
    # file_list_path = f"{os.path.dirname(os.path.abspath(__file__))}\\Data\\Output\\all\\Act3\\need_to_check.json"

    file_list_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_order_list}"
    with open(file_list_path, "r", encoding="utf-8") as file:
        file_list = json.load(file)
    # print(json_content)
    for title in file_list:
        for dialog in json_content['pb']:
            if dialog['title'] == title:
                print(title)
                for sentence in dialog['dialog']:
                    # if "wem_location" in sentence:
                    print(f"{sentence['ch']}\n{sentence['eng']}".replace("<i>", "").replace("</i>", ""))
                print()


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

    output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{tmp_content_json}"
    with open(output_path, "w", encoding="utf-8") as file:
        # Write the JSON data to the file
        json.dump(content_json, file, ensure_ascii=False)
    return wem_list


def random_order(json_content):
    import random
    # random.shuffle(json_content['pb'])
    file_list = []
    output_string = ""
    for item in json_content['pb']:
        file_list.append(item['title'])
        output_string += generate_output_list(f"123{item['title']}1234", item['dialog'])

    output_file_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_order_list}"
    print(f"write to {output_file_path}")
    with open(output_file_path, 'w') as output_file:
        json.dump(file_list, output_file)

    output_dialog_txt_file(output_string)


def generate_final_json(json_content):
    directory = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_voice_order_list}"
    # Load the contents of the JSON file
    with open(directory, 'r') as file:
        file_list = json.load(file)

    dialog_list = []
    for file in file_list:
        for dialog in json_content['pb']:
            if file == dialog['title']:
                print(dialog)
                dialog_list.append(dialog)
    final_json = {"pb": dialog_list}

    output_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{final_content_json}"
    with open(output_path, "w", encoding="utf-8") as file:
        # Write the JSON data to the file
        json.dump(final_json, file, ensure_ascii=False)


def combine_audio_sub():
    full_file_name = f"{os.path.dirname(os.path.abspath(__file__))}\\{final_content_json}"
    with open(full_file_name, 'r', encoding='utf-8') as f:
        content_json = json.loads(f.read())

    start_time = 100
    time_gap = 1000
    inbetween = 600
    output_audio = AudioSegment.silent(duration=start_time)

    current_time = start_time
    order = 1
    subtitles = pysrt.SubRipFile()

    for dialog in content_json['pb']:
        skip_current_dialog = False
        for sentence in dialog['dialog']:
            if "wem_location" in sentence:
                wem_path = sentence['wem_location']
                wav_path = f"{wem_path[:-4]}.wav"
                # wem_to_wav(wem_path, wav_path)
                audio_segment = AudioSegment.from_file(wav_path, format='wav')
                # Load the audio file
                output_audio += audio_segment + AudioSegment.silent(duration=inbetween)

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
                subtitle_item.text = f"{sentence['ch']}\n{sentence['eng']}" \
                    .replace("<i>", "").replace("</i>", "") \
                    .replace("<br>", "").replace("</br>", "")

                # Append the subtitle item to the subtitles list
                subtitles.append(subtitle_item)

                # Update the current time counter
                current_time += duration + inbetween
                order += 1
                print(current_time)
                # subtitle_item.text = f"{sentence['ch']}\n{sentence['eng']}"

            else:
                skip_current_dialog = True
                break
        # Load the audio file
        output_audio += AudioSegment.silent(duration=time_gap)
        current_time += time_gap

        if skip_current_dialog:
            print(f"skip the dialog of {dialog['title']}")
            continue

    # Export the concatenated audio to a .wav file
    wav_destintion = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_audio_path}"
    output_audio.export(wav_destintion, format="wav")
    print(f"saved wav: {wav_destintion}")
    srt_destination = f"{os.path.dirname(os.path.abspath(__file__))}\\{output_srt_path}"
    subtitles.save(srt_destination)
    print(f"saved srt: {srt_destination}")
