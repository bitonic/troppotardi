<%inherit file="/layout.mako"/>

<%def name="title()">${parent.title()} ${c.image.author}</%def>

<%def name="head()">
${parent.head()}
<script type="text/javascript" src="/js/mootools-1.2.4-core-yc.js"></script>
<script type="text/javascript">
// Resizes the image if the screen height is not enough
window.addEvent('domready', function() {
    var image = $('image');
    image.addEvent('load', function() {
        if (image.getSize().y + 10 > window.getSize().y)
        {
            image_height = window.getSize().y - 10;
            old_image_width = image.getSize().x;
            image_width = image.width * image_height / image.getSize().y;
            image.setProperties({
                height: image_height,
                width: image_width,
            });
        }
    });
});
</script>
</%def>

<div id="text">
    <b>
    % if c.image.author_url:
        <a href="${c.image.author_url}" target="_blank">${c.image.author}</a>
    % else:
        ${c.image.author}
    % endif
    </b>
     - ${c.image.day.strftime("%d.%m.%Y")}
    % if c.image.text:
        <br/><span id="descr">${c.image.text}</span>
    % endif
</div>

<div id="prevnext">
% if hasattr(c, 'older') or hasattr(c, 'newer'):
    <div id="previous">
    % if hasattr(c, 'newer'):
            <a href="${h.url(controller='images', action='show', day=c.newer)}">&larr;</a>
    % endif
    </div>
    <div id="fullsize">
        <a href="${c.image.url}" alt="Fullsize image">Fullsize image</a>
    </div>
    % if hasattr(c, 'older'):
        <div id="next">
            <a href="${h.url(controller='images', action='show', day=c.older)}">&rarr;</a>
        </div>
    % endif
% endif
</div>

<div id="img_div">
    % if hasattr(c, 'older'):
        <a href="${h.url(controller='images', action='show', day=c.older)}">
            <img src="${h.thumbnailer(c.image.filename, max_width=690, max_height=690)}" alt="${c.image.day}" id="image" />
        </a>
    % else:
        <img src="${h.thumbnailer(c.image.filename, max_width=690, max_height=690)}" alt="${c.image.day}" id="image" />
    % endif
</div>
