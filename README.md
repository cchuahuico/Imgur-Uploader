Imgur Uploader
--------------
--------------
Upload image to imgur.com and copies link to image to clipboard.            
                               
Requirements: 
-------------
-------------

 - Python 2.5+ / ActiveState Python (if
   using windows because of dependency
   on win32clipboard module)
 - GTK based desktop manager (for Unix
   based OS)
 - pycurl:
   http://pycurl.sourceforge.net/      

Usage:
------
------

![imgurup help](http://i.imgur.com/S5Xhz.png)

Alternative:
------------
------------
The way I used this is I added new context menus and actions in my default file manager.  
 
For GNOME users with nautilus installed, I used a utility called [Nautilus Actions][1]. For Ubuntu users, this can be installed by entering: `sudo apt-get install nautilus-actions`

Here's a screenshot of the menu:  

![upload menu](http://i.imgur.com/cNWM5.png)


  [1]: http://freshmeat.net/projects/nautilus-actions/

Deleting Images:
----------------
----------------
It is possible to delete an image already uploaded to imgur's server using the `-d` or `--del` option. The script keeps a hash of your image in a temp file and uses that to delete the latest uploaded image.
