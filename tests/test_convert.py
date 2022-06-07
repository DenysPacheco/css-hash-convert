import os
import re

from src.utils import lookFiles, read


def test_find_spaces_html():

    results = find_spaces_html()

    assert results == []


def test_find_not_hashed_classes_html():

    results = find_html_classes()
    list = set()
    ignore = ["fa"]

    for item in results:
        for line in item:
            stripLine = line.split('"')[1].split()
            for i in stripLine:
                for ig in ignore:
                    if ig not in i:
                        list.add(i)

    for item in list:
        assert item.startswith("_")


def test_non_min_tags_html():
    files = lookFiles()
    css_files = [file for _, file in files if file.endswith(".css")]

    for file in files:
        dir, arc = file
        name, ext = arc.split(".")
        arc = name + ".min." + ext
        if arc.endswith(".html"):
            f = os.path.join(dir, arc)
            links = re.findall(
                "(?<=<link).*(?<=href..)(?!http)(\\S+)(?=\"|\\')", str(read(f))
            )
            for line in links:
                if line in css_files:
                    assert ".min" in line


# test_non_min_tags_html()

########## Test Functions ##########


def find_spaces_html():
    files = lookFiles()
    results = 0

    for file in files:
        dir, arc = file
        name, ext = arc.split(".")
        arc = name + ".min." + ext
        if arc.endswith(".html"):
            f = os.path.join(dir, arc)
            results = re.findall(
                "[^><a-zA-Z0-9\"',._-] ( *)|(<!--(.*?)-->)", str(read(f))
            )

    return results


def find_html_classes():
    files = lookFiles()
    results = []

    for file in files:
        dir, arc = file
        name, ext = arc.split(".")
        arc = name + ".min." + ext
        if arc.endswith(".html"):
            f = os.path.join(dir, arc)
            results.append(re.findall('class[\t]*=[\t]*"[^"]+', str(read(f))))

    return results
