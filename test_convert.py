import re
import os
from functions import *


def test_find_spaces_html():

    results = find_spaces_html()

    assert results == []


def test_find_not_hashed_classes_html():

    results = find_html_classes()
    list = set()
    ignore = ['fa']

    for item in results:
        for line in item:
            stripLine = line.split('"')[1].split()
            for i in stripLine:
                for ig in ignore:
                    if(ig not in i):
                        list.add(i)

    for item in list:
        assert item.startswith('_')


########## Test Functions ##########

def find_spaces_html():
    files = lookFiles()
    results = 0

    for file in files:
        dir, arc = file
        name, ext = arc.split('.')
        arc = name + '.min.' + ext
        # print(os.path.join(dir, arc))
        if(arc.endswith('.html')):
            f = os.path.join(dir, arc)
            results = re.findall(
                "[^><a-zA-Z0-9\"',._-] ( *)|(<!--(.*?)-->)", str(read(f)))

    return results


def find_html_classes():
    files = lookFiles()
    results = []

    for file in files:
        dir, arc = file
        name, ext = arc.split('.')
        arc = name + '.min.' + ext
        if(arc.endswith('.html')):
            f = os.path.join(dir, arc)
            results.append(re.findall(
                "class[\t]*=[\t]*\"[^\"]+", str(read(f))))

    return results
