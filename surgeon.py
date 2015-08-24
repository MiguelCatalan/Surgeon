#!/usr/bin/python
__author__ = 'miguel'
import glob
from xml.etree import ElementTree

RESOURCES_DIR = 'app/src/main/res/'
MAIN_VALUES_DIR = 'values/'


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
    xml_files = glob.glob(path + 'strings_*')
    xml_element_tree = None
    for xml_file in xml_files:
        data = ElementTree.parse(xml_file).getroot()
        print("Processing file " + xml_file)
        for result in data.iter('resources'):
            if xml_element_tree is None:
                xml_element_tree = data
            else:
                xml_element_tree.extend(result)

    if xml_element_tree is not None:
        format_xml(xml_element_tree)
        return xml_element_tree

# Main program
if __name__ == "__main__":
    print "-" * 40
    print("Surgeon in the operation room!")
    main_file = merge_string_files(RESOURCES_DIR + MAIN_VALUES_DIR)