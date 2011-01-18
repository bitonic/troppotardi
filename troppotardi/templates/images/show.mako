<%inherit file="/layout.mako"/>

<%def name="title()">${parent.title()} ${c.image.author}</%def>

<%def name="head()">
${parent.head()}
<script type="text/javascript" src="/js/mootools-core-1.3-full-compat-yc.js"></script>
<script type="text/javascript">
maximized = false;

window.addEvent('domready', function() {
    // Resizes the image if the screen height is not enough
    var image = $$('#image img')[0];
    image.addEvent('load', function() {
        if (image.getSize().y + 20 > window.getSize().y)
        {
            image_height = window.getSize().y - 20;

            if (image_height < 450)
                image_height = 450;

            old_image_width = image.getSize().x;
            image_width = image.width * image_height / image.getSize().y;
            image.setProperties({
                height: image_height,
                width: image_width,
            });
        }
    });

    // Adds arrows control
    window.addEvent('keydown', function(event){
        % if hasattr(c, 'newer'):
            if (event.key == 'left') {
                window.location = "${h.url(controller='images', action='show', day=c.newer, qualified=True)}";
            }
        % endif
        % if hasattr(c, 'older'):
            if (event.key == 'right') {
                window.location = "${h.url(controller='images', action='show', day=c.older, qualified=True)}";
            }
        % endif
    });

    // Adds the maximize stuff
    var image_links = $$('#image ul')[0];
    var width = window.getSize().x - 200;
    var url = '${url(controller='images', action='display_thumb', image=c.image.filename)}';
    url += '&max_width=' + (width - 30);
    
    // Preload
    var big_img = new Image();
    big_img.src = url;

    big_img.addEvent('load', function(event) {
        if (big_img.width > 690) {
            image_links.innerHTML += '<li><a href="javascript:toggle_maximize(\'' + url + '\', ' + width +')"><img src="/layout_images/maximize.png" alt="Maximize" /></a></li>';
        }
    });
});

function toggle_maximize(url, width) {
    if (maximized) {
        $('image_show').src = '${h.thumbnailer(c.image.filename, max_width=690, max_height=800)}';
    } else {
        $('image_show').src = url;
        $('image').setStyle('width', width + 'px');
        $('container').setStyle('width', (width + 200) + 'px');
    }
    maximized = !maximized;
}
</script>
</%def>

<div id="img_div">
    <div id="image">
        <ul>
            <li><a href="${c.image.url}" target="_blank"><img src="/layout_images/save.png" alt="Save image" /></a></li>
        </ul>
        % if hasattr(c, 'older'):
            <a href="${h.url(controller='images', action='show', day=c.older)}">
                <img src="${h.thumbnailer(c.image.filename, max_width=690, max_height=800)}" alt="${c.image.day}" id="image_show" />
            </a>
        % else:
            <a href="#">
                <img src="${h.thumbnailer(c.image.filename, max_width=690, max_height=800)}" alt="${c.image.day}" id="image_show" />
            </a>
        % endif
    </div>

    <div id="prevnext">
    % if hasattr(c, 'older') or hasattr(c, 'newer'):
        % if hasattr(c, 'newer'):
            <a href="${h.url(controller='images', action='show', day=c.newer)}" id="previous">&larr;</a>
        % endif             
        % if hasattr(c, 'older'):
            <a href="${h.url(controller='images', action='show', day=c.older)}" id="next">&rarr;</a>
        % endif
    % endif
    </div>

    <div id="text">
        <b>
        % if c.image.author_url:
            <a href="${c.image.author_url}" target="_blank">${c.image.author}</a>
        % else:
            ${c.image.author}
        % endif
        </b><br/>
        ${c.image.day.strftime("%d.%m.%Y")}
        % if c.image.text:
            <br/><span id="descr">${c.image.text}</span>
        % endif
    </div>
</div>
