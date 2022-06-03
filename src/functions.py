import json
import sys
import os
import random
import re
import string
from os.path import isfile, join


def loadConfig():
    """Load initial configurations of the json file.

    Returns:
        tuple: (config, _PATH)
                - config (dict): the vars of configurations
                - _PATH (string): string of the root path
    """

    # Side tweak to fix file path for testing (and running script and build docs)
    if 'test' in os.path.basename(sys.path[0]):
        _localdir = os.path.dirname(sys.path[0]) + '/src'
    else:
        _localdir = sys.path[0]

    # if there is no config file (then it's .min), get the global config var
    if not os.path.exists(_localdir + '/config.json'):
        global config
    else:
        # Load config.json
        with open(f"{_localdir}/config.json") as json_data_file:
            config = json.load(json_data_file)

    # Configure the PATH arg to run the script on
    if config["dirsSearch"]:
        _PATH = os.getcwd() + "/" + str(config["dirsSearch"][0]) + "/"
    else:
        _PATH = os.getcwd() + "/"

    return config, _PATH


config, _PATH = loadConfig()


def read(file):
    """Basic functions to read contents of files.

    Args:
        file (string): path of the file

    Returns:
        list: lines of the file
    """
    with open(file, "r") as f:
        lines = f.readlines()
        f.close()
    return lines


def write(root, new_name, lines):
    """Basic funtions to write in a file.

    Args:
        root (string): path of the root for the file
        new_name (string): new name of the file
        lines (list): list of the string to write
    """
    with open(os.path.join(root, new_name), "w") as exf:
        exf.writelines(lines)
        exf.close()


def getVars(file):
    """Get and prepare the vars to use for a single file;
    Being the name, extension, new name and content (based on the proper regex) on the file.

    Args:
        file (string): path to the file

    Returns:
        tuple: (new_name, classes_file)
                - new_name (string): the new name with the minifier extension
                - classes_file (list): the content of the file extracted from the regex
    """
    # Get the extension and use as a flag e.g.: HTML, CSS...
    type_file = file.split(".")[1].upper()

    lines = read(file)

    # Use the right regex to find the classes on the file
    classes_file = re.findall(config["pattern" + type_file], str(lines))

    name, ext = file.split(".")
    new_name = name + config["sufix"] + "." + ext

    return new_name, classes_file


def lookFiles():
    """Look for the files to convert. Find all files with matching extensions out of config.json

     - Use _PATH as the root.
     - Ignore the dirs as specified in config['dirsIgnore']
     - Select files with extensions as specified in config['filesSearch']
     - Ignore files with extensions as specified in config['filesIgnore']

    Returns:
        list: list of tuples [(root, file)] of all the files founded (given the extension on config.json)
    """
    search_files = []
    # Look for files
    for root, subdirectories, files in os.walk(_PATH):
        # Comprehension to break outter loop
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
        extension (string): extension type

    Returns:
        list: list of tuples [(root, file)] of the selected extension
                - root (string): root path for the file (without the filename) 
                - file (string): filename
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

            # Create the dictionary with the classe's hashes of the CSS
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
                print(f"{10*'*'} \t {new_name.split('/')[-1]} \t {10*'*'}")

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

            # Seach only the files (set) contained by the html
            for index, single_line in enumerate(lines):
                # look only the head lines - 'in' for minimized files
                if "</head>" in single_line:
                    break
                for root, css_file_name in css_files:
                    # if css_file_name in single_line and 'link' in single_line:
                    if css_file_name in single_line:

                        class_strip_name = re.findall(
                            config["patternHTMLLinks"], str(single_line)
                        )[0].split("/")[-1]

                        css_found.add(class_strip_name)

                        single_line = single_line.replace(
                            css_file_name,
                            f"{css_file_name.split('.')[0]}{config['sufix']}.css",
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
