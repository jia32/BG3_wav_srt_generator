from party_banter import *
from in_world_voice import *
from spell import *
from all_voice import *
from single_lsj import generate_other_script
from constant import base_path
from patch_diff import *


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
    script_location = rf"{base_path}\Halsin\script\\"
    # job_list = ['GLO_Elminster_AD_Camp', 'GLO_Elminster_AD_Volo',
    #             'GLO_Elminster_AD_GaleTressym', 'GLO_Elminster_AD_Gale']
    job_name = "GLO_BG_PointNClick_Halsin_NarrativeArc_Start"

    # for job_name in job_list:
    filename = f"{job_name}.lsj"

    # print_dialog_txt()

    # target_folder = rf"{base_path}\Orin\scripts\imposter_npc\\"
    # script_txt = rf"{script_location}{job_name}.txt"
    script_txt = rf"{script_location}file_name_dict.json"
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
    # generate_script()  # 加载文件夹里的事件脚本
    # output_dialog_order(1) # 复制目标wem文件
    # output_dialog_order(2)  # 调整对话的顺序，手动加random形式
    # output_dialog_order(3) # 根据file_list，生成输出的脚本
    output_dialog_order(4)  # 打印文本，对比一下
    # output_dialog_order(5)
    # # 需要手动将wem转换为wav
    # combine_audio_sub()  # 合成音频和字幕


def generate_other_files():
    generate_other_script()  # 加载文件夹里的事件脚本


def generate_all_files():
    char = "Halsin"
    # distinguish_audio(char)
    # combine_char_audio(char)

    combine_audio(char, 1, 1000)
    combine_audio(char, 2, 1000)
    combine_audio(char, 3, 1000)
    # combine_audio(char, 4, 1000)
    # combine_audio(char, 5, 1000)
    # combine_audio(char, 6, 1000)
    # combine_audio(char, 7, 1000)
    # combine_audio(char, 8, 1000)


def compare_new_patch():
    last_version = r"E:\tmp\converted\Patch-2\\"
    curr_version = r"E:\tmp\converted\Patch-4\\"
    find_different_files(last_version, curr_version)
    # difference_of_existing_files(curr_version)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # generate_banter_files()
    # generate_other_files()
    generate_char_script()
    # generate_spell_files()
    # generate_all_files()
    # compare_new_patch()
