from models import *
import os
import shutil


def clean_folder(folder: str):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


if __name__ == "__main__":
    clean_folder("./frames")
    clean_folder("./output")
    a = Animation(144, 5, (1440, 1440), title="An animation")
    a.start()
