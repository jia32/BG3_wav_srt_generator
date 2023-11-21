import json
import os
import shutil
import fnmatch
from pydub import AudioSegment
import pysrt
from PIL import Image
from constant import school_list, spell_json, voice_location, school_path_wem, school_path_wav, \
    speaker_code, spell_icon, translated_spell
from utils import content_exist, sort_by_number

tmp_order = ['h8b43b0acg323cg44fbg910eg712f6b5b545b', 'hef563c3bg94b5g4e25gb5dag8c6a6f361e22',
             'hfad5c255g3d3cg4aa5gbae0ga8c89ab7a90e', 'h356e0207gf8c9g4171g862cgf85d9760be09',
             'h48cf9493g5c07g4fe4gb47bg67864c98cb9f', 'h9895257egb924g4effg912cgb5b44d4098a2',
             'hf00c7012gc068g484eg9b4bg3c26342c247f', 'h173cacffgaa6fg4558gbca8g864c2a5d8e5c',
             'h848fe684ga338g4555g8e45ge95d5a2f5342', 'hfb3dc237gd2c2g4101g9f98ged994f612697',
             'h13aa341cg89fdg4c1aga0ddg57941fd8ee9e', 'h66ef9c55g3226g47e6g9a31g7e10bc27a9e2',
             'h4ae6d73bg0f8fg4eacgb024g1036f0b7523a', 'he79cbf1eg4411g49e3g9137g0453bea51f08',
             'h8c83e7b4g0e7eg4198gbd38g28226af40cc9', 'h3b8f941bga0eag47a8g83e2g8e35861eca9e',
             'h6506ee73g01d1g4778gb2b6ga142dc87f531', 'h1787081bg8f62g4613g9552g85ce498beb17',
             'ha46e5b49g5dadg4766g8fb2g13d4a42c4f51', 'hfe9a326bgbcd2g4bbagaf8cg115902432bdc',
             'h8dee04a1gf7ecg4478ga300g4b2ae47a520a', 'hcd1bb4c0gb178g4e7agabfag0c3ea2413874',
             'h0c98fea7gd78dg4bc4ga990g3de9c109eef9', 'hf8ab0b8agac8ag4491g9b89g4e51c9465b04',
             'ha2734e20g2342g42c5g8a20g34b83256a213', 'h55a1014eg96bfg4926ga750g8548b06abed0',
             'h7a33a703g5046g45b9ga8a8g40d66dfacbe4', 'h4cf8ea57g952eg41e8g8af7ge7209e343279',
             'he7087be6g22e0g4466gaee6gd5e38a3ecd6a', 'he7f83310g162bg425agac62g9a06dc709cec',
             'ha028e318g6f18g4e99g850agce0075738ddb', 'h9fb57fb4g8574g4a63ga293gaaca1c5c2af7',
             'h39d30c9dgbd9fg430egb013g664f119bf9ef', 'h6c60d320gaf48g48e2gbaefg4b56ebf8b285',
             'h48f8b812g46ffg424bg83e4gf3472c51f65b', 'h051a4870g670eg4c91ga602g43c370eb8cee',
             'hb345642bgef80g4429g822dgdf5e9eaa1b6f', 'hddcb3a27ge8a6g4724g9210ge6492203b5a6',
             'h0bb5ab76g0e99g44f4gb7efg60e90fc29c54', 'hdcee8b1dg27fcg4097ga1b8gcea06761dfe0',
             'h4db73f45g8934g488fga75bg4ecc3e59b328']


def copy_wem_by_ch(base_path, script_path):
    # TODO: copy wav
    return


def copy_wem_by_school():
    count = 0
    with open(school_list, 'r') as file:
        abj_spell_list = [line.rstrip('\r\n') for line in file.readlines()]
    with open(spell_json, 'r', encoding='utf-8') as f:
        json_content = json.loads(f.read())
    unique_list = []
    need_to_be_copied = []
    for spell_logic in abj_spell_list:
        for spell_line in json_content:
            if spell_line['logic'] == spell_logic:
                if spell_logic in unique_list:
                    continue
                unique_list.append(spell_logic)
                print(spell_logic)
                for spell_content in spell_line['content_list']:
                    # random_spell_content = random.choice(spell_line['content_list'])
                    if content_exist(spell_content["contentuid"]):
                        need_to_be_copied.append(spell_content["contentuid"])
                        break
    print(unique_list)
    print(need_to_be_copied)
    # need_to_be_copied = ['h8b43b0acg323cg44fbg910eg712f6b5b545b', 'hef563c3bg94b5g4e25gb5dag8c6a6f361e22', 'hfad5c255g3d3cg4aa5gbae0ga8c89ab7a90e', 'h356e0207gf8c9g4171g862cgf85d9760be09', 'h48cf9493g5c07g4fe4gb47bg67864c98cb9f', 'h9895257egb924g4effg912cgb5b44d4098a2', 'hf00c7012gc068g484eg9b4bg3c26342c247f', 'h173cacffgaa6fg4558gbca8g864c2a5d8e5c', 'h848fe684ga338g4555g8e45ge95d5a2f5342', 'hfb3dc237gd2c2g4101g9f98ged994f612697', 'h13aa341cg89fdg4c1aga0ddg57941fd8ee9e', 'h66ef9c55g3226g47e6g9a31g7e10bc27a9e2', 'h4ae6d73bg0f8fg4eacgb024g1036f0b7523a', 'he79cbf1eg4411g49e3g9137g0453bea51f08', 'h8c83e7b4g0e7eg4198gbd38g28226af40cc9', 'h3b8f941bga0eag47a8g83e2g8e35861eca9e', 'h6506ee73g01d1g4778gb2b6ga142dc87f531', 'h1787081bg8f62g4613g9552g85ce498beb17', 'ha46e5b49g5dadg4766g8fb2g13d4a42c4f51', 'hfe9a326bgbcd2g4bbagaf8cg115902432bdc', 'h8dee04a1gf7ecg4478ga300g4b2ae47a520a', 'hcd1bb4c0gb178g4e7agabfag0c3ea2413874', 'h0c98fea7gd78dg4bc4ga990g3de9c109eef9', 'hf8ab0b8agac8ag4491g9b89g4e51c9465b04', 'ha2734e20g2342g42c5g8a20g34b83256a213', 'h55a1014eg96bfg4926ga750g8548b06abed0', 'h7a33a703g5046g45b9ga8a8g40d66dfacbe4', 'h4cf8ea57g952eg41e8g8af7ge7209e343279', 'he7087be6g22e0g4466gaee6gd5e38a3ecd6a', 'he7f83310g162bg425agac62g9a06dc709cec', 'ha028e318g6f18g4e99g850agce0075738ddb', 'h9fb57fb4g8574g4a63ga293gaaca1c5c2af7', 'h39d30c9dgbd9fg430egb013g664f119bf9ef', 'h6c60d320gaf48g48e2gbaefg4b56ebf8b285', 'h48f8b812g46ffg424bg83e4gf3472c51f65b', 'h051a4870g670eg4c91ga602g43c370eb8cee', 'hb345642bgef80g4429g822dgdf5e9eaa1b6f', 'hddcb3a27ge8a6g4724g9210ge6492203b5a6', 'h0bb5ab76g0e99g44f4gb7efg60e90fc29c54', 'hdcee8b1dg27fcg4097ga1b8gcea06761dfe0', 'h4db73f45g8934g488fga75bg4ecc3e59b328']

    count = 0
    for file_name in need_to_be_copied:
        pattern = f"*{file_name}.wem"
        for root, dirs, files in os.walk(voice_location):
            for filename in fnmatch.filter(files, pattern):
                # If the filename matches the pattern, print the full path of the file
                # print(os.path.join(root, filename))
                source_file = os.path.join(root, filename)
                target_directory = f"{school_path_wem}"
                print(target_directory)
                copied_path = shutil.copy(source_file, target_directory)
                print(f"copied to {copied_path}")
                count += 1
    print(f"copied {count} files")
    # organize_by_companion()
    return need_to_be_copied


def organize_by_companion():
    # pattern = f"*{file_name}.wem"
    with open(school_list, 'r') as file:
        spell_list = [line.rstrip('\r\n') for line in file.readlines()]

    for root, dirs, files in os.walk(school_path_wav):
        for filename in files:
            if "_" in filename:
                charactor = filename.split('_', 1)[0]
                if charactor in speaker_code:
                    for i, spell in enumerate(tmp_order):
                        if spell in filename:
                            file_order = i
                            break
                        else:
                            file_order = "school"
                    target_location = f"{school_path_wav}{speaker_code[charactor]}\\"
                    if not os.path.exists(target_location):
                        os.makedirs(target_location)

                    target_filename = f"{target_location}{file_order}.wav"
                    print(target_filename)
                    if not os.path.exists(target_filename):
                        copied_path = shutil.copy(os.path.join(root, filename), target_filename)
                        print(f"copied to {copied_path}")
                    else:
                        print(f"{target_filename} exists, skip")


def generate_spell_audio():
    with open(spell_json, 'r', encoding='utf-8') as f:
        json_content = json.loads(f.read())

    time_gap = 800

    character_list = list(speaker_code.values())
    for character in character_list:
        output_audio = AudioSegment.silent(duration=time_gap)
        current_time = time_gap
        subtitles = pysrt.SubRipFile()
        order = 1

        wav_path = rf"{school_path_wav}{character}\\"
        print(wav_path)
        for root, dirs, files in os.walk(wav_path):
            for file in sorted(files, key=sort_by_number):
                # 查询对应台词
                specific_line = generate_spell_srt_line(json_content, tmp_order[order - 1])
                wav_current = rf"{wav_path}{file}"
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

        # wav_destination = rf"{school_path_wav}{character}.wav"
        # output_audio.export(wav_destination, format="wav")
        # print(f"saved wav: {wav_destination}")
        srt_destination = rf"{school_path_wav}{character}.srt"
        subtitles.save(srt_destination)
        print(f"saved srt: {srt_destination}")
        print(order)


def convert_dds_to_png():
    for root, dirs, files in os.walk(spell_icon):
        for file in files:
            image = Image.open(rf"{spell_icon}{file}")
            image.save(f"{spell_icon}{file[:-4]}.png", "PNG")


def generate_spell_srt_line(spell_list, filename):
    # print(filename)

    for spell_node in spell_list:
        for spell in spell_node['content_list']:
            if spell['contentuid'] in filename:
                # print(spell_node)
                print(spell['eng'])
                # latin = spell['eng'].replace("<br>", "")
                latin = spell['eng'].split('<br>')[0].strip()
                for ending in [" v3", " v2", " v1"]:
                    if latin.endswith(ending):
                        latin = latin[:-len(ending)]

                return f"{latin}\n{spell_node['context']}\n{translated_spell[spell_node['context']]}"
