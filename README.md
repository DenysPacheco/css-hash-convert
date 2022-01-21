# Css Hashfy Converter

This is a python script to hashfy css classes.
It was inspired on Google's approach to minimize classes names to faster load web pages.

## What it does

- [x] Make a hash out of css and id classes
- [x] Auto apply for all the html files
- [x] Create `-hashed` file with the output
- [x] Auto change the css file to `-hashed` in the html link tag
- [x] Multiple files on multiple folders

## Usage

Just put the script/files on the top folder and execute.

It will search all files with the extensions marked on the configuration file.

It will give the output with `foo-hashed.html` and `foo-hashed.css`.

### Configure

Change in the [configuration file](/config.json) the directories to be ignored, hash length and overwrite files.

## To Change?

- [ ] Separation of classes and ids in prefix
