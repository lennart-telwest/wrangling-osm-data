#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET

OSM_FILE = "/Users/lt/Git/portfolio-projects/open_streetmap_data_wrangling/data/hamburg_germany.osm"
SAMPLE_FILE = "/Users/lt/Git/portfolio-projects/open_streetmap_data_wrangling/data/hamburg_sample_small.osm"

'''
Create a sample of elements with the correct tag:
'''

k = 20 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')