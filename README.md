geogut
======

Tiny command line tool(s) for geocoding from strings

## gut.py

This script for now does one thing only: It tries to return the geo-position (longitude, latitude) of a street intersection.

It uses the Overpass API, which is based on OpenStreetmap data. This means that returned data is courtesy of OpenStreetmap. See http://www.openstreetmap.org/copyright on how to attribute.

### Usage

    python gut.py [options] "Street1 / Street2"

Street1 and Street2 have to be actual street names. If they have an intersection, the location of the intersection will be printed out.

### Example

This will find the intersection of the two streets "Am Bayenturm" and "Ubierring". The option "-b" gives a bounding box which restricts the search result to a certain area. In this case, it is a box around the city of Cologne, Germany.

    > python gut.py -b 6.7,50.8,7.1,51.0 "Am Bayenturm / Ubierring"
    >>>> 6.967146475,50.922364224999995

For batch processing give file with an intersection on each line as `stdin` and get a pair of coordinates for each line on `stdout`. `stderr` is used for log messages.

    > python gut.py -b 6.7,50.8,7.1,51.0 < input.txt > output.txt

### Parameters

#### -b, --bbox=[BBOX]

This is optional but highly recommended, since street names are highly ambigious. By restricting the search to a certain bounding box you can ensure that the result is more or less constrained to a certain city or regions. This also helps you speed up the query and limit data transfer considerably!

If you leave out this option, you risk bad results. If intersections of several streets with the same name exist, the average of these points will be returned. This might be in the middle of nowhere.

The bounding box is given as comma-seperated float values in the following order:

1. lower longitude
2. lower latitude
3. higher longitude
4. higher latitude

### Caching

Overpass API requests are cached automatically in a file called `geogut_cache.py` in the current working directory.
This speeds up identical requests and takes load from the Overpass servers.

You can delete the cache file in order to make sure that the server is connected for fresh results. The file
will be recreated upon next run.
