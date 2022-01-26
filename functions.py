import os
import json
import re
from os.path import isfile, join


def loadconfig():
    # Load config.json
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    _PATH = os.getcwd() + '/'

    return config, _PATH


config, _PATH = loadconfig()


def read(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        f.close()
    return lines


def write(root, new_name, lines):
    with open(os.path.join(root, new_name), 'w') as exf:
        exf.writelines(lines)
        exf.close()


def getvars(file):
    # Get the extension and use as a flag e.g.: HTML, CSS...
    pattern_file = file.split('.')[1].upper()

    lines = read(file)

    # Use the right regex to find the classes on the file
    substring = re.findall(config['pattern' + pattern_file], str(lines))

    name, ext = file.split('.')
    new_name = name + config['extCopy'] + '.' + ext

    return new_name, substring


def lookfiles():
    search_files = []
    # Look for files
    for root, subdirectories, files in os.walk(_PATH):
        # Comprehension to break outter loop
        if any([dirsIgnore for dirsIgnore in config['dirsIgnore'] if dirsIgnore in root]):
            continue

        # And all its files
        for index, file in enumerate(files):
            for filesSearch in config['filesSearch']:
                for filesIgnore in config['filesIgnore']:
                    if(filesSearch in file and filesIgnore not in file):
                        search_files.append((root, file))

    return search_files


def csshash(search_files):

    classes_dict = {}
    count = 0

    # Get all the files with the '.css' extension
    css_files = [(root, file)
                 for root, file in search_files if file.endswith('.css')]

    # Copy the files of the search
    for root, file in css_files:
        lines = read(os.path.join(root, file))

        new_name, substring = getvars(os.path.join(root, file))

        # If the file doesn't exist, create a new one
        if(config['overwriteFiles'] or not isfile(join(root, new_name))):

            # Create the dictionary with the classe's hashes of the CSS
            classes_dict.update(
                {s: str(abs(hash(s)) % (10 ** config['hashLength'])) for s in substring})

            # CSS WRITE

            # Copy the hashes to the copied lines of the file
            for index, l in enumerate(lines):
                for k, v in classes_dict.items():
                    if k in l:
                        l = l.replace(k, 'c'+v)
                if(config['minimize']):
                    lines[index] = ''.join(l.split())
                else:
                    lines[index] = l

            write(root, new_name, lines)
            count += 1
            if(config['output']):
                print(f"{10*'*'} \t {new_name.split('/')[-1]} \t {10*'*'}")

        # If it exists, pass
        else:
            print(f'!! file already existed: {new_name}')

    return classes_dict, css_files, count


def htmlhash(search_files, classes_dict, css_files):

    count = 0

    # Overwrite HTML classes
    html_files = [(root, file)
                  for root, file in search_files if file.endswith('.html')]

    # Copy the files of the search
    for root, file in html_files:
        lines = read(os.path.join(root, file))

        new_name, substring = getvars(os.path.join(root, file))

        # HTML WRITE

        # HTML overwrite link tags
        if(config['overwriteFiles'] or not isfile(join(root, new_name))):
            for index, l in enumerate(lines):
                for root, file in css_files:
                    if file in l and 'link' in l:
                        l = l.replace(
                            file, f"{file.split('.')[0]}{config['extCopy']}.css")
                lines[index] = l

            # Overwrite html lines with the hashed css classes
            for index, l in enumerate(lines):
                for k, v in classes_dict.items():
                    if k in l:
                        l = l.replace(k, 'c'+v)
                if(config['minimize']):
                    lines[index] = ''.join(l.split())
                else:
                    lines[index] = l

            write(root, new_name, lines)
            count += 1
            if(config['output']):
                print(f"{10*'*'} \t {new_name.split('/')[-1]} \t {10*'*'}")

        # If it exists, pass
        else:
            print(f'!! file already existed: {new_name}')

    return count
