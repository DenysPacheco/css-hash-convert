# Css Hashfy Converter

This is a python script to hashfy css classes.
It was inspired on Google's approach to minimize classes names to faster load web pages.

## What it does

- [x] Make a hash out of css classes and apply for all html
- [x] Create `hashed` files with the output
- [x] Auto change the css name of the link tag 

## Usage

Just put the script/files on the top folder and execute.

It will search all files with the extensions marked on the configuration file.

It will give the output with `foo-hashed.html`

### Configure

Use the [configuration file](config.json) to change behaviour and variables of the script

## Future features

- [ ] Hashfy id's
- [ ] Multiple files on mutiple folders (with track)
- [ ] Hash function use letters
- [ ] Delete old files on new run
- [ ] Add tests?
