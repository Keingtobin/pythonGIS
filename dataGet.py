#This script will get the data that we want

#convert size in miles to coordinate degree values
def size_to_coords(size):
    """
    @param size: Distance in miles.
    """
    abs_size = abs(size)
    latmove = float(1/69)*abs_size
    lonmove = float(1/54.6)*abs_size
    return latmove,lonmove

#make a BBOX
def makeBBOX(long, lat, size = 20):
    """
    @param long: The longitude of the center of your box
    @param lat: The latitude of the center of your box
    @param size: Default=20. Size of the edges of your box in miles
    @return: Returns an array in BBOX style [minLong, minLat, maxLong, maxLat]
    """
    latmove, lonmove = size_to_coords(float(size/2))
    minLong = long - lonmove
    maxLong = long + lonmove
    minLat = lat - latmove
    maxLat = lat + latmove
    return [minLong, minLat, maxLong, maxLat]

