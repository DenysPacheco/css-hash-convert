# Css Hashfy Minify Converter ♻️

This is a **Python** script to **hashfy** & **minify** css classes.

It was inspired on Google's approach to minimize class names for faster loading web pages. 

(Plus a few things that I would like to see together on the same place)

## 😄 What it does

- [x] Make a hash out of css and id classes
- [x] Make a random hash each run
- [x] Minify your css
- [x] Remove comments
- [x] Auto apply changes for all the html files
- [x] Create `.min` sufixed file with the output
- [x] Auto change the css file names to `.min` in the html link tag
- [x] Multiple files on multiple folders (top-down) ✨

## 📘 Usage

Just put these files on the top folder and execute `convert.py`.

- [convert.py](convert.py) 
- [functions.py](functions.py) 
- [config.json](config.json)

It will search all files with the extensions marked on the configuration file. (default .html and .css)

It will give the output with `foo.min.html` and `foo.min.css`.

### ⚙️ Configure

Change in the [configuration file](/config.json) the directories to be ignored, hash length and overwrite files.

Configurations options:

- directories to ignore
- prefix of css classes
- sufix of files
- hash length
- overwrite files
- minimize
- console output

**Mind that: if `overwrite: false`, the hash will not be equal to the old files; therefore: not in sync; therefore: 👋 bye bye css.**

## 🤔 What to come

- [ ] How about js too?
- [ ] Obfuscate everything?
