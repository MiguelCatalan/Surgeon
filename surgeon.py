#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Miguel Catalan Bañuls'
import glob
import xml.dom.minidom
import os
from xml.etree import ElementTree

import config


RESOURCES_DIR = config.PROJECT_PATH + config.MODULE_NAME + '/src/' + config.FLAVOUR + '/res/'


def junk_empty_lines(temp):
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
    xml_files = glob.glob(path + '/' + config.STRING_FILES_PREFIX + '*' + config.STRING_FILES_SUFFIX)
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
    dom_a = xml.dom.minidom.parse(file_1 + "/merge_strings.xml")
    dom_b = xml.dom.minidom.parse(file_2 + "/merge_strings.xml")

    strings_a = dom_a.getElementsByTagName("string")
    strings_b = dom_b.getElementsByTagName("string")

    diff = []
    for elementA in strings_a:
        for elementB in strings_b:
            if elementA.getAttribute('name') == elementB.getAttribute('name'):
                diff.append(elementA)
    results = set(strings_a).difference(diff)

    formatted_results = []
    for result in results:
        formatted_results.append(result.toprettyxml())

    formatted_results = junk_empty_lines(formatted_results)
    print "Found ", len(formatted_results), " differences in " + file_2
    return formatted_results


def create_xml_format(content):
    content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<resources>\n" + content
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
        try:
            save_file(directory + "/merge_strings.xml", ElementTree.tostring(temp_file))
        except AttributeError:
            print "Oops!  That was no valid number.  Try again..."

        if directory is not directories[0]:
            save_file(directory + "/" + config.DIFF_FILE_NAME,
                      create_xml_format('\n'.join(get_differences(directories[0], directory))))
            # get_true_differences(directories[0], directory)
            print "Saving changes in " + directory + "/" + config.DIFF_FILE_NAME
        print "\n"

    for directory in directories:
        remove_file(directory + "/merge_strings.xml")

    print "-" * 60
    print("Surgeon is done ٩(◕‿◕٩)")
    print "-" * 60