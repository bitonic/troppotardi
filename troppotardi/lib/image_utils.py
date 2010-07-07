from PIL import Image
import os
from pylons import config

def thumbnailer(filename, max_width=None, max_height=None):
    name, ext = os.path.splitext(filename)
    name = name + '_' + str(max_width) + 'x' + str(max_height) + ext

    if not os.path.isfile(os.path.join(config['thumbs_dir'], name)):

        im = Image.open(os.path.join(config['images_dir'], filename))
        (width, height) = im.size
        if max_width and not max_height:
            max_height = height * max_width / width
        elif max_height and not max_width:
            max_width = width * max_height / height
    
        size = max_width, max_height
        im.thumbnail(size, Image.ANTIALIAS)
            
        im.save(os.path.join(config['thumbs_dir'], name))
            
    return os.path.join(config['thumbs_base_url'], name)
