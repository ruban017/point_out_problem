from PIL import Image, ExifTags
from pprint import pprint

def get_coor(path):
    img = Image.open(path)
    exif = {
    ExifTags.TAGS[k]: v
    for k , v in img._getexif().items()
    if k in ExifTags.TAGS
    }

    if exif:
        north = exif['GPSInfo'][2]
        east = exif['GPSInfo'][4]
        lat = ((((north[0]*60)+north[1])*60)+north[2])/60/60
        long =  ((((east[0]*60)+east[1])*60)+east[2])/60/60

        lat, long = (float(lat)), (float(long))
        return (lat, long)
        #return (f"Latitude and Longitude: {lat, long} \nDate and Time: {exif['DateTimeOriginal']} \nMake of the device: {exif['Make']} \nModel: {exif['Model']}")

    else:
        print("No data")



# c = get_coor(r'drive_images\test.jpg')

# print(c[0])
# print(c[1])

