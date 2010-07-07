window.addEvent('domready', initialize);

// Has the magnified been initialized?
var magnified = false;

function initialize()
{
    var img_helpers = $('img_helpers');
    var img_div = $('img_div');
    var image = $('image');
    
    // Image stuff
    if (img_helpers && image && img_div) {
        img_helpers.hide();
        img_helpers.set('html', img_helpers.get('html') +
                        '&middot; <a href="javascript:magnify_im()">Expand</a>');
        img_div.addEvent('mouseover', function(){img_helpers.show()});
        img_div.addEvent('mouseout', function(){img_helpers.hide()});

    }
}

function magnify_im()
{
    if (!magnified) {
        // Initialize the magnified window div
        var magnified_div = new Element('div', {
            'id': 'magnified_div',
        });
        magnified_div.setStyles({
            'position':'absolute',
            'left':'50%',
            'display':'none',
        });
        
        var magnified_img = new Element('img', {
            'src': $('img_link').get('href'),
            'id': 'magnified_img',
        });
        magnified_img.setStyle('cursor', 'pointer');
        magnified_img.addEvent('click', demagnify_im);
        
        magnified_img.inject(magnified_div);
        magnified_div.inject(document.body);
        
        magnified_div.setStyle('display', 'none');

        window.imgsize = {
            'x': magnified_img.width,
            'y': magnified_img.height,
        };
        alert(magnified_img.width);
        magnified = true;
    }
    res_magnified_im();
    $('magnified_div').setStyle('display', 'block');
}

function demagnify_im()
{
    $('magnified_div').setStyle('display', 'none');
}

function res_magnified_im()
{
    var winsize = window.getSize();
    winsize.x -= 40;
    winsize.y -= 40;

    var imgsize = window.imgsize;

    var imgresize = {
        'x': imgsize.x,
        'y': imgsize.y,
    };
    
    if (imgsize.x > winsize.x && imgsize.x <= imgsize.y) {
        imgresize.x = winsize.x;
        imgresize.y = imgresize.x * imgsize.y / imgsize.x;
    } else if (imgsize.y > winsize.y) {
        imgresize.y = winsize.y;
        imgresize.x = imgresize.y * imgsize.x / imgsize.y;
    }
    
    $('magnified_img').set('width', imgresize.x);
    $('magnified_img').set('height', imgresize.y);
    $('magnified_div').setStyles({
        'margin-left': -(imgresize.x / 2),
        'top': (winsize.y + 40 - imgresize.y) / 2,
    });
}