geogut
======

Tiny command line tool(s) for geocoding from strings

## gut.py

This script for now does one thing only: It tries to return the geo-position (latitude, longitude) of a street intersections.

### Usage

    python gut.py [options] "Street1 / Street2"

Street1 and Street2 have to be actual street names. If they have an intersection, the location of the intersection will be printed out.

### Example

This will find the intersection of the two streets "Am Bayenturm" and "Ubierring". The option "-b" gives a bounding box which restricts the search result to a certain area. In this case, it is a box around the city of Cologne, Germany.

    > python gut.py -b 50.8,6.7,51.0,7.1 "Am Bayenturm / Ubierring"
    >>>> (50.922364224999995, 6.967146475)

### Parameters

#### -b, --bbox=[BBOX]

This is optional but highly recommended, since street names are highly ambigious. By restricting the search to a certain bounding box you can ensure that the result is more or less constrained to a certain city or regions. This also helps you speed up the query and limit data transfer considerably!

If you leave out this option, you risk bad results. If intersections of several streets with the same name exist, the average of these points will be returned. This might be in the middle of nowhere.

The bounding box is given as comma-seperated float values in the following order:

1. lower latitude
2. lower longitude
3. higher latitude
4. higher longitude