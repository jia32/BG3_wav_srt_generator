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
    # csv_to_json(spell_out_csv, spell_with_ch)

    # start from here
    # copy_wem_by_school()
    char = "Minthara"
    # copy_spell_wem_by_ch(char)

    # update tmp_order with output from previous step
    # organize_by_companion()

    # generate_spell_audio(char)
    convert_dds_to_png()


def generate_char_script():
    # write_output_json(char_ori, char_final)
    script_location = rf"{base_path}Minthara\script\\"
    # job_list = os.listdir(script_location)
    # for job in job_list:
    #     job_name = job[:-4]
    #     print(job_name)
    # job_list = ['GLO_PAD_CombatReact_PartyDeath', 'GLO_BG_PointNClick_GenericOrigin_NarrativeArc_Start']
    job_name = "GLO_BG_PointNClick_Minthara_NarrativeArc_Start"

    # for job_name in job_list:
    filename = f"{job_name}.lsj"

    # print_dialog_txt()

    # target_folder = rf"{base_path}\Orin\scripts\imposter_npc\\"
    script_txt = rf"{script_location}{job_name}.txt"
    script_txt = rf"{script_location}final_order.json"
    dict_path = rf"{script_location}file_name_dict.json"
    # current_target_path = rf"{script_location}\wem\{job_name}\\"
    #
    # script_path = rf"{base_path}\Orin\scripts\{job_name}\\"
    # script_txt = f"{script_path}{job_name}.txt"
    wav_path = rf"{script_location}\wav\\"

    create_dialog_txt(script_location, filename)
    # create_dialog_txt_only(script_location)
    # Optional operations:
    # generate_partial_final_txt(script_location, "roman")
    # double_check_file_order(script_location)

    # copy_audio_wem(script_txt, current_target_path)
    #     script_txt = rf"{script_location}sneak.json"

    # generate_full_audio_srt_by_file(script_location, script_txt, dict_path, wav_path, job_name)
    # wav_path = rf"{script_location}\roman\\"
    # outwav_name = rf"roman"
    # generate_full_audio(wav_path, outwav_name)


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
    char = "Minthara"
    # copy_all_wem(char)
    distinguish_audio(char)
    # combine_char_audio(char)
    #
    # combine_audio(char, 1, 1000)
    # combine_audio(char, 2, 1000)
    # combine_audio(char, 3, 1000)
    # combine_audio(char, 4, 1000)
    # combine_audio(char, 5, 1000)
    # combine_audio(char, 6, 1000)
    # combine_audio(char, 7, 1000)
    # combine_audio(char, 8, 1000)


def compare_new_patch():
    last_version = r"E:\Project\BG3_party_banter\Data\text\Dialogs-patch4\\"
    curr_version = r"E:\Project\BG3_party_banter\Data\text\Dialogs-patch5\\"

    last_voice = r"E:\tmp\bg3-modders-multitool\UnpackedData\Voice\Mods\Gustav\Localization\English\Soundbanks\\"
    curr_voice = r"E:\tmp\bg3-modders-multitool\UnpackedMods\Voice\Mods\Gustav\Localization\English\Soundbanks\\"
    output_name = "voice"
    # find_different_files(last_voice, curr_voice, output_name)

    # compare_file_size(last_version, curr_version)
    # difference_of_existing_files(curr_version)
    # output_diff_voice(last_folder, curr_folder)
    # find_flag_by_word("gale")
    # lsj_path = rf"{base_path}\Gale\script\END_BrainBattle_CombatOver_Nested_AfterGithLeave.lsj"
    # find_flag_by_lsj(lsj_path)
    find_flagname_by_tag()
    char = "Minthara"
    # copy_wem_file_new_patch(char)
    char_list = ["Gale", "Minsc", "Raphael", "Halsin", "Shadowheart"]
    # for char in char_list:
    # find_lsj_by_wem(char)
    # char = "Shadowheart"
    # copy_lsj_to_script(char)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # generate_banter_files()
    # generate_other_files()
    # generate_char_script()
    # generate_spell_files()
    # generate_all_files()
    compare_new_patch()
    # tmp = "h13f7e675gdf5eg4f44g8489g4bc1538f5e2e"
    # print(generate_line_srt_by_filename(f"123_{tmp}.wem", True, True, {}))
