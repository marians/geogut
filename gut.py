#!/usr/bin/env python
# encoding: utf-8

import sys
import urllib
from optparse import OptionParser
import json


def overpass(queryparts):
    """
    Make an Overpass API request with the given query parts (list).
    All query parts will be issued in one request, seperated by
    semicolon. Return the resulting elements.
    """
    query = '[out:json];' + "\n"
    for part in queryparts:
        query += part + ';' + "\n"
    query += 'out body;' + "\n"
    request = urllib.urlopen(
        'http://overpass-api.de/api/interpreter',
        urllib.urlencode({'data': query.encode('utf-8')})
    )
    body = request.read()
    response = json.loads(body)
    return response['elements']


def get_nodes_for_street(string, options):
    """
    Return all nodes belonging to the street with the name given as string.
    Can be restricted to a bounding box (options.bbox).
    """
    overpass_args = []
    if options.bbox is not None:
        (lowerlat, lowerlon, upperlat, upperlon) = options.bbox.split(',')
        overpass_args.append('way["name"="%s"](%s,%s,%s,%s)' % (string, lowerlat, lowerlon, upperlat, upperlon))
    else:
        overpass_args.append('way["name"="%s"]' % string)
    overpass_args.append('>')  # recurse
    #print overpass_args
    elements = overpass(overpass_args)
    nodes = {}
    for el in elements:
        nodes[el['id']] = el
    return nodes


def geocode(string, options):
    """
    Parse a string containing multiple street names, divided by slash,
    and return the position of their intersection.
    Currently intersections are only found if at least one common node
    exists.
    TODO:
    - Fuzzy name resolution
    - approximation if streets have no intersection but close-enough nodes
    """
    parts = string.split('/')
    for n in range(0, len(parts)):
        parts[n] = parts[n].strip()
    if len(parts) > 1:
        nodes1 = get_nodes_for_street(parts[0], options)
        nodes2 = get_nodes_for_street(parts[1], options)
        crossnodes = get_common_nodes(nodes1, nodes2)
        if len(crossnodes) == 0:
            sys.stderr.write("Bummer: " + string + " have no intersection.\n")
            return None
        elif len(crossnodes) == 1:
            print string, "has 1 intersection node."
            return (crossnodes[0]['lat'], crossnodes[0]['lon'])
        else:
            print string, "has", len(crossnodes), "intersection nodes."
            return avg_nodes(crossnodes)


def get_common_nodes(nodes1, nodes2):
    """
    Return a list of nodes common to both lists nodes1 and nodes2
    """
    nodes = []
    nodeset = set(nodes1.keys()) & set(nodes2.keys())
    for n in nodeset:
        nodes.append(nodes1[n])
    return nodes


def avg_nodes(nodes):
    """
    Returns the average latitute/longitude of a list of nodes
    """
    sum_lat = 0
    sum_lon = 0
    count = 0
    for node in nodes:
        sum_lat += node['lat']
        sum_lon += node['lon']
        count += 1
    return (
        sum_lat / count,
        sum_lon / count
    )


if __name__ == '__main__':
    op = OptionParser()
    op.add_option("-c", "--country", dest="country",
        help="Restrict search to country (multiple countries seperated by comma", metavar="COUNTRY")
    op.add_option("-b", "--bbox", dest="bbox",
        help="Define this bounding box (lower lat, lower lon, upper lat, upper lon)", metavar="BBOX")
    op.add_option("-r", "--restrict", action="store_true", dest="restrict",
        help="Restrict the search to bbox. Otherwise will prefer items within bbox.")
    (options, args) = op.parse_args()
    if len(args) == 0 or args[0] == '':
        sys.stderr.write("You didn't provide a string to geocode.")
        sys.exit(1)
    print geocode(unicode(args[0], 'utf-8'), options)