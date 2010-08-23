"""
    imgurUp.py - Imgur Uploader
    author: Clarence Chuahuico
    
    Uploads an image to Imgur and link to original image for viewing is immediately copied to the gtk clipboard
    
    This program was meant to be added in the context menu of image files (.jpg/png/gif) but it 
    can also be used as a command line application. 
"""

from optparse import OptionParser
from xml.dom import minidom
import pycurl
import StringIO
import sys

try:
    import gtk 
except:
    print "Only GTK compatible GUI available for now."
    sys.exit(5);


def parse_opts():
    parser = OptionParser()
    parser.add_option("-o", "--original", action="store_true", dest="orig",
            help="Get original image size")
    parser.add_option("-s", "--small", action="store_true", dest="small",
            help="Get small thumbnail")
    parser.add_option("-l", "--large", action="store_true", dest="large",
            help="Get large thumbnail")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Please specify one valid filename or path")
        sys.exit(4)
    else:
        filename = args

    # If none of the options was specified, use original size by default
    if not any(options):
        options.orig = True
    else:
        # The string returns are names of xml tags that are part of imgur's response
        # to the request
        if options.orig:
            return ("original_image", filename)
        elif options.small:
            return ("small_thumbnail", filename)
        elif options.large:
            return ("large_thumbnail", filename)

def main():
    (size, image_name) = parse_opts()

    c = pycurl.Curl()

    values = [("key", "07c5b88af0f218d24da23498f5e1beb7"),
              ("image", (c.FORM_FILE, image_name))]

    c.setopt(c.URL, "http://imgur.com/api/upload.xml")
    c.setopt(c.HTTPPOST, values)
    b = StringIO.StringIO()
    
    # write output/server response to b for further link processing
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    c.close()
    
    result = b.getvalue()
    doc = minidom.parseString(result)
    
    # grab the contents of the value under specific size tag
    # ie. <original_image>http://www.imgur.com/xYz</original_image>
    img_link = doc.getElementsByTagName(size)[0].firstChild.nodeValue
    
    clipboard = gtk.clipboard_get()
    clipboard.set_text(img_link)
    
    # store the contents so other applications can also have access to the data
    clipboard.store()

if __name__ == "__main__":
    main()
