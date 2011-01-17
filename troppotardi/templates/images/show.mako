<%inherit file="/layout.mako"/>

<%def name="title()">${parent.title()} ${c.image.author}</%def>

<%def name="head()">
${parent.head()}
<script type="text/javascript" src="/js/mootools-1.2.4-core-yc.js"></script>
<script type="text/javascript" src="/js/FullScreenImage.js"></script>
<script type="text/javascript">
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

    /*
    // Full screen
    $('image').set('href', 'javascript:void(0)');
    var fullScreenPanel = new FullScreenImage($('image'), {swf:'/js/FullScreenImage.swf'});
    fullScreenPanel.show("${c.image.url}");
    */
});
</script>
</%def>

<div id="img_div">
    % if hasattr(c, 'older'):
        <a href="${h.url(controller='images', action='show', day=c.older)}" id="image">
            <img src="${h.thumbnailer(c.image.filename, max_width=690, max_height=800)}" alt="${c.image.day}" />
        </a>
    % else:
        <img src="${h.thumbnailer(c.image.filename, max_width=690, max_height=800)}" alt="${c.image.day}" id="image" />
    % endif

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
