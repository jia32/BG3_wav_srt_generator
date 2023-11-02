import json
import os
import shutil
import fnmatch
from pydub import AudioSegment
import pysrt
import random

from utils import load_text_from_lsj, print_text_from_lsj, generate_line_srt_by_filename, find_through_metafile
from constant import karlach_wem, karlach_tmp, karlach_directory, karlach_wav, voice_location, speaker_code, \
    speaker_code_ch

'''
@Project:        BG3 voice generator
@File:           in_world_voice.py
@Author:         Jasmine
@Description：   用来读取及生成点击地图时，角色发出的语音/对话。这部分内容很多，所以需要手工挑选。
                 使用txt中间文件来，选取需要生成的音频及字幕
                 支持多个lsj文件-一组lsj文件生成一个音频
'''


def create_dialog_txt(script_location, filename):
    '''
    根据lsj文件，生成txt中间文件(txt, contentuid)

    :param script_location:
    :param filename:
    :return:
    '''
    # for destination in portal_list:
    out_string = ""
    # lsj_script = back_to_camp
    # for root, dirs, files in os.walk(script_location):
    #     for filename in files:
    # current_path = os.path.join(root, filename)

    sommon_f = open(f"{script_location}{filename}", 'r', encoding='utf-8')
    sommon_content = json.loads(sommon_f.read())
    # print(sommon_content)
    sommon_json_content_list = load_text_from_lsj(sommon_content)
    # print(sommon_content)
    out_string += print_text_from_lsj(sommon_json_content_list, filename[:-4])
    sommon_f.close()

    # if value is not None:
    #     response_f = open(response_script, 'r', encoding='utf-8')
    #     response_content = json.loads(response_f.read())
    #     response_json_content_list = load_text_from_lsj(response_content)
    #     out_string += print_text_from_lsj(response_json_content_list, f"response of {value}")
    #     response_f.close()
    target_location = f"{script_location}{filename[:-4]}.txt"
    if not os.path.exists(karlach_directory):
        os.makedirs(karlach_directory)
    out_string = out_string.rstrip("\n")
    with open(target_location, "w", encoding="utf-8") as output_txt:
        output_txt.write(out_string)


def print_dialog_txt():
    with open(karlach_tmp, "r", encoding="utf-8") as file:
        lines = file.readlines()

        for i in range(0, len(lines), 2):
            line1 = lines[i].strip()  # 去除行末尾的换行符和空格
            line2 = lines[i + 1].strip()
            line2 = f"000_{line2}.wem"
            specific_line = generate_line_srt_by_filename(line2)
            print(specific_line)


def copy_audio_wem(script_txt, current_target_path):
    '''
    根据中间文件txt，将需要的wem文件copy到工作目录下
    :param target_folder:
    :param script_txt:
    :param current_target_path:
    :return:
    '''
    count = 0
    # summon_ch_dict = {"Vampire": "Astarion"}
    # for destination in portal_list:
    # script_txt = f"{karlach_directory}back.txt"
    if not os.path.exists(current_target_path):
        os.makedirs(current_target_path)
        print(f"created {current_target_path}")
    print(f"open {script_txt}")
    wem_meta = {}
    with open(script_txt, 'r') as file:
        lines = file.readlines()
        lines_to_keep = []

        for i in range(0, len(lines), 2):
            line1 = lines[i].strip()  # 去除行末尾的换行符和空格
            line2 = lines[i + 1].strip()
            matches = []

            print(line2)
            if "_" in line2:
                pattern = f"{line2}.wem*"
            else:
                pattern = f"*{line2}.wem"
            # if "heart" in line1:
            count += 1

            for root, dirs, files in os.walk(voice_location):
                for filename in fnmatch.filter(files, pattern):
                    matches.append(filename)

            if matches is not None and len(matches) == 0:
                # print(f"try another method")
                matches = find_through_metafile(line2, wem_meta)
                # print(len(matches))
                if matches is not None and len(matches) == 0:
                    print(f"{line2} not found in meta")
                else:
                    print(f"{line2} found in meta")
                # print(line1)
                # print(line2)
                # continue
            elif len(matches) > 1:
                print(f"{pattern} have more then 1 matches")
                # randomly choose one match to replace line2
                random_match = random.choice(matches)
                new_line2 = random_match.replace(".wem", "").split("\\")[-1]  # extract the filename without .wem
                line2 = new_line2

            # append the lines to keep
            lines_to_keep.extend([line1, line2])
            if matches is not None:

                for match in matches:
                    # line1 = line1.replace("*", "")
                    print(match)

                    # new_name = re.sub(r'[\\:*?"<>|]', '', new_name)
                    new_name = f"{karlach_wem}{i}.wem"

                    if os.path.exists(new_name):
                        # Extract the file extension
                        base_name, extension = os.path.splitext(new_name)

                        # Initialize a counter
                        # counter = 1

                        # Keep incrementing the counter until a unique name is found
                        # while os.path.exists(f"{base_name}_{counter}{extension}"):
                        #     counter += 1

                        # Append the counter to the file name
                        # new_name = f"{base_name}_{counter}{extension}"

                    wanted_file = os.path.join(root, match)
                    destination_directory = current_target_path

                    try:
                        print()
                        copied_path = shutil.copy(wanted_file, destination_directory)
                        print(f"{copied_path} is copied")
                        # if os.path.exists(rf"{karlach_wem}{match}"):
                        #     os.rename(rf"{karlach_wem}{match}", new_name)
                        #     print(f"renamed from {match} to {new_name}")
                    except FileNotFoundError:
                        print(f"文件不存在，跳过: {wanted_file}")
    print(wem_meta)
    print(lines_to_keep)
    with open(script_txt, 'w') as file:
        file.write('\n'.join(lines_to_keep))
    print(f"copied {count} files")


def generate_full_audio_srt_by_file(script_path, script_txt, wav_path, job_name):
    '''
    根据中间文件txt，生成字幕及音频
    :param script_path:
    :param wav_path:
    :return:
    '''
    wem_meta = {}

    time_gap = 600
    output_audio = AudioSegment.silent(duration=time_gap)
    current_time = time_gap
    subtitles = pysrt.SubRipFile()
    order = 1
    count = 0

    # for key in portal_list:
    # script_txt = karlach_tmp
    # wav_path = karlach_wav
    output_audio = AudioSegment.silent(duration=time_gap)
    current_time = time_gap
    subtitles = pysrt.SubRipFile()
    order = 1
    count = 0

    with open(script_txt, 'r') as file:
        lines = file.readlines()
    even_lines = list(set(lines[1::2]))
    # print(even_lines)
    for i in range(0, len(even_lines)):
        # for i in range(0, len(lines), 2):
        matches = []

        # line1 = lines[i].strip()  # 去除行末尾的换行符和空格
        line2 = even_lines[i].strip()
        # print(line1)
        # if "_" in line2:
        #     pattern = f"{line2}.wav*"
        # else:
        pattern = f"*{line2}.wav"
        # print(pattern)
        count += 1
        order += 1
        for root, dirs, files in os.walk(wav_path):
            # for filename in sorted(files, key=sort_by_number):
            # print(line2)
            for filename in fnmatch.filter(files, pattern):
                matches.append({"filename": filename, "content": filename})

        if len(matches) == 0:
            for wem, meta in wem_meta.items():
                if meta == line2:
                    charactor = wem.split('_', 1)[0]
                    content = f"{charactor}_{meta}.wav"
                    matches.append({"filename": f"{wem}.wav", "content": content})
                    # print(matches)
                    break
        # print(matches)
        for match in matches:
            # print(match)
            specific_line = generate_line_srt_by_filename(match['content'])
            # specific_line = line1.split('<br>')[0]
            # for ending in [" v3", " v2", " v1"]:
            #     if specific_line.endswith(ending):
            #         specific_line = specific_line[:-len(ending)]
            # specific_line = specific_line.replace("<i>", "").replace("</i>", "")
            print(specific_line)

            wav_current = rf"{wav_path}{match['filename']}"
            audio_segment = AudioSegment.from_file(wav_current, format='wav')
            output_audio += audio_segment + AudioSegment.silent(duration=time_gap)

            duration = len(audio_segment)
            subtitle_item = pysrt.SubRipItem()

            subtitle_item.start = pysrt.SubRipTime(milliseconds=current_time)
            subtitle_item.end = subtitle_item.start + pysrt.SubRipTime(milliseconds=duration)
            subtitle_item.index = order
            subtitle_item.text = f"{specific_line}"

            current_time += duration + time_gap

            subtitles.append(subtitle_item)

        # current_time += time_gap * 3
        # output_audio += AudioSegment.silent(duration=time_gap*3)

    wav_destination = rf"{script_path}{job_name}_{job_name}.wav"
    output_audio.export(wav_destination, format="wav")
    print(f"saved wav: {wav_destination}")
    srt_destination = rf"{script_path}{job_name}_{job_name}.srt"
    subtitles.save(srt_destination)
    print(f"saved srt: {srt_destination}")
    print(order)


def generate_full_audio():
    '''
    跟generate_full_audio_srt_by_file差不多，基本是废弃状态
    :return:
    '''
    time_gap = 1000
    output_audio = AudioSegment.silent(duration=time_gap)
    current_time = time_gap
    subtitles = pysrt.SubRipFile()
    order = 1
    # order_list = [8, 10, 12, 14, 32, 34, 36, 38, 56, 58, 60, 62, 80, 82, 84, 104, 106, 108, 110, 128, 130, 132, 134,
    #               152, 154, 156, 158, 178, 180, 182, 184, 202, 204, 206, 208]
    # new_order = []
    # for order_int in order_list:
    #     new_order.append(order_int-8)
    # order_list = new_order

    for root, dirs, files in os.walk(karlach_wav):
        # for file in sorted(files, key=sort_by_number):
        for file in files:
            # 提取文件名开头的序号
            # line_number = int(file.split("-", 1)[0])
            # # 查询对应台词
            # # specific_line = get_specific_line(karlach_tmp, line_number + 1)
            # pattern = r"\d+-(.*)\."
            # match = re.search(pattern, file)
            # if match:
            #     specific_line = match.group(1)
            # else:
            #     specific_line = get_specific_line(karlach_tmp, line_number + 1)

            # if sort_by_number(file) in order_list:
            if "_" in file:
                charactor = file.split('_', 1)[0]
                if charactor in speaker_code:
                    speaker = speaker_code[charactor]
                else:
                    speaker = ""
                    print(charactor)
                if charactor in speaker_code_ch:
                    speaker_ch = speaker_code_ch[charactor]
                else:
                    speaker_ch = ""
            specific_line = f"{speaker_ch}\n{speaker}"
            print(specific_line)

            wav_current = rf"{karlach_wav}{file}"
            audio_segment = AudioSegment.from_file(wav_current, format='wav')
            output_audio += audio_segment + AudioSegment.silent(duration=time_gap)

            duration = len(audio_segment)
            subtitle_item = pysrt.SubRipItem()

            subtitle_item.start = pysrt.SubRipTime(milliseconds=current_time)
            subtitle_item.end = subtitle_item.start + pysrt.SubRipTime(milliseconds=duration)
            subtitle_item.index = order
            subtitle_item.text = f"{specific_line}"

            current_time += duration + time_gap

            subtitles.append(subtitle_item)
            order += 1

        wav_destination = rf"{karlach_directory}output.wav"
        output_audio.export(wav_destination, format="wav")
        print(f"saved wav: {wav_destination}")
        srt_destination = rf"{karlach_directory}output.srt"
        subtitles.save(srt_destination)
        print(f"saved srt: {srt_destination}")
        print(order)
