import os
import json
import re
from os import listdir
from os.path import isfile, join

def read(file):
    with open(file, 'r') as f:
            lines = f.readlines()
            f.close()
    return lines


def write(_PATH, new_name, lines):
    with open(_PATH + new_name, 'w') as exf:
        exf.writelines(lines)
        exf.close()


def getVars(file, config):
    # Get the extension and use as a flag e.g.: HTML, CSS...
    pattern_file = file.split('.')[1].upper()

    lines = read(file)

    # Use the right regex to find the classes on the file
    substring = re.findall(config['pattern' + pattern_file], str(lines))

    name, ext = file.split('.')
    new_name = name + config['extCopy'] + '.' + ext

    return new_name, substring


def main():
    # Load config.json
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    _PATH = os.getcwd() + '/'

    # Look for files
    search_files = [f for f in listdir(_PATH) if isfile(join(_PATH, f)) and [bool(
        s) for s in config['filesSearch'] if f.endswith(s)] and [bool(i) for i in config['filesIgnore'] if i not in f]]

    print(f'files: {search_files}\n')

    # Initializing alg vars
    count = 0
    classes_dict = {}

    # Get all the files with the '.css' extension
    css_files = [file for file in search_files if '.css' in file]

    # Copy the files of the search
    for file in css_files:
        lines = read(file)

        new_name, substring = getVars(file, config)

        # If the file doesn't exist, create a new one
        if(not isfile(join(_PATH, new_name))):
            substring = [s.translate({ord('.'): None, ord(
                '{'): None}).strip() for s in substring]

            # Create the dictionary with the classe's hashes of the CSS
            classes_dict.update(
                {s: str(abs(hash(s)) % (10 ** config['hashLength'])) for s in substring})

            # CSS WRITE

            # Copy the hashes to the copied lines of the file
            for index, l in enumerate(lines):
                for k, v in classes_dict.items():
                    if k in l:
                        l = l.replace(k, 'c'+v)
                lines[index] = l

            write(_PATH, new_name, lines)
            count += 1
            print(f"{10*'*'} \t {new_name} \t {10*'*'}")

        # If it exists, pass
        else:
            print(f'!! file {new_name} already existed! !!')

    # Overwrite HTML classes
    html_files = [file for file in search_files if '.html' in file]

    # Copy the files of the search
    for file in html_files:
        lines = read(file)

        new_name, substring = getVars(file, config)

        # HTML WRITE

        # HTML overwrite link tags
        if(not isfile(join(_PATH, new_name))):
            for index, l in enumerate(lines):
                for file in css_files:
                    if file in l and 'link' in l:
                        l = l.replace(
                            file, f"{file.split('.')[0]}{config['extCopy']}.css")
                lines[index] = l

            # Overwrite html lines with the hashed css classes
            for index, l in enumerate(lines):
                for k, v in classes_dict.items():
                    if k in l:
                        l = l.replace(k, 'c'+v)
                lines[index] = l

            write(_PATH, new_name, lines)
            count += 1
            print(f"{10*'*'} \t {new_name} \t {10*'*'}")

        # If it exists, pass
        else:
            print(f'!! file {new_name} already existed! !!')

    print()
    print(f'finished! {str(int(count/len(search_files))*100)}% done.')


main()
