from functions import cssHash, htmlHash, loadConfig, lookFiles
import os

config, _PATH = loadConfig()

search_files = lookFiles()


def main():
    """Main function to run the script.
    More details explained on the `functions` docs
    """

    search_files = lookFiles()

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
    main()
