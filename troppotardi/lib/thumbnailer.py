from PIL import Image
import os
from pylons import config

def thumbnailer(filename, max_width=None, max_height=None, crop=False):
    """Given the filename of an image in the image dir,
    it thumbnails it and stores it in the thumbnails directory
    (both directories are defined in the ini file).
    It then returns the url of the thumbnail."""
    
    name, ext = os.path.splitext(filename)

    name = name + '_' + str(max_width) + 'x' + str(max_height)

    if crop:
        name += '_crop_'

    name += ext

    # If the thumbnail already exists, don't create it.
    # This could be dangerous if the image could be changed, but
    # the image cannot be changed right now, so it should be safe.
    if not os.path.isfile(os.path.join(config['thumbs_dir'], name)):
        
        im = Image.open(os.path.join(config['images_dir'], filename))
        (width, height) = im.size

        # If the image is smaller then the max size, we don't touch it
        if not (width <= max_width and height <= max_height):
            if crop and max_width and max_height:
                if width >= height:
                    thumb_height = max_height
                    thumb_width = width * max_height / height
                    sx = (thumb_width - max_width) / 2
                    up = 0
                    dx = sx + max_width
                    low = max_height
                else:
                    thumb_width = max_width
                    thumb_height = max_width * height / width
                    sx = 0
                    up = (thumb_height - max_height) /2
                    dx = max_width
                    low = max_height + up
                    
                im.thumbnail((thumb_width, thumb_height), Image.ANTIALIAS)
                im = im.crop((sx, up, dx, low))
            else:
                if max_width and max_height:
                    if width > height: max_height = None
                    else: max_width = None
                
                # Calculate the size...
                if max_width and not max_height:
                    max_height = height * max_width / width
                elif max_height and not max_width:
                    max_width = width * max_height / height
                
                im.thumbnail((max_width, max_height), Image.ANTIALIAS)

        # Save it 
        im.save(os.path.join(config['thumbs_dir'], name))
            
    return os.path.join(config['thumbs_base_url'], name)