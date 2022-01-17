import re
import json

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

#name = 'index-hashed.html'
name = 'style-hashed.css'
with open(config['path'] + name, 'r') as f:
    lines = f.readlines()
    patternfile = name.split('.')[1].upper()
    substring = re.findall(config[f'pattern{patternfile}'], str(lines))

    #print(patternFile, substring)

substring = [s.translate({ord('.'): None, ord(
    '{'): None}).strip() for s in substring]

#substring = [string.split('"')[1].split() for string in substring]
#substring = list(set([s for lista in substring for s in lista]))

d = {}
""" for s in substring:
    shash = abs(hash(s)) % (10 ** 6)
    #print(s, shash)
    d.update({s: shash}) """

d.update({s: str(abs(hash(s)) % (10 ** 6)) for s in substring})

print(d, type(d))

for index, l in enumerate(lines):
    for k, v in d.items():
        if k in l:
            lines[index] = l.replace(k, 'c'+v)

print(lines)

with open(config['path'] + name, 'w') as f:
    f.writelines(lines)
    f.close()


#substring = [string.split('"')[1].split() for string in substring]

#setting = list(set([s for lista in substring for s in lista]))
# print(setting)
