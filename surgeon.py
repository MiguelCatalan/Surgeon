#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Miguel Catalan Bañuls'
import glob
import xml.dom.minidom
import difflib
import os
from xml.etree import ElementTree

import config


RESOURCES_DIR = config.PROJECT_PATH + config.MODULE_NAME + '/src/' + config.FLAVOUR + '/res/'


def junkemptylines(temp):
    textA = []
    for text in temp:
        text = text.rstrip()
        if len(text):
            textA.append(text)
    return textA


def format_xml(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            format_xml(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def merge_string_files(path):
    xml_files = glob.glob(path + '/strings_*')
    xml_element_tree = None
    print("Merging files from " + path)
    for xml_file in xml_files:
        data = ElementTree.parse(xml_file).getroot()
        for result in data.iter('resources'):
            if xml_element_tree is None:
                xml_element_tree = data
            else:
                xml_element_tree.extend(result)

    if xml_element_tree is not None:
        format_xml(xml_element_tree)
        return xml_element_tree


def save_file(path_file, content):
    file_output = open(path_file, "wb")
    file_output.write(content.encode('utf-8'))
    file_output.close()


def remove_file(path_file):
    os.remove(path_file)


def get_all_values_dirs():
    values_dir = glob.glob(RESOURCES_DIR + 'values')
    values_dir.extend(glob.glob(RESOURCES_DIR + 'values-[a-z,A-Z][a-z,A-Z]'))
    values_dir.extend(glob.glob(RESOURCES_DIR + 'values-[a-z,A-Z][a-z,A-Z]-r*'))
    return values_dir


def get_differences(file_1, file_2):
    domA = xml.dom.minidom.parse(file_1 + "/merge_strings.xml")
    temp = domA.toprettyxml().splitlines(1)
    textA = junkemptylines(temp)
    domB = xml.dom.minidom.parse(file_2 + "/merge_strings.xml")
    temp = domB.toprettyxml().splitlines(1)
    textB = junkemptylines(temp)
    d = difflib.Differ()
    all = list(d.compare(textA, textB))
    diff = [l for l in all if l.startswith('- ') or l.startswith('+ ')]
    print "Found ", len(diff), " differences in " + file_2
    return diff


def create_xml_format(content):
    content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<resources>\n" + content
    content.replace("- 	", " 	")
    content.replace("+ 	", " 	")
    content = content + "\n</resources>"
    return content

# Main program
if __name__ == "__main__":
    print "-" * 60
    print("Surgeon in the operation room! ٩(◕‿◕٩)")
    print "-" * 60
    directories = get_all_values_dirs()

    main_files = []
    for directory in directories:
        temp_file = merge_string_files(directory)
        main_files.append(temp_file)
        save_file(directory + "/merge_strings.xml", ElementTree.tostring(temp_file))
        if directory is not directories[0]:
            save_file(directory + "/diff_strings.xml",
                      create_xml_format('\n'.join(get_differences(directories[0], directory))))
            print "Saving changes in " + directory + "/diff_strings.xml"
        print "\n"

    for directory in directories:
        remove_file(directory + "/merge_strings.xml")

    print "-" * 60
    print("Surgeon is done ٩(◕‿◕٩)")
    print "-" * 60