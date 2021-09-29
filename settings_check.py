import settings
import sys
import pprint



def dir_ignore():
    pass


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


def py_dir_path():
    if settings.PY_DIR_PATH[-1] == "/" or settings.PY_DIR_PATH[-1] == "\ ".replace(" ", ""):
        pass
    elif settings.PY_DIR_PATH == "":
        pass
    else:
        print("error: settings.PY_DIR_PATH -> パスの最後にスラッシュをつけてください．")
        pprint.pprint(settings.PY_DIR_PATH)
        sys.exit()


def check_all():
    path_file_name()
    file_extension()
    abbrebiation()
    omission()
    dir_structure()
    base_path()
    base_file_name()
    write_extension()
    default_replace_word_dict()
    py_dir_path()