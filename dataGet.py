from pystac_client import Client

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
def makeBBOX(lat, long, size = 20):
    """
    This function creates a simple bounding box that is used to search for Landsat images in a certain location
    @param lat: The latitude of the center of your box
    @param long: The longitude of the center of your box
    @param size: Default=20. Size of the edges of your box in miles
    @return: Returns an array in BBOX style [minLong, minLat, maxLong, maxLat]
    """
    latmove, lonmove = size_to_coords(float(size/2))
    minLong = long - lonmove
    maxLong = long + lonmove
    minLat = lat - latmove
    maxLat = lat + latmove
    return [minLong, minLat, maxLong, maxLat]

#Let's query the Landsat STAC server to get what we want.
def stacSearch(bbox, dt, max_items = -1, cf=-1):
    """
    This funciton queries the Landsat STAC server and returns the results
    @param bbox: [minLong, minLat, maxLong, maxLat]. The bounding box of the area you wish to search
    @param dt: "YEAR-MONTH-DAY/YEAR-MONTH-DAY". The timerange you wish to search over
    @param max_items: The max number of items you wish to get back. If no input, will return everything found in search
    @param cf: Filters search to only have less than input cloud coverage.
    @return: Returns the item object from the search.
    """
    LandsatSTAC = Client.open("https://landsatlook.usgs.gov/stac-server")

    if max_items != -1 and cf != -1:
        searchResults = LandsatSTAC.search(
            max_items = max_items,
            bbox = bbox,
            datetime = dt,
            collections=['landsat-c2l2-sr'],
            query={"eo:cloud_cover":{"lt":cf}})
    elif max_items:
        searchResults = LandsatSTAC.search(
            max_items = max_items,
            bbox = bbox,
            datetime = dt,
            collections=['landsat-c2l2-sr'])
    elif cf:
        searchResults = LandsatSTAC.search(
            bbox = bbox,
            datetime = dt,
            collections=['landsat-c2l2-sr'],
            query={"eo:cloud_cover":{"lt":cf}})
    else: 
        searchResults = LandsatSTAC.search(
            bbox = bbox,
            datetime = dt,
            collections=['landsat-c2l2-sr'],)

    return searchResults

def getBands(searchItem, bands):
    """
    Get specified bands from query results
    @param searchItem: The search result item from LandsatSTAC search results
    @param bands: An array of strings containing the common names of wanted bands
    """
    itemDict = [i.to_dict() for i in searchItem.items()]
    #supa dupa slow nested loop
    bandsArr = []
    #anotha one
    for item in itemDict:
        hitArr = []
        for i in range(len(bands)):
            hitArr.append(item['assets'][bands[i]]['href'])
        bandsArr.append(hitArr)
    return bandsArr