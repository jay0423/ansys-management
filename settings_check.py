import settings
import sys
import pprint


def os():
    if settings.OS == "mac" or settings.OS == "windows":
        pass
    else:
        print("error: settings.OS -> OS名が間違っています．")
        pprint.pprint(settings.OS)
        sys.exit()


def path_file_name():
    pass


def file_extension():
    pass


def abbrebiation():
    pass


def omission():
    pass


def dir_structure():
    pass


def base_path():
    pass


def base_file_name():
    pass


def write_extension():
    pass


def default_replace_word_dict():
    pass


def check_all():
    os()
    path_file_name()
    file_extension()
    abbrebiation()
    omission()
    dir_structure()
    base_path()
    base_file_name()
    write_extension()
    default_replace_word_dict()