from pydub import AudioSegment
import pysrt
from PIL import Image
from utils import *

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


def copy_spell_wem_by_ch(char):
    source_wem_path = rf"{base_path}{char}\char_wav\\"
    target_directory = rf"{base_path}{char}\spell_wav\\"
    target_spell_list_path = rf"{base_path}{char}\spell.json"

    print(source_wem_path)
    if not os.path.exists(source_wem_path):
        print("need to copy char_wav")
        return

    with open(spell_all_txt, 'r') as file:
        all_spell_list = [line.rstrip('\r\n') for line in file.readlines()]

    with open(spell_json, 'r', encoding='utf-8') as f:
        json_content = json.loads(f.read())

    need_to_be_copied = {}
    for spell_logic in all_spell_list:
        need_to_be_copied[spell_logic] = []
        for spell_line in json_content:
            if spell_line['logic'] == spell_logic:
                # print(spell_logic)
                for spell_content in spell_line['content_list']:
                    pattern = f"*{spell_content['contentuid']}.wav"
                    found_file = if_content_exist(pattern, source_wem_path)
                    if found_file:
                        need_to_be_copied[spell_logic].append(found_file)

    print(len(need_to_be_copied))
    with open(target_spell_list_path, 'w') as output_file:
        json.dump(need_to_be_copied, output_file)

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    count = 0
    for spell_desc_spec, filename_list in need_to_be_copied.items():
        for wav_file in filename_list:
            for root, dirs, files in os.walk(source_wem_path):
                for filename in fnmatch.filter(files, wav_file):
                    source_file = os.path.join(root, filename)
                    shutil.move(source_file, target_directory)
                    print(f"move {source_file} to {target_directory}")
                    count += 1
        print(f"copied {count} files")

    return need_to_be_copied


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


def generate_spell_audio(char):
    source_wav_path = rf"{base_path}{char}\spell_wav\\"
    target_directory = rf"{base_path}{char}\spell\\"
    target_spell_list_path = rf"{base_path}{char}\spell.json"
    spell_list = spell_order_txt

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    with open(target_spell_list_path, 'r', encoding='utf-8') as f:
        spell_list_json = json.loads(f.read())

    with open(spell_list, 'r') as file:
        spell_list = file.readlines()

    time_gap = 800

    output_audio = AudioSegment.silent(duration=time_gap)
    current_time = time_gap
    subtitles = pysrt.SubRipFile()
    subtitles_desc = pysrt.SubRipFile()
    order = 1

    for spell_order in spell_list:
        spell_desc_name = spell_order.strip()
        wav_list = spell_list_json[spell_order.strip()]
        subtitle_item = pysrt.SubRipItem()
        subtitle_item_desc = pysrt.SubRipItem()
        specific_line = find_spell_srt_by_desc(spell_desc_name)
        spell_note = find_spell_note_by_desc(spell_desc_name)

        subtitle_item.start = pysrt.SubRipTime(milliseconds=current_time)
        subtitle_item_desc.start = pysrt.SubRipTime(milliseconds=current_time)
        print(current_time)
        print(specific_line)

        if len(wav_list) > 0:
            wav_current = rf"{source_wav_path}{wav_list[0]}"
            audio_segment = AudioSegment.from_file(wav_current, format='wav')
            output_audio += audio_segment + AudioSegment.silent(duration=time_gap)
            duration = len(audio_segment)
            current_time += duration + time_gap

        print(current_time)
        subtitle_item.end = pysrt.SubRipTime(milliseconds=current_time)
        subtitle_item.index = order
        subtitle_item.text = f"{specific_line}"
        subtitles.append(subtitle_item)

        subtitle_item_desc.end = pysrt.SubRipTime(milliseconds=current_time)
        subtitle_item_desc.index = order
        subtitle_item_desc.text = f"{spell_note}"
        subtitles_desc.append(subtitle_item_desc)

        order += 1

        output_audio += AudioSegment.silent(duration=time_gap)
        current_time += time_gap

    wav_destination = rf"{target_directory}spell.wav"
    output_audio.export(wav_destination, format="wav")
    print(f"saved wav: {wav_destination}")
    srt_destination = rf"{target_directory}spell.srt"
    subtitles.save(srt_destination)
    print(f"saved srt: {srt_destination}")
    note_destination = rf"{target_directory}spell_note.srt"
    subtitles_desc.save(note_destination)
    print(f"saved note srt: {note_destination}")

    print(order)


def convert_dds_to_png():
    for root, dirs, files in os.walk(spell_icon):
        for file in files:
            image = Image.open(rf"{spell_icon}{file}")
            print(f"{spell_icon}{file[:-4]}.png")
            image.save(f"{spell_icon}{file[:-4]}.png", "PNG")


def find_spell_srt_by_desc(desc):
    with open(spell_json, 'r', encoding='utf-8') as f:
        json_content = json.loads(f.read())
    for spell_line in json_content:
        if spell_line['logic'] == desc:
            latin = spell_line['line']
            eng = spell_line['context']
            translated_ch = translated_spell[eng.strip()]
            return f"{translated_ch}\n{eng}\n{latin}"


def find_spell_note_by_desc(desc):
    with open(spell_with_ch, 'r', encoding='utf-8') as f:
        json_content = json.loads(f.read())
    for spell_line in json_content:
        spell_logic = spell_line['label']
        if spell_logic == desc:
            note_ch = spell_line['desc']
            if "L0" in spell_logic:
                note_ch = f"{note_ch}: 0环/戏法"
            elif "L1to3" in spell_logic:
                note_ch = f"{note_ch}: 1-3环"
            elif "L4to5" in spell_logic:
                note_ch = f"{note_ch}: 4-5环"
            if spell_line['spell'] != "":
                return f"{spell_line['label']}\n{note_ch}\n比如： {spell_line['spell']}"
            else:
                return f"{spell_line['label']}\n{note_ch}"



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
