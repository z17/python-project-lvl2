import os


def get_file_data(file_path: str):
    with open(file_path) as file:
        name, extension = os.path.splitext(file.name)
        return file.read(), standardize_extension(extension)


def standardize_extension(extension: str):
    extension = extension.lower()
    if extension.startswith('.'):
        return extension[1:]
    return extension
