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
import tempfile
import os
import webbrowser

try:
    import gtk 
except:
    print "Only GTK compatible systems available for now."
    sys.exit(5)


TEMP_DIR = tempfile.gettempdir()
TEMP_FILE = "imgurupx.tmp"

def delete_image():
    try:
        url = open(os.path.join(TEMP_DIR, TEMP_FILE), "r").read()
        webbrowser.open(url)
        # terminate right after opening the browser since 
        # there is nothing more to be done
        sys.exit(0)
    except IOError:
        print "Temp file doesn't exist or was deleted. Cannot delete image from server."

def parse_opts(): 
    usage = """usage: %prog [OPTIONS] IMAGE
    OR %prog [-d] to delete latest uploaded image"""

    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--original", action="store_true", dest="orig",
            help="Get original image size")
    parser.add_option("-s", "--small", action="store_true", dest="small",
            help="Get small thumbnail")
    parser.add_option("-l", "--large", action="store_true", dest="large",
            help="Get large thumbnail")
    parser.add_option("-d", "--del", action="store_true", dest="delete",
            help="Delete last uploaded image. Warning: When [-d/--del] is specified, all other" 
                  " options are ignored.")

    (options, args) = parser.parse_args()

    # only one valid positional argument allowed -- the image file path or name
    if len(args) != 1:
        parser.error("Please specify one valid filename or path")
    else:
        filename = args[0]

    if options.delete:
        delete_image()
    # The strings returned are names of xml tags that are part of imgur's response
    # to the request
    if options.small:
        return ("small_thumbnail", filename)
    elif options.large:
        return ("large_thumbnail", filename)
    else:
        return ("original_image", filename)
        
def write_old_link(url):
    try:
        open(os.path.join(TEMP_DIR, TEMP_FILE), "w").write(url)
    except IOError:
        print "Unable to create temp file."
    
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

    write_old_link(doc.getElementsByTagName("delete_page")[0].firstChild.nodeValue)
    
    clipboard = gtk.clipboard_get()
    clipboard.set_text(img_link)
    
    # store the contents so other applications can also have access to the data
    clipboard.store()

if __name__ == "__main__":
    main()
