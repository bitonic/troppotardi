from PIL import Image
import os
from pylons import config

def thumbnailer(filename, max_width=None, max_height=None):
    """Given the filename of an image in the image dir,
    it thumbnails it and stores it in the thumbnails directory
    (both directories are defined in the ini file).
    It then returns the url of the thumbnail."""
    
    name, ext = os.path.splitext(filename)

    # Name = oldname_newwidth_newheight.extension
    name = name + '_' + str(max_width) + 'x' + str(max_height) + ext

    # If the thumbnail already exists, don't create it.
    # This could be dangerous if the image could be changed, but
    # the image cannot be changed right now, so it should be safe.
    if not os.path.isfile(os.path.join(config['thumbs_dir'], name)):

        im = Image.open(os.path.join(config['images_dir'], filename))
        (width, height) = im.size

        # Calculate the size...
        if max_width and not max_height:
            max_height = height * max_width / width
        elif max_height and not max_width:
            max_width = width * max_height / height
    
        size = max_width, max_height

        # Thumbnail it
        im.thumbnail(size, Image.ANTIALIAS)
            
        # Saving it 
        im.save(os.path.join(config['thumbs_dir'], name))
            
    return os.path.join(config['thumbs_base_url'], name)
