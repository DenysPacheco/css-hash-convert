import os
from functions import *

config, _PATH = loadconfig()

search_files = lookfiles()


def main():
    search_files = lookfiles()

    if(config['output']):

        #print(f'files: {search_files}\n')

        print('CSS Hashfy found files:', end='\n\n')
        for root, file in search_files:
            print(os.path.join(root, file))
        print()

        print('Starting hashing...', end='\n\n')

    # Initializing alg vars
    classes_dict, css_files, css_count = csshash(search_files)

    html_count = htmlhash(search_files, classes_dict, css_files)

    if(config['output']):

        print()
        print(
            f'finished! {str(int((html_count + css_count)/len(search_files))*100)}% done.')


main()
