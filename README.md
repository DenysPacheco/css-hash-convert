# Css Hashfy Minify Converter ♻️

This is a **Python** script to **hashfy** & **minify** css classes and html tags.

It was inspired on Google's approach to minimize class names for faster loading web pages and a *bit of my ideas*.

(Plus a few things that I would like to see together on the same place)

## 😄 What it does

- [x] Make a random hash **each run** out of css and id classes
- [x] Minify your css and html
- [x] Remove comments 👌
- [x] Create `.min` sufixed file with the output
- [x] Auto apply changes for all the html files (class sub and style link tags)
- [x] Multiple files on multiple folders (top-down) ✨

## 📘 Usage

Just put these files on the most top folder and execute.

- Use [convert.min.py](convert.min.py) that has all it's needed to run alone.

Alternatively...

- [convert.py](convert.py) (main)
- [functions.py](functions.py)
- [config.json](config.json)



It will search all files with the extensions marked on the [configuration file](config.json) and do the changes. (default `.html` and `.css`)

It will give the output with `foo.min.html` and `foo.min.css`.

## ⚙️ Configure

Change in the [configuration file](/config.json) the directories to be ignored, hash length, overwrite files and others. (On the [convert.min.py](convert.min.py) the configurations are in the beggining of the file)

### Configurations options:

- files to search
- files to ignore
- directories to ignore
- sufix (of files)
- prefix (of hashed classes)
- Regex of css
- Regex of html
- Regex of remove comments css
- Regex of remove comments html_count
- hash length
- overwrite files
- minimize
- console output

**Mind that: if `overwrite: false`, the hash will not be equal to the old files; therefore: not in sync; therefore: 👋 bye bye css.**

## 🤔 What to come

- [ ] How about js too?
- [ ] Obfuscate everything?
