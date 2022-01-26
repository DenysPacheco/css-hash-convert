# Css Hashfy Minify Converter

This is a python script to hashfy css classes.
It was inspired on Google's approach to minimize classes names to faster load web pages.

## What it does

- [x] Make a hash out of css and id classes
- [x] Make a random hash each run
- [x] Minify your css
- [x] Auto apply for all the html files
- [x] Create `-hashed` file with the output
- [x] Auto change the css file names to `-hashed` in the html link tag
- [x] Multiple files on multiple folders (top-down)

## Usage

Just put the script/files on the top folder and execute.

It will search all files with the extensions marked on the configuration file.

It will give the output with `foo-hashed.html` and `foo-hashed.css`.


### Configure

Change in the [configuration file](/config.json) the directories to be ignored, hash length and overwrite files.

**Mind that: if `overwrite` is `false` the hash will not be equal to the old files, therefore not in sync.**

## What to come

- [ ] Obfuscate everything?
- [ ] How about js too?
