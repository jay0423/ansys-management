import shutil
import os

shutil.copy('ansys_management/start/ansys_management.txt', './ansys_management.py')
shutil.copy('ansys_management/start/settings_child.txt', './settings_child.py')
shutil.copy('ansys_management/start/path.xlsx', './path.xlsx')

if not os.path.isfile("./abbreviation.json"):
    shutil.copy('ansys_management/start/abbreviation.json', './abbreviation.json')