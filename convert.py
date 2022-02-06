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


main()
