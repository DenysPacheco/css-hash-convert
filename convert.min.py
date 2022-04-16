

#################### Configurations ####################

config = {
    "filesSearch": [
        ".html",
        ".css"
    ],
    "filesIgnore": [
        ".min"
    ],
    "dirsIgnore": [
        ".",
        "packages",
        "src",
        "dist"
    ],
    "sufix": ".min",
    "prefix": "_",
    "patternCSS": "[\\.\\#]-?([_a-zA-Z]+[_a-zA-Z0-9-]*)\\s*\\{",
    "patternHTML": "class[\t]*=[\t]*\"[^\"]+",
    "patternCSSClear": "\\/\\*.*\\*\\/",
    "patternHTMLClear": "[^><a-zA-Z0-9\"',._-] ( *)|(<!--(.*?)-->)",
    "patternHTMLLinks": "(?<=<link).*(?<=href..)(?!http)(\\S+)(?=\"|\\')",
    "patternHTMLLinksAlt": "(?<=<link)(.href=\"|\\')(?!http)(\\S+)(?=\"|\\')",
    "patternHTMLHead": "<head>(?:.|\\n|\\r)+?</head>",
    "hashLength": 6,
    "overwriteFiles": True,
    "minimize": True,
    "console": True
}


#################### Functions ####################

import os
import json
import random
import re
from os.path import isfile, join
import string


def loadConfig():
    # Load config.json
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    _PATH = os.getcwd() + '/'

    return config, _PATH


config, _PATH = loadConfig()


def read(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        f.close()
    return lines


def write(root, new_name, lines):
    with open(os.path.join(root, new_name), 'w') as exf:
        exf.writelines(lines)
        exf.close()


def getVars(file):
    # Get the extension and use as a flag e.g.: HTML, CSS...
    type_file = file.split('.')[1].upper()

    lines = read(file)

    # Use the right regex to find the classes on the file
    classes_file = re.findall(config['pattern' + type_file], str(lines))

    name, ext = file.split('.')
    new_name = name + config['sufix'] + '.' + ext

    return new_name, classes_file


def lookFiles():
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


def getFiles(search_files, extension):
    type_files = [(root, file)
                  for root, file in search_files if file.endswith(extension)]

    return type_files


def cssHash(search_files):

    classes_dict = {}
    count = 0

    # Get all the files with the '.css' extension
    css_files = getFiles(search_files, '.css')

    # Copy the files of the search
    for root, file_name in css_files:
        lines = read(os.path.join(root, file_name))

        new_name, classes = getVars(os.path.join(root, file_name))

        # If the file doesn't exist, create a new one
        if(config['overwriteFiles'] or not isfile(join(root, new_name))):

            # Create the dictionary with the classe's hashes of the CSS
            for css_class in classes:
                name_hash_file = '-'.join([file_name, css_class])
                hash_number = ''

                for _ in range(config['hashLength']):
                    hash_number += str(''.join(random.choice(
                        string.ascii_uppercase + string.ascii_lowercase + string.digits)))

                    classes_dict.update({name_hash_file: hash_number})

            # CSS WRITE

            # Copy the hashes to the copied lines of the file
            for index, single_line in enumerate(lines):
                for key, value in classes_dict.items():
                    key = key.split('-', 1)[1]

                    if key in single_line:
                        single_line = single_line.replace(
                            key, config['prefix']+value)

                if(config['minimize']):
                    single_line = re.sub(
                        config['patternCSSClear'], '', str(single_line)).strip()
                    lines[index] = ''.join(single_line.split())
                else:
                    lines[index] = single_line

            write(root, new_name, lines)
            count += 1
            if(config['console']):
                print(f"{10*'*'} \t {new_name.split('/')[-1]} \t {10*'*'}")

        # If it exists, pass
        else:
            print(f'!! file already existed: {new_name}')

    return classes_dict, css_files, count


def htmlHash(search_files, classes_dict, css_files):

    count = 0

    # Overwrite HTML classes
    html_files = getFiles(search_files, '.html')

    # Copy the files of the search
    for root, file_name in html_files:
        lines = read(os.path.join(root, file_name))

        new_name, substring = getVars(os.path.join(root, file_name))

        # HTML WRITE

        # HTML overwrite link tags
        if(config['overwriteFiles'] or not isfile(join(root, new_name))):
            css_found = set()

            # Seach only the files (set) contained by the html
            for index, single_line in enumerate(lines):
                # look only the head lines - 'in' for minimized files
                if('</head>' in single_line):
                    break
                for root, css_file_name in css_files:
                    # if css_file_name in single_line and 'link' in single_line:
                    if css_file_name in single_line:

                        class_strip_name = re.findall(
                            config['patternHTMLLinks'], str(single_line))[0].split('/')[-1]

                        css_found.add(class_strip_name)

                        single_line = single_line.replace(
                            css_file_name, f"{css_file_name.split('.')[0]}{config['sufix']}.css")

                        lines[index] = single_line

            # Overwrite html lines with the hashed css classes
            for index, single_line in enumerate(lines):

                temp_dict = {}
                for key, value in classes_dict.items():

                    if key.split('-')[0] in css_found:
                        temp_dict.update({key: value})

                for key, value in temp_dict.items():

                    css_class = key.split('-', 1)[1]
                    if css_class in single_line:
                        single_line = single_line.replace(
                            css_class, config['prefix']+value)

                if(config['minimize']):
                    lines[index] = re.sub(
                        config['patternHTMLClear'], '', str(single_line)).strip()
                else:
                    lines[index] = single_line

            write(root, new_name, lines)
            count += 1
            if(config['console']):
                print(f"{10*'*'} \t {new_name.split('/')[-1]} \t {10*'*'}")

        # If it exists, pass
        else:
            print(f'!! file already existed: {new_name}')

    return count



#################### Converter ####################

import os
from functions import *

config, _PATH = loadConfig()

search_files = lookFiles()


def main():
    search_files = lookFiles()

    if(config['console']):

        #print(f'files: {search_files}\n')

        print('CSS Hashfy found files:', end='\n\n')
        for root, file in search_files:
            print(os.path.join(root, file))
        print()

        print('Starting hashing...', end='\n\n')

    # Initializing alg vars
    classes_dict, css_files, css_count = cssHash(search_files)

    html_count = htmlHash(search_files, classes_dict, css_files)

    if(config['console']):

        print()
        print(
            f'finished! {str(int((html_count + css_count)/len(search_files))*100)}% done.')


################ Main ################

main()


