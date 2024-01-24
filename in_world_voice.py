import json
import os
import shutil
import fnmatch
from pydub import AudioSegment
import pysrt
import random

from utils import *
from constant import *

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
    sommon_f.close()

    need_note = "PointNClick" in filename
    # print(sommon_content)
    sommon_json_content_list = load_text_from_lsj(sommon_content, need_note)
    print(sommon_json_content_list)

    target_location = f"{script_location}{filename[:-4]}.txt"

    if need_note:
        write_multi_text_from_lsj(sommon_json_content_list, script_location)
        generate_file_order(script_location)
        # generate_partial_final_txt(script_location)
        double_check_file_order(script_location)
    else:
        out_string += print_text_from_lsj(sommon_json_content_list, filename[:-4])
        if not os.path.exists(karlach_directory):
            os.makedirs(karlach_directory)
        out_string = out_string.rstrip("\n")
        with open(target_location, "w", encoding="utf-8") as output_txt:
            output_txt.write(out_string)


def create_dialog_txt_only(script_location):
    final_txt = []
    for i in range(1, 95):
        txt_location = f"{script_location}{i}.txt"
        print(f"loading from {txt_location}")

        with open(txt_location, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for j in range(0, len(lines), 2):
            line1 = lines[j].strip().replace("<i>", "").replace("</i>", "") \
                .replace("<br>", "").replace("<b>", "").replace("</b>", "")
            print(line1)
            final_txt.append(line1)

    target_location = f"{script_location}all_txt.txt"
    final_txt = list(set(final_txt))

    with open(target_location, "w", encoding="utf-8") as output_txt:
        output_txt.write('\n'.join(final_txt))
        print(f"Writing lines to {target_location}")


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
                matches = find_through_metafile(line2, wem_meta)
                if matches is not None and len(matches) == 0:
                    print(f"{line2} not found in meta")
                else:
                    print(f"{line2} found in meta")

            elif len(matches) > 1:
                print(f"{pattern} have more then 1 matches")
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


def generate_srt_for_translations(working_path, script_txt, dict_path, job_name):
    out_path = rf"{working_path}needs_to_be_translated.txt"

    with open(script_txt, 'r') as file:
        working_scenario_list = json.load(file)
    with open(dict_path, 'r') as file:
        dict_json = json.load(file)

    lines = []
    for need_to_work in working_scenario_list:
        for key, strings in need_to_work.items():
            for string in strings:
                out_list = find_dicts_with_key(string, dict_json)
                for tmp_dict in out_list:
                    for tmp, paths in tmp_dict.items():
                        for path in paths:
                            txt_path = rf"{working_path}{path}"
                            with open(txt_path, "r") as file:
                                lines += file.readlines()

    even_lines = lines[0::2]
    lines_needs_to_be_translated = list(set(even_lines))

    lines_needs_to_be_translated = [
        string.replace("<i>", "").replace("</i>", "").replace("<br>", "").replace("</br>", "").strip() for string in
        lines_needs_to_be_translated]

    with open(out_path, 'w') as file:
        file.writelines(lines_needs_to_be_translated)


def check_translation(working_path):
    need_to_translation_path = rf"{working_path}needs_to_be_translated.txt"

    with open(need_to_translation_path, 'r') as file:
        uniq_line = file.readlines()

    out_path = rf"{working_path}needs_to_be_translated.txt"
    translation_json = load_tav_translation(astarion_translation_path)

    translation_eng = []
    need_to_add = []
    for engline, chline in translation_json.items():
        translation_eng.append(f"{engline}\n")
    for uniq in uniq_line:
        if uniq not in translation_eng:
            need_to_add.append(uniq.replace("\n", ""))
    print(len(need_to_add))
    print(need_to_add)


def generate_full_audio_srt_by_file(base_path, script_txt, dict_path, wav_path, job_name):
    """
    根据中间文件txt，生成字幕及音频
    :param job_name:
    :param dict_path:
    :param base_path:
    :param script_txt:
    :param wav_path:
    :return:
    """
    if "PointNClick" not in job_name:
        with open(script_txt, 'r') as file:
            lines = file.readlines()
        # even_lines = list(set(lines[1::2])
        # even_lines = lines[1::2]
        print(lines)
        # print(even_lines)
        generate_wav_srt_by_txt(lines, base_path, wav_path, job_name, True, True, {})
    else:
        with open(script_txt, 'r') as file:
            working_scenario_list = json.load(file)
        with open(dict_path, 'r') as file:
            dict_json = json.load(file)
        print(dict_json)
        generate_wav_srt_for_PnC(working_scenario_list, base_path, dict_json, job_name, wav_path)


def generate_wav_srt_for_PnC(working_scenario_list, root_path, dict_json, job_name, wav_path, ):
    if "GenericOrigin" in job_name:
        translation_json = tav_pnc_translation
    elif "Jaheira" in job_name:
        translation_json = load_char_translation(jaheira_translation_path)
    elif "Astarion" in job_name:
        translation_json = load_char_translation(astarion_translation_path)
    elif "Gale" in job_name:
        translation_json = load_char_translation(gale_translation_path)
    else:
        translation_json = {}
    wem_meta = {}

    time_gap = 600

    output_audio = AudioSegment.silent(duration=time_gap)
    current_time = time_gap
    subtitles = pysrt.SubRipFile()
    subtitles_note = pysrt.SubRipFile()
    order = 1
    count = 0
    note_order = 1
    for need_to_work in working_scenario_list:
        for key, strings in need_to_work.items():
            for string in strings:
                out_list = find_dicts_with_key(string, dict_json)
                for tmp_dict in out_list:
                    for tmp, paths in tmp_dict.items():
                        length = 0
                        subtitle_note_item = pysrt.SubRipItem()
                        subtitle_note_item.start = pysrt.SubRipTime(milliseconds=current_time)

                        for path in paths:
                            txt_path = rf"{root_path}{path}"
                            with open(txt_path, "r") as file:
                                lines = file.readlines()
                                length += len(file.readlines())

                                even_lines = lines[1::2]

                                for i in range(0, len(even_lines)):
                                    matches = []
                                    line2 = even_lines[i].strip()
                                    pattern = f"*{line2}.wav"
                                    count += 1
                                    order += 1
                                    for root, dirs, files in os.walk(wav_path):
                                        for filename in fnmatch.filter(files, pattern):
                                            matches.append({"filename": filename, "content": filename})

                                    if len(matches) == 0:
                                        for wem, meta in wem_meta.items():
                                            if meta == line2:
                                                charactor = wem.split('_', 1)[0]
                                                content = f"{charactor}_{meta}.wav"
                                                matches.append({"filename": f"{wem}.wav", "content": content})
                                                break
                                    for match in matches:
                                        specific_line = generate_line_srt_by_filename(match['content'], False, False,
                                                                                      translation_json)
                                        print(specific_line)

                                        wav_current = rf"{wav_path}{match['filename']}"
                                        audio_segment = AudioSegment.from_file(wav_current, format='wav')
                                        output_audio += audio_segment + AudioSegment.silent(duration=time_gap)

                                        duration = len(audio_segment)
                                        subtitle_item = pysrt.SubRipItem()

                                        subtitle_item.start = pysrt.SubRipTime(milliseconds=current_time)
                                        subtitle_item.end = subtitle_item.start + pysrt.SubRipTime(
                                            milliseconds=duration)
                                        subtitle_item.index = order
                                        subtitle_item.text = f"{specific_line}"

                                        current_time += duration + time_gap

                                        subtitles.append(subtitle_item)
                        note_order += 1
                        subtitle_note_item.end = pysrt.SubRipTime(milliseconds=current_time)
                        subtitle_note_item.index = note_order
                        subtitle_note_item.text = f"{tmp}"
                        subtitles_note.append(subtitle_note_item)

    wav_destination = rf"{root_path}{job_name}.wav"
    output_audio.export(wav_destination, format="wav")
    print(f"saved wav: {wav_destination}")
    srt_destination = rf"{root_path}{job_name}.srt"
    subtitles.save(srt_destination)
    print(f"saved srt: {srt_destination}")
    print(order)
    srt_note_destination = rf"{root_path}{job_name}_note.srt"
    subtitles_note.save(srt_note_destination)
    print(f"saved srt: {srt_note_destination}")
    print(note_order)


def generate_wav_srt_by_txt(lines, out_path, wav_path, job_name, with_speaker, with_ch, translation_json):
    even_lines = lines[1::2]

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
            specific_line = generate_line_srt_by_filename(match['content'], with_speaker, with_ch, translation_json)
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

    wav_destination = rf"{out_path}{job_name}_{job_name}.wav"
    output_audio.export(wav_destination, format="wav")
    print(f"saved wav: {wav_destination}")
    srt_destination = rf"{out_path}{job_name}_{job_name}.srt"
    subtitles.save(srt_destination)
    print(f"saved srt: {srt_destination}")
    print(order)


def generate_full_audio(wav_path, outwav_name):
    '''
    直接将wav_path中的所有wav拼接在一起
    :return:
    '''
    time_gap = 1000
    output_audio = AudioSegment.silent(duration=time_gap)

    for root, dirs, files in os.walk(wav_path):
        for file in files:
            if ".wav" in file:
                wav_current = rf"{wav_path}{file}"
                print(wav_current)

                audio_segment = AudioSegment.from_file(wav_current, format='wav')
                output_audio += audio_segment + AudioSegment.silent(duration=time_gap)

        wav_destination = rf"{wav_path}{outwav_name}.wav"
        output_audio.export(wav_destination, format="wav")
        print(f"saved wav: {wav_destination}")
