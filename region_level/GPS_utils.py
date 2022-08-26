import numpy as np

from math import floor

origin_longitude        = -74.0829103
origin_latitude         =  40.7201914
top_left_longitude      = -73.9376847
top_left_latitude       =  40.8635402
bottom_right_longitude  = -73.9638201
bottom_right_latitude   =  40.6129328
# Top-right lat/lon 40.78907511 -73.92568926

# origin_longitude        = -74.081382
# origin_latitude         = 40.720894
# top_left_longitude      = -73.938361
# top_left_latitude       = 40.855682
# bottom_right_longitude  = -73.976151
# bottom_right_latitude   = 40.621217
# # Top-right lat/lon 40.7666219 -73.8163201

def gps_to_xy( lon, lat,
                    xbuckets = 1,
                    ybuckets = 1,
                    orlon = origin_longitude,
                    orlat = origin_latitude,
                    tllon = top_left_longitude,
                    tllat = top_left_latitude,
                    brlon = bottom_right_longitude,
                    brlat = bottom_right_latitude,
                    to_int = False ):
    ''' 
    gps_to_xy: Given a pair of GPS coordinates representing a
        location and 4 pairs of GPS coordinates defining a grid,
        get the GPS coordinates relative to that grid.
        (See: https://en.wikipedia.org/wiki/Change_of_basis) 
    # Arguments:
        lon, lat: Floating points representing GPS coordinates
        xbuckets, ybuckets: Integers represnting the grid size.
        orlon, orlat, ... brlat: Floating point values representing
            the GPS coordinates of the four corners defining the grid.
        to_int: If true, return the x, y coordinates in the grid
            as integers rather than floats
    # Returns:
        x, y coordinates in the grid (as floats, unless to_int == True).
            (E.g. gps_to_xy(lon=orlon, lat=orlat) = (0, 0))
            (E.g. gps_to_xy(lon=brlon, lat=brlat) = (1, 0))
    '''
    origin = np.array((orlon, orlat))

    b1 = np.array([brlon, brlat]) - origin
    b2 = np.array([tllon, tllat]) - origin
    B = np.array([b1, b2])

    x = np.array([lon, lat]) - origin

    c = np.matmul(x, np.linalg.inv(B))
    
    if not to_int:
        return c[0] * xbuckets, c[1] * ybuckets
    return floor(c[0] * xbuckets), floor(c[1] * ybuckets)

origin_array = np.array([origin_longitude, origin_latitude])
inv_basis = np.array([[ 4.39071984, 3.28529058],
                      [-4.44820552, 3.64768804]])

def pgps_to_xy(lon, lat):
    ''' gps_to_xy, using prebaked values to increase performance.'''
    x = (lon, lat) - origin_array
    c = np.matmul(x, inv_basis)
    return c[0], c[1]
