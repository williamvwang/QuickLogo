from PIL import Image
import os
import math
import easygui
import webbrowser
import cloudinary
import cloudinary.uploader
import cloudinary.api

"""
QuickLogo v1.1 (Beta)
by William Wang

Takes in an image, strips it of most common-colored pixels,
then uploads it to a Cloudinary cloud of your choice.

To resolve dependencies:
$ pip install pillow
$ pip install easygui
$ pip install cloudinary

"""

def most_frequent_color(image):
    """
    Input:
    image -- Image file

    Output:
    Most frequent color found in the image as a 4-tuple (R,G,B,A)
    """
    x, y = image.size
    colors = image.getcolors(x * y)

    most_frequent = colors[0] # first (count, rgba value) in colors

    for count, pixel in colors:
        if count > most_frequent[0]:
            most_frequent = (count, pixel)

    return most_frequent[1]

def color_to_transparency(image, target_color, threshold):
    """
    Transforms pixels within a certain color range to transparent

    Inputs:
    file_in -- string filename of image to transform
    file_out -- string filename the transformed image will be saved to
    target_color -- RGBA tuple representing the esteimated color to remove
    threshold -- maximum 4D distance between target_color and removed pixels

    Outputs:
    None
    """
    # Convert to sequence object containing pixel values
    pixelData = image.load()

    target_red, target_green, target_blue, target_opacity = target_color[0], target_color[1], target_color[2], target_color[3],

    # Find all near-target-color pixels and set their opacity to 0
    for y in xrange(image.size[1]):
        for x in xrange(image.size[0]):
            pixel = pixelData[x, y]
            red, green, blue, opacity = pixel[0], pixel[1], pixel[2], pixel[3]
            if math.sqrt((red - target_red)**2 + (green - target_green)**2 + (blue - target_blue)**2 + (opacity - target_opacity)**2) <= threshold:
                pixelData[x, y] = (255,255,255,0)
    print "Color to transparency applied"

    return image

def preview(file_in, savepath, file_out):
    """
    Opens before and after comparison in web browser
    """
    html = open("testpage.html", "w")
    html.write("<html><head><title>Test Page</title><style>body{background:rgba(0,0,0,.7);color:#fff;font-family:'Arial';}img{max-height:30%;max-width:40%;display:block;margin-left:auto;margin-right:auto;margin-top:10px;}</style>")
    temp = "</head><body>Before<img src='" + file_in + "'>After<img src='"+ savepath + file_out + "'></body></html>"
    html.write(temp)
    html.close()
    webbrowser.open("testpage.html", new=2, autoraise=False)

def upload(filename):
    """
    Performs upload to specified cloud

    Input:
    filename -- string filename of image to upload
    """
    cloud_name = None  # YOUR_CLOUD_NAME_HERE
    api_key = None     # YOUR_API_KEY_HERE
    api_secret = None  # YOUR_API_SECRET_HERE

    cloudinary.config( 
      cloud_name = cloud_name, 
      api_key = api_key, 
      api_secret =  api_secret
    )
    return cloudinary.uploader.upload(filename)

def run(file_in, savepath, threshold=30):
    """
    Runs QuickLogo

    Inputs:
    file_in -- string filename of image to transform
    file_out -- string filename the transformed image will be saved to
    threshold -- maximum 4D distance between target_color and removed pixels
    """
    alias = file_in.split("\\")[-1]
    print "Transforming", alias
    file_out = "".join(alias.split(".")[:-1]) + "-out.png"

    img = Image.open(file_in)
    # Convert to RGBA colorspace
    img = img.convert("RGBA")
    
    target_color = most_frequent_color(img)
    transformed = color_to_transparency(img, target_color, threshold)

    local_savepath = savepath
    if not os.path.exists(local_savepath):
        os.makedirs(local_savepath)
    transformed.save(local_savepath + file_out, "PNG")        # output file name and extension
    print "Saved to", savepath + file_out
 
    return file_out


# Main
file_in = str(easygui.fileopenbox("Select image to process..."))
savepath = "./TestOut/"     # Manually specify image save directory

if (not file_in == "."):
    file_out = run(file_in, savepath , 50)
    preview(file_in, savepath, file_out)

    """ Uncomment this block to enable Cloudinary upload

    proceed = raw_input("Continue with upload? (Y/N) >")
    if proceed.lower() == 'y':
        print upload(savepath + file_out)
        print "Upload Complete"
    elif proceed.lower() == 'n':
        print "Upload aborted"
    else:
        print "Invalid input, upload aborted"

    """
    print "Done"
else:
    print "No file was specified"