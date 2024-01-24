from party_banter import *
from in_world_voice import *
from spell import *
from all_voice import *
from single_lsj import generate_other_script
from constant import base_path
from patch_diff import *


def generate_spell_files(char):
    # dont run top 2
    # collect_spell_files()
    # print_spell()
    # csv_to_json(spell_out_csv, spell_with_ch)

    # start from here
    # copy_wem_by_school()
    # char = "Halsin"
    copy_spell_wem_by_ch(char)

    # update tmp_order with output from previous step
    # organize_by_companion()

    generate_spell_audio(char)
    # convert_dds_to_png()


def generate_char_script(char, job_name):
    # write_output_json(char_ori, char_final)
    # char = "Shadowheart"
    script_location = rf"{base_path}{char}\script\\"

    # for root, dirs, job_list in os.walk(script_location):
    # job_list = os.listdir(script_location)
    job_list =["WYR_KillDirectorGortash_Gortash_Dead"]
    for job in job_list:
        # if ".lsj" in job:
        job_name = job #[:-4]
        print(job_name)
        # job_list = ['GLO_PAD_CombatReact_PartyDeath', 'GLO_BG_PointNClick_GenericOrigin_NarrativeArc_Start']
        # job_name = "CAMP_MinscJaheira_PAD_PostReunion"

        # for job_name in job_list:
        filename = f"{job_name}.lsj"

        # print_dialog_txt()

        # target_folder = rf"{base_path}\Orin\scripts\imposter_npc\\"
        dict_path = rf"{script_location}file_name_dict.json"
        current_target_path = rf"{script_location}\wem\{job_name}\\"

        # script_path = rf"{base_path}\Orin\scripts\{job_name}\\"
        script_txt = f"{script_location}{job_name}.txt"
        wav_path = rf"{script_location}\wav\\"
        # job_name = "final_order"
        # script_txt = rf"{script_location}final_order.json"

        # create_dialog_txt(script_location, filename)
        # create_dialog_txt_only(script_location)
        # Optional operations:
        # generate_partial_final_txt(script_location, "roman")

        # double_check_file_order(script_location)
        # for i in range(1, 94):
        #     tmp_txt = rf"{script_location}\{i}.txt"
        copy_audio_wem(script_txt, current_target_path)
        #     script_txt = rf"{script_location}sneak.json"
        # script_txt = rf"{script_location}final_order.json"
        # generate_srt_for_translations(script_location, script_txt, dict_path, job_name)
        # check_translation(script_location)

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


def generate_all_files(char):
    # char_list = ['Shadowheart']
    # char = "Tav/Durge voice 5"
    # copy_all_wem(char)
    # distinguish_audio(char)
    combine_char_audio(char)
    #
    path = f"{char}\\wav"
    # combine_audio_only(path, 1, 1000)
    # combine_audio(char, 2, 1000)
    # combine_audio(char, 3, 1000)
    #
    # combine_audio(char, 4, 1000)
    # combine_audio(char, 5, 1000)
    # combine_audio(char, 6, 1000)
    # combine_audio(char, 7, 1000)
    # combine_audio(char, 8, 1000)


def compare_new_patch():
    last_version = r"\text\Dialogs-patch4\\"
    curr_version = r"\text\Dialogs-patch5\\"

    output_name = "voice"
    # find_different_files(last_voice, curr_voice, output_name)

    # compare_file_size(last_version, curr_version)
    # difference_of_existing_files(curr_version)
    # find_different_files(last_voice, curr_voice)
    find_flag_by_word("RARE")
    # lsj_path = rf"{base_path}\Gale\script\END_BrainBattle_CombatOver_Nested_AfterGithLeave.lsj"
    # find_flag_by_lsj(lsj_path)
    # tag_list = ['RARE']
    # find_flagname_by_tag(tag_list)
    # char = "Minsc"
    # copy_wem_file_new_patch(char)
    char_list = ["Gale", "Minsc", "Raphael", "Halsin", "Shadowheart"]
    # for char in char_list:
    char = "MonkAmulet"
    # find_lsj_by_wem(char)
    # char = "Shadowheart"
    # copy_lsj_to_script(char)

    # hotfix16_english_filepath = "/Data/Input/english.hotfix16.loca.xml"
    # hotfix17_english_filepath ="/Data/Input/english.hotfix.17.xml"
    # compare_xml(f"{os.path.dirname(os.path.abspath(__file__))}\\{hotfix16_english_filepath}",f"{os.path.dirname(os.path.abspath(__file__))}\\{hotfix17_english_filepath}" )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # char_name = "Jaheira"
    # generate_banter_files()
    # generate_other_files()
    generate_char_script("Gortash", "WYR_KillDirectorGortash_Gortash_Dead")
    # generate_line_srt_by_filename(filename, with_name, with_ch, translation_json):

    # char_list = ["Raphael"]
    # for char_name in char_list:
    #     generate_all_files(char_name)
    # combine_audio_only("narrator\\all", 1, 1000)

    # char_list = ["Astarion", "Wyll"]
    # for char_name in char_list:
    #     generate_spell_files(char_name)

    # compare_new_patch()
    # tmp = "h13f7e675gdf5eg4f44g8489g4bc1538f5e2e"
    # print(generate_line_srt_by_filename(f"123_{tmp}.wem", True, True, {}))

    # find_lsj_ch_keyword("Gale", "damn you", "Gale says damn you")
    # from_srt_to_txt(srt_path, txt_path)
