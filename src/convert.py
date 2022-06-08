from utils import cssHash, htmlHash, loadConfig, loadPath, lookFiles

import os
import sys


def main(args):
    """Main function to run the script.
    More details explained on the `functions` docs
    """

    # Load config before path for the global variable scope
    config = loadConfig()

    if args:
        _PATH = loadPath(args[0])
    else:
        _PATH = loadPath()

    _PATH = os.path.realpath(_PATH)

    search_files = lookFiles(_PATH)

    if search_files:

        if config["console"]:

            # print(f'files: {search_files}\n')

            print("CSS Hashfy found files:", end="\n\n")
            for root, file in search_files:
                print(os.path.join(root, file))
            print()

            print("Starting hashing...", end="\n\n")

        # Initializing algo vars
        classes_dict, css_files, css_count = cssHash(search_files)

        html_count = htmlHash(search_files, classes_dict, css_files)

        if config["console"]:

            print()
            print(
                f"finished! {str(int((html_count + css_count)/len(search_files))*100)}% done."
            )

    else:
        print("!!! No files found!")


################ Main ################

if __name__ == "__main__":
    main(sys.argv[1:])
