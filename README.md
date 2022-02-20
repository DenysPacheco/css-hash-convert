
# Css Hashfy & Minify Converter ♻️

This is a **Python** script to **hashfy & minify** css classes and html tags.

It was inspired on Google's approach to minimize class names for faster loading web pages and a *bit of my ideas*.

(Plus a few things that I would like to see together on the same place)

## Contents

- [Css Hashfy & Minify Converter ♻️](#css-hashfy--minify-converter-️)
  - [Contents](#contents)
  - [😄 What it does](#-what-it-does)
  - [📘 Usage](#-usage)
  - [⚙️ Configure](#️-configure)
    - [Configuration options](#configuration-options)
      - [overwrite note](#overwrite-note)
  - [🤔 What to come](#-what-to-come)

## 😄 What it does

- [x] Make a random hash **each run** out of css and id classes (see [overwrite](#overwrite-note))
- [x] Minify css and html files
- [x] Remove comments 👌
- [x] Create `.min` sufixed files as output
- [x] Auto apply changes for all the html files (class subst and style link tags)
- [x] Multiple files on multiple folders (top-down) ✨

## 📘 Usage

Just put these files on the most top folder and execute.

- Use [convert.min.py](convert.min.py) that has all it needs to run alone.

Alternatively...

- [convert.py](convert.py) (`main`)
- [functions.py](functions.py)
- [config.json](config.json)

It will search for all the files with the matching extensions marked on the [configuration file](config.json) and do the changes. (default `.html` and `.css`)

It will give the output with `foo.min.html` and `foo.min.css` on the same directorie as the original ones.

## ⚙️ Configure

Change in the [configuration file](/config.json) the directories to be ignored, hash length, overwrite files and others. (On the [convert.min.py](convert.min.py) the configurations are in the beggining of the file)

### Configuration options

| Flags            | Meaning                                  |
| ---------------- | ---------------------------------------- |
| filesSearch      | Extensions of the files to search        |
| filesIgnore      | Extensions of the files to ignore        |
| dirsIgnore       | Directories to ignore on the search      |
| sufix            | Sufix of the outputed files              |
| prefix           | Prefix of the css classes                |
| patternCSS       | Regex of the css to take classes and ids |
| patternHTML      | Regex of the html to take the classes    |
| patternCSSClear  | Regex to remove the css comments         |
| patternHTMLClear | Regex to remove the html comments        |
| hashLength       | Lenght of the hash                       |
| overwriteFiles   | Overwrite the output files               |
| minimize         | Minimize the files                       |
| console          | Print console output                     |

#### overwrite note

> **Mind that: if `overwrite: false`, the css hash will not be equal to the old html files;**
> **therefore: not in sync;**
> **therefore: 👋 bye bye css.**

## 🤔 What to come

- [ ] How about js too?
- [ ] Obfuscate everything?
