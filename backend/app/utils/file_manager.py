#backend/app/utils/fil e_manager.py
import os


def save_file(file, path):

    folder = os.path.dirname(path)

    if not os.path.exists(folder):
        os.makedirs(folder)

    file.save(path)