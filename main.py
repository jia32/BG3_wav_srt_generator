import os
import json

pb_script_location1 = "\\Data\\Input\\PB_script\\companion_location"
pb_script_location2 = "\\Data\\Input\\PB_script\\companions"

voice_meta_location = "Input\\VoiceMeta"
voice_location = "E:\\tmp\\bg3-modders-multitool\\UnpackedData\\Voice\\Mods\\Gustav\\Localization\\English\\Soundbanks"

speaker = {
    "Gale": "ad9af97d-75da-406a-ae13-7071c563f604",
    "Laezel": "58a69333-40bf-8358-1d17-fff240d7fb12",
    "Wyll": "c774d764-4a17-48dc-b470-32ace9ce447d",
    "Astarion": "c7c13742-bacd-460a-8f65-f864fe41f255",
    "Shadowheart": "3ed74f06-3c60-42dc-83f6-f034cb47c679",
    "Halsin": "7628bc0e-52b8-42a7-856a-13a6fd413323",
    "Minthara": "25721313-0c15-4935-8176-9f134385451b",
    "Jaheira": "91b6b200-7d00-4d62-8dc9-99e8339dfa1a",
    "Karlach": "2c76687d-93a2-477b-8b18-8a14b549304c",
    "Minsc": "0de603c5-42e2-4811-9dad-f652de080eba",
} #LSString

def init_directory():
    """
    create a folder for each banter
    :return: list of banter name
    """
    pass


def generate_script():
    """
    create script for each banter, include content uid, .wem file name, uuid, children node info, speaker
    :return:
    """
    # Get the directory path of the current file
    current_directory = f"{os.path.dirname(os.path.abspath(__file__))}\\{pb_script_location2}"
    file_name_list = os.listdir(current_directory)
    # for file_name in file_name_list:
    file_name = "PB_Wyll_Gale_Potential.lsj"
    full_file_name = f"{current_directory}\\{file_name}"
    f = open(full_file_name, 'r')
    content = json.loads(f.read())
    output_json = {
        "speakerList":[]
    }
    print(content)


def copy_wem():
    """
    copy .wem file into its banter directory
    :return:
    """
    pass


def output_wav_subtitle():
    """
    concatenate audios and generate subtitle
    :return:
    """
    pass


def generate_banter_files():
    init_directory()
    generate_script()
    copy_wem()
    output_wav_subtitle()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    generate_banter_files()
