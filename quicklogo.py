from PIL import Image
import easygui
import webbrowser
import cloudinary
import cloudinary.uploader
import cloudinary.api

"""
QuickLogo
by William Wang

Takes in an image, strips it of near-white pixels,
then uploads it to a Cloudinary cloud of your choice.

To resolve dependencies:
$ pip install pillow
$ pip install easygui
$ pip install cloudinary

"""

def white_to_transparency(file_in, file_out, limit=200):
    """
    Transforms white-ish pixels to transparent

    Inputs:
    file_in -- string filename of image to transform
    file_out -- string filename the transformed image will be saved to
    limit -- RGB value of (limit, limit, limit) will be used as lower "whiteness" bound of a pixel.

    Outputs:
    None

    Note: lowering limit too far will result in removal of certain dark grey pixels. For example,
    a limit of 160 or lower will completely remove the Apple logo. Change this value at your discretion.
    """
    alias = file_in.split("\\")[-1]
    print "Transforming", alias
    img = Image.open(file_in)
    # Convert to RGBA colorspace
    img = img.convert("RGBA")
    # Convert to sequence object containing pixel values
    pixelData = img.load()

    # Find all near-white pixels and set their opacity to 0
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            pixel = pixelData[x, y]
            red, green, blue = pixel[0], pixel[1], pixel[2]
            # Suggested value for limit is ~200, can adjust depending on image
            if red > limit and green > limit and blue > limit:
                pixelData[x, y] = (255,255,255,0)
    print "White to transparency applied"

    img.save(file_out, "PNG")              # output file name and extension
    print "Saved to", file_out

def preview(file_in, file_out):
    html = open("testpage.html", "w")
    html.write("<html><head><title>Test Page</title><style>body{background:rgba(0,0,0,.7);color:#fff;font-family:'Arial';}img{max-height:30%;max-width:40%;display:block;margin-left:auto;margin-right:auto;margin-top:10px;}</style>")
    temp = "</head><body>Before<img src='"+file_in+"'>After<img src='"+file_out+"'></body></html>"
    html.write(temp)
    html.close()
    webbrowser.open("testpage.html", new=2, autoraise=False)

def upload(filename):
    """
    Performs upload to specified cloud

    Input:
    filename -- string filename of image to upload
    """
    cloud_name = None   # YOUR_CLOUD_NAME_HERE
    api_key = None  # YOUR_API_KEY_HERE
    api_secret = None  # YOUR_API_SECRET_HERE

    cloudinary.config( 
      cloud_name = cloud_name, 
      api_key = api_key, 
      api_secret =  api_secret
    )
    return cloudinary.uploader.upload(filename)

# Main
file_in = str(easygui.fileopenbox())
file_out = "out.png"

white_to_transparency(file_in, file_out, 160)
preview(file_in, file_out)

proceed = raw_input("Continue? (Y/N) >")

if proceed.lower() == 'y':
    print upload(file_out)
    print "Done"
elif proceed.lower() == 'n':
    print "Upload aborted"
else:
    print "Invalid input, upload aborted"