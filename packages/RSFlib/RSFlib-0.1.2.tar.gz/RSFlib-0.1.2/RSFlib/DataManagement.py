''' Methods for data management '''
import os


def fileName(path):
    ''' method that takes path as input and returns unique path if input
    path already exist (prevent data unique data overwrite) '''
    name, suffix = os.path.splitext(path)
    num = ""
    while True:
        new_path = f"{name}{num}{suffix}"
        if not os.path.exists(new_path):
            break
        if num == "":
            num = -1
        num += 1
    return new_path
