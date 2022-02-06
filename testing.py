import re
from functions import *


htmlString = """<div class="center-text di-4">
        <p class="backg-success">This is a text of a html</p>
    </div>"""

lines = read('examples/index.html')

for index, line in enumerate(lines):
    # print(index, line)
    line = re.sub(config['patternHTMLClear'], '', str(line)).strip()
    lines[index] = line

print(lines)

write('examples/', 'index.min.html', lines)
"""
print(htmlString.replace('\n', ''))

pattern = "[^><a-zA-Z] ( *)"

#text_after = re.sub(regex_search_term, regex_replacement, text_before)
find = re.sub(pattern, '', str(htmlString))

print(find)
"""
