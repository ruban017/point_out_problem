#model.py


from gmplot import gmplot
import uuid
from coor import get_coor


def locatee(lat, long):
    gmap = gmplot.GoogleMapPlotter(lat, long, 12)

    gmap.marker(lat, long, 'cornflowerblue')
    

    gmap.draw('location.html')


# print(get_coor(r'drive_images\test.jpg'))
# c = get_coor(r'drive_images\test.jpg')
# locatee(c[0], c[1])