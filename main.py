from party_banter import generate_script, output_dialog_order, combine_audio_sub
from in_world_voice import create_dialog_txt, print_dialog_txt, copy_audio_wem, generate_full_audio, \
    generate_full_audio_srt_by_file
from spell import copy_wem_by_school, organize_by_companion, generate_spell_audio, convert_dds_to_png
from all_voice import distinguish_audio, generate_line_srt_by_filename, combine_audio
from single_lsj import generate_other_script
from constant import base_path


def generate_spell_files():
    # dont run top 2
    # collect_spell_files()
    # print_spell()

    # start from here
    copy_wem_by_school()
    # update tmp_order with output from previous step
    organize_by_companion()
    generate_spell_audio()
    convert_dds_to_png()


def generate_char_script():
    # write_output_json(char_ori, char_final)
    script_location = rf"{base_path}\Daisy\script\\"
    # job_list = ['GLO_Elminster_AD_Camp', 'GLO_Elminster_AD_Volo',
    #             'GLO_Elminster_AD_GaleTressym', 'GLO_Elminster_AD_Gale']
    job_name = "Daisy_ContingencyLines_Final"

    # for job_name in job_list:
    filename = f"{job_name}.lsj"

    # print_dialog_txt()

    # target_folder = rf"{base_path}\Orin\scripts\imposter_npc\\"
    script_txt = rf"{script_location}{job_name}.txt"
    current_target_path = rf"{script_location}\wem\{job_name}\\"
    #
    # script_path = rf"{base_path}\Orin\scripts\{job_name}\\"
    # script_txt = f"{script_path}{job_name}.txt"
    wav_path = rf"{script_location}\wav\\"

    # create_dialog_txt(script_location, filename)
    # copy_audio_wem(script_txt, current_target_path)
    generate_full_audio_srt_by_file(script_location, script_txt, wav_path, job_name)
    # generate_full_audio()


def generate_banter_files():
    generate_script()  # 加载文件夹里的事件脚本
    # output_dialog_order(1) # 复制目标wem文件
    # output_dialog_order(2) # 调整对话的顺序，手动加random形式
    # output_dialog_order(3) # 根据file_list，生成输出的脚本
    # # 需要手动将wem转换为wav
    # combine_audio_sub()  # 合成音频和字幕


def generate_other_files():
    generate_other_script()  # 加载文件夹里的事件脚本


def generate_all_files():
    char = "daisy"
    distinguish_audio(char)
    # combine_char_audio(char)

    combine_audio(char, 1, 1000)
    # combine_audio(char, 2, 1000)
    # combine_audio(char, 3, 1000)
    # combine_audio(char, 4, 1000)
    # combine_audio(char, 5, 1000)
    # combine_audio(char, 6, 1000)
    # combine_audio(char, 7, 1000)
    # combine_audio(char, 8, 1000)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # generate_banter_files()
    # generate_other_files()
    generate_char_script()
    # generate_spell_files()
    # generate_all_files()
