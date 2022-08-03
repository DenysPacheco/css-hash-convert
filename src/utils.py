import json
import sys
import os
import random
import re
import string
from os.path import isfile, join


def confirmPath(path):
    """Confirm if a path is a valid directory path.

    Args:
        path (str): path to dir

    Raises:
        OSError: if path is not dir or does not exists

    Returns:
        string: the same path, if valid
    """

    if not os.path.isdir(path):
        raise OSError(
            f'{path}: Path is not a directory path or it does not exists.')

    return path


def confirmFile(path):
    """Confirm if a path is a valid file path.

    Args:
        path (str): path to file

    Raises:
        OSError: if path is not file or does not exists

    Returns:
        str: the same path, if valid
    """

    if not os.path.isfile(path):
        raise OSError(
            f'{path}: Path is not a file path or it does not exists.')

    return path


def loadConfig():
    """Initialize the config.json file and config var

    Returns:
        dict: config dictionary
    """

    # Side tweak to fix file path for testing (and running script and build docs)
    if not 'src' == os.path.basename(sys.path[0]):
        _localdir = os.path.join(sys.path[0], 'src')
    else:
        _localdir = sys.path[0]

    # if there is no config file (then it's .min), get the global config var for converter.min.py
    if not os.path.exists(os.path.join(_localdir, 'config.json')):
        global config
    else:
        # Load config.json
        with open(f"{os.path.join(_localdir, 'config.json')}") as json_data_file:
            config = json.load(json_data_file)
            return config


def loadPath(path=''):
    """Loads the PATH to the dir with the files to convert

    Args:
        path (str, optional): path of the dir (in config.json defaults to 'examples'). Defaults to ''.

    Returns:
        str: the path of the dir to convert the files
    """

    # Doesn't need load for the config in main loads in the global scope
    # But it does have to put on the tests
    config = loadConfig()

    if path:
        _PATH = confirmPath(path)
    else:

        # Configure the PATH arg to run the script on
        if config["dirsSearch"]:
            _PATH = os.path.join(os.getcwd(), str(config["dirsSearch"][0]))
        else:
            _PATH = os.getcwd()

    return _PATH


def read(file):
    """Basic functions to read contents of files.

    Args:
        file (str): path of the file

    Returns:
        list: lines of the file
    """

    if confirmFile(file):
        with open(file, "r") as f:
            lines = f.readlines()
            f.close()
        return lines


def write(root, new_name, lines):
    """Basic functions to write in a file.

    Args:
        root (str): path of the root for the file
        new_name (str): new name of the file
        lines (list): list of the string to write
    """

    if confirmPath(root):
        with open(os.path.join(root, new_name), "w") as exf:
            exf.writelines(lines)
            exf.close()


def getVars(file):
    """Get and prepare the vars to use for a single file;
    Being the name, extension, new name and content (based on the proper regex) on the file.

    Args:
        file (str): path to the file

    Returns:
        tuple: (new_name, classes_file)
                - new_name (str): the new name with the minifier extension
                - classes_file (list): the content of the file extracted from the regex
    """

    if confirmFile(file):

        # Get the extension and use as a flag e.g.: HTML, CSS...
        ext = os.path.splitext(file)[1].replace('.', '')
        filename = os.path.basename(file)
        onlyName = filename.split('.')[0]
        type_file = ext.upper()

        lines = read(file)

        # Use the right regex to find the classes on the file
        classes_file = re.findall(config["pattern" + type_file], str(lines))

        if not '.min' in filename:
            new_name = onlyName + config["suffix"] + '.' + ext
        else:
            raise Exception(f'file: {filename} is a .min file')

        return new_name, classes_file


def lookFiles(path):
    """Look for the files to convert. Find all files with matching extensions out of config.json

        - Use _PATH as the root.
        - Ignore the dirs as specified in config['dirsIgnore']
        - Select files with extensions as specified in config['filesSearch']
        - Ignore files with extensions as specified in config['filesIgnore']

    Args:
        path (str): path to convert the files

    Returns:
        list: list of tuples [(root, file)] of all the files founded (given the extension on config.json)
    """

    _PATH = confirmPath(path)

    search_files = []
    # Look for files
    for root, subdirectories, files in os.walk(_PATH):
        # Comprehension to break outer loop
        if any(
            [dirsIgnore for dirsIgnore in config["dirsIgnore"] if dirsIgnore in root]
        ):
            continue

        # And all its files
        for index, file in enumerate(files):
            for filesSearch in config["filesSearch"]:
                for filesIgnore in config["filesIgnore"]:
                    if filesSearch in file and filesIgnore not in file:
                        search_files.append((root, file))

    return search_files


def getFiles(search_files, extension):
    """Get the list of files, separate and filter them by the extension and returns a tuple of (root, file)

    Args:
        search_files (list): list of all files searched
        extension (str): extension type

    Returns:
        list: list of tuples [(root, file)] of the selected extension
                - root (str): root path for the file (without the filename) 
                - file (str): filename
    """

    type_files = [
        (root, file) for root, file in search_files if file.endswith(extension)
    ]

    return type_files


def cssHash(search_files):
    """Hash the css classes and return a tuple

    Args:
        search_files (list): list of all files founded

    Returns:
        tuple: (classes_dict, css_files, count)
                - classes_dict (list): list of dicts ({class: hashed}) of the hashed css classes
                - css_files (list): list of tuples ([(root, file)]) of css files
                - count (int): counter of the files altered
    """

    classes_dict = {}
    count = 0

    # Get all the files with the '.css' extension
    css_files = getFiles(search_files, ".css")

    # Copy the files of the search
    for root, file_name in css_files:
        lines = read(os.path.join(root, file_name))

        new_name, classes = getVars(os.path.join(root, file_name))

        # If the file doesn't exist, create a new one
        if config["overwriteFiles"] or not isfile(join(root, new_name)):

            # Create the dictionary with the classes hashes of the CSS
            for css_class in classes:
                name_hash_file = "-".join([file_name, css_class])
                hash_number = ""

                for _ in range(config["hashLength"]):
                    hash_number += str(
                        "".join(
                            random.choice(
                                string.ascii_uppercase
                                + string.ascii_lowercase
                                + string.digits
                            )
                        )
                    )

                    classes_dict.update({name_hash_file: hash_number})

            # CSS WRITE

            # Copy the hashes to the copied lines of the file
            for index, single_line in enumerate(lines):
                for key, value in classes_dict.items():
                    key = key.split("-", 1)[1]

                    if key in single_line:
                        single_line = single_line.replace(
                            key, config["prefix"] + value)

                if config["minimize"]:
                    single_line = re.sub(
                        config["patternCSSClear"], "", str(single_line)
                    ).strip()
                    lines[index] = "".join(single_line.split())
                else:
                    lines[index] = single_line

            write(root, new_name, lines)
            count += 1
            if config["console"]:
                print(f"{10*'*'} \t {new_name.split('/')[-1]}   \t {10*'*'}")

        # If it exists, pass
        else:
            print(f"!! file already existed: {new_name}")

    return classes_dict, css_files, count


def htmlHash(search_files, classes_dict, css_files):
    """Hash the html files and return a count of files altered

    Args:
        search_files (list): list of all files founded
        classes_dict (list): list of dicts ({class: hashed}) of the hashed css classes
        css_files (list): list of tuples ([(root, file)]) of css files

    Returns:
        int: count of the html files altered
    """

    count = 0

    # Overwrite HTML classes
    html_files = getFiles(search_files, ".html")

    # Copy the files of the search
    for root, file_name in html_files:
        lines = read(os.path.join(root, file_name))

        new_name, substring = getVars(os.path.join(root, file_name))

        # HTML WRITE

        # HTML overwrite link tags
        if config["overwriteFiles"] or not isfile(join(root, new_name)):
            css_found = set()

            # Search only the files (set) contained by the html
            for index, single_line in enumerate(lines):
                # look only the head lines - 'in' for minimized files
                if "</head>" in single_line:
                    break
                for _, css_file_name in css_files:
                    # if css_file_name in single_line and 'link' in single_line:
                    if css_file_name in single_line:

                        class_strip_name = re.findall(
                            config["patternHTMLLinks"], str(single_line)
                        )[0].split("/")[-1]

                        css_found.add(class_strip_name)

                        single_line = single_line.replace(
                            css_file_name,
                            f"{css_file_name.split('.')[0]}{config['suffix']}.css",
                        )

                        lines[index] = single_line

            # Overwrite html lines with the hashed css classes
            for index, single_line in enumerate(lines):

                temp_dict = {}
                for key, value in classes_dict.items():

                    if key.split("-")[0] in css_found:
                        temp_dict.update({key: value})

                for key, value in temp_dict.items():

                    css_class = key.split("-", 1)[1]
                    if css_class in single_line:
                        single_line = single_line.replace(
                            css_class, config["prefix"] + value
                        )

                if config["minimize"]:
                    lines[index] = re.sub(
                        config["patternHTMLClear"], "", str(single_line)
                    ).strip()
                else:
                    lines[index] = single_line

            write(root, new_name, lines)
            count += 1
            if config["console"]:
                print(f"{10*'*'} \t {new_name.split('/')[-1]} \t {10*'*'}")

        # If it exists, pass
        else:
            print(f"!! file already existed: {new_name}")

    return count
