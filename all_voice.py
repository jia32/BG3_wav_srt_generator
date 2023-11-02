import json
import os
import shutil
import fnmatch
from pydub import AudioSegment
import pysrt
from utils import generate_line_srt_by_filename, load_text_from_lsj
from constant import char_final, translated, base_path

'''
@Project:        BG3 voice generator
@File:           all_voice.py
@Author:         Jasmine
@Description：   手动复制粘贴wem并转换成wav后，根据角色名称自动生成音频及字幕
                 由于实在是太大了所以手动iteration
'''

def distinguish_audio(job_name):
    wav_path = rf"{base_path}{job_name}\wav\\"
    char_wav_path = rf"{base_path}{job_name}\char_wav\\"
    orin_tmp_path = rf"{base_path}Orin\scripts\wav\{job_name}\\"
    if not os.path.exists(char_wav_path):
        os.makedirs(char_wav_path)
    if not os.path.exists(orin_tmp_path):
        os.makedirs(orin_tmp_path)
    output_file_path = rf"{base_path}\{job_name}\need_to_move.json"

    # gather_to_be_moved(wav_path, char_wav_path)
    # copy_with_file_list(output_file_path, char_wav_path)
    # remove_orin(orin_path, wav_path, orin_tmp_path)


def remove_orin(orin_path, wav_path, target_path):
    file_match = []
    count = 0

    for root, dirs, files in os.walk(orin_path):
        for filename in files:
            pattern = f"*{filename}"
            for wav_root, wav_dirs, wav_files in os.walk(wav_path):
                for matched_wav in fnmatch.filter(wav_files, pattern):
                    file_match.append(matched_wav)
                    source_wav = os.path.join(wav_root, matched_wav)
                    shutil.move(source_wav, target_path)
                    print(f"moved {matched_wav} to {target_path}")
                    count += 1
    print(f"moved {count} files")


def copy_with_file_list(output_file_path, target_path):
    with open(output_file_path, 'r', encoding='utf-8') as f:
        data = f.read()
    file_list = eval(data)
    count = 0
    print(f"need to copy {len(file_list)} files")

    for file_dict in file_list:
        for key, value in file_dict.items():
            shutil.move(value, target_path)
            print(f"moved {key} from {value} to {target_path}")
            count += 1
    print(f"copied {count} files")


def gather_to_be_moved(path, job_name):
    to_be_moved = []
    for root, dirs, files in os.walk(path):
        for i, file in enumerate(files):
            wav_current = rf"{path}{file}"
            specific_line = generate_line_srt_by_filename(file)
            if specific_line != '' and specific_line.find('\n') == -1:
                current = {specific_line: wav_current}
                to_be_moved.append(current)
                print(current)
            else:
                print()
    output_file_path = rf"{base_path}\{job_name}\need_to_move.list"
    with open(output_file_path, 'w') as output_file:
        json.dump(to_be_moved, output_file)


def combine_char_audio(job_name):
    wav_path = rf"{base_path}\{job_name}\char_wav\\"
    out_path = rf"{base_path}\{job_name}\\"
    char_f = open(char_final, 'r', encoding='utf-8')
    char_f_content = json.loads(char_f.read())
    json_content_list = load_text_from_lsj(char_f_content)
    # print(json_content_list)
    count = 0
    matches = []
    for node in json_content_list:
        if 'note' not in node:
            # print(node)
            continue
        specific_line = node['note']
        line_matches = []
        file_match = []
        if 'content_list' in node:
            for content in node['content_list']:

                pattern = f"*{content['contentuid']}.wav"
                count += 1
                for root, dirs, files in os.walk(wav_path):
                    # for filename in sorted(files, key=sort_by_number):
                    #     print(line2)
                    for filename in fnmatch.filter(files, pattern):
                        file_match.append(filename)
                        count += 1
            if len(file_match) != 0:
                line_matches.append({
                    "filelist": file_match,
                    "text": specific_line
                })
        if line_matches:
            matches.append(line_matches)

    time_gap = 500
    output_audio = AudioSegment.silent(duration=time_gap)
    order = 0
    current_time = 500
    subtitles = pysrt.SubRipFile()

    for match in matches:
        # print(match)
        specific_line = match[0]['text'].strip()
        if "\n" not in specific_line:
            specific_line = add_translation(specific_line)
        order += 1
        num = 0
        current_audio = AudioSegment.silent(duration=0)

        for wav_current in match[0]['filelist']:
            wav_current = rf"{wav_path}{wav_current}"
            audio_segment = AudioSegment.from_file(wav_current, format='wav')
            current_audio += audio_segment + AudioSegment.silent(duration=time_gap)
            num += 1
            print(wav_current)
            # print(len(audio_segment))
        print(num)
        duration = len(current_audio)
        print(duration)

        subtitle_item = pysrt.SubRipItem()

        subtitle_item.start = pysrt.SubRipTime(milliseconds=current_time)
        subtitle_item.end = subtitle_item.start + pysrt.SubRipTime(milliseconds=duration)
        subtitle_item.index = order
        subtitle_item.text = f"{specific_line}"
        print(specific_line)
        print(current_time)
        # print(specific_line)

        subtitles.append(subtitle_item)
        output_audio += current_audio + AudioSegment.silent(duration=time_gap)
        current_time = len(output_audio)

    out_srt_destination = rf"{out_path}out_char.srt"
    subtitles.save(out_srt_destination)
    print(f"saved srt: {out_srt_destination}")
    wav_destination = rf"{out_path}out_char.wav"
    output_audio.export(wav_destination, format="wav")
    print(f"saved wav: {wav_destination}")


def add_translation(line):
    if line in translated:
        return f"{translated[line]}\n{line}"
    else:
        return line


def combine_audio(job_name):
    '''
    组合最后的音频和字幕
    有些角色的太多了，所以以1000为界。由于跑得太慢所以没有做完全的自动化处理，手动iteration
    :param job_name:
    :return:
    '''
    path = rf"{base_path}{job_name}\wav\\"
    out_path = rf"{base_path}{job_name}\\"
    time_gap = 500
    output_audio = AudioSegment.silent(duration=time_gap)
    order = 0
    current_time = time_gap
    subtitles = pysrt.SubRipFile()

    file_limit = 1000  # 每个输出文件包含的最大文件数量
    output_counter = 1  # 输出文件计数器

    for root, dirs, files in os.walk(path):
        for i, file in enumerate(files):
            # if i > 6000:
            wav_current = rf"{path}{file}"
            audio_segment = AudioSegment.from_file(wav_current, format='wav')

            channel1 = audio_segment.channels
            channel2 = output_audio.channels
            if channel1 != channel2:
                if channel1 > channel2:
                    audio_segment = audio_segment.set_channels(channel2)
                if channel1 < channel2:
                    output_audio = output_audio.set_channels(channel1)

            output_audio += audio_segment + AudioSegment.silent(duration=time_gap)
            order += 1
            print(order)
            specific_line = generate_line_srt_by_filename(file)
            print(specific_line)

            duration = len(audio_segment)
            subtitle_item = pysrt.SubRipItem()

            subtitle_item.start = pysrt.SubRipTime(milliseconds=current_time)
            subtitle_item.end = subtitle_item.start + pysrt.SubRipTime(milliseconds=duration)
            subtitle_item.index = order
            subtitle_item.text = f"{specific_line}"

            current_time += duration + time_gap

            subtitles.append(subtitle_item)
            if i == 1000:
                # if (i + 1) % file_limit == 0:
                # out_wav_destination = rf"{out_path}out_{output_counter}.wav"
                # output_audio.export(out_wav_destination, format="wav")
                # output_counter += 1
                # output_audio = AudioSegment.silent(duration=0)

                out_srt_destination = rf"{out_path}all_1.srt"
                subtitles.save(out_srt_destination)
                print(f"saved srt: {out_srt_destination}")
                wav_destination = rf"{out_path}all_1.wav"
                output_audio.export(wav_destination, format="wav")
                print(f"saved wav: {wav_destination}")
    # current_time += time_gap * 3
    # output_audio += AudioSegment.silent(duration=time_gap*3)

    # 处理剩余的文件
    # if len(output_audio) > 0:
    #     out_wav_destination = rf"{out_path}out_{output_counter}.wav"
    #     output_audio.export(out_wav_destination, format="wav")
    # out_srt_destination = rf"{out_path}out_{output_counter}.srt"
    # subtitles.save(out_srt_destination)
    # print(f"saved srt: {out_srt_destination}")
