<%inherit file="/layout.mako"/>

<%def name="title()">${parent.title()} ${c.image.author}</%def>

<%def name="head()">
${parent.head()}
<link href="/css/show.css" media="screen" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="http://mazzo.li/jslibs/mootools-1.3-yc.js"></script>
<script type="text/javascript" src="http://mazzo.li/jslibs/mootools-more-1.3-yc.js"></script>
<script type="text/javascript">
var maximized = false;
var main_image;
var image_size = undefined;

window.addEvent('domready', function() {
    main_image = $('main_image');

    // Resizing
    Asset.image(main_image.src, {
        onLoad: function() {
            if (image_size == undefined) {
                image_size = main_image.getSize();
            }
            
            resize_image();
            
            window.addEvent('resize', resize_image);            
        }
    });

    // Adds arrows control
    window.addEvent('keydown', function(event){
        % if hasattr(c, 'newer'):
            if (event.key == 'left' || event.key == 'k') {
                window.location = "${c.newer}";
            }
        % endif
        % if hasattr(c, 'older'):
            if (event.key == 'right' || event.key == 'j') {
                window.location = "${c.older}";
            }
        % endif
    });

    // Adds the maximize stuff
    var image_links = $('resize_maximize');
    var width = window.getSize().x - $('right_col').getSize().x;
    var url = '${url(controller='images', action='display_thumb', image=c.image.filename)}';
    url += '&max_width=' + (width - 20);

    // Inject the element
    var maximize_image = new Element('li');
    maximize_image.grab(
        new Element('img', {
            src: '/layout_images/maximize.png',
            alt: 'Maximize',
            styles: {
                cursor: 'pointer',
            },
            events: {
                click: function() {toggle_maximize(url)},
            }
        }));
    
    image_links.grab(maximize_image);
});

function toggle_maximize(url) {
    if (maximized)
        main_image.set(
            'src', 
            '${h.thumbnailer(c.image.filename, max_width=690, max_height=700)}');
    else
        main_image.set('src', url);

    maximized = !maximized;

    resize_image();
}

function resize_image() {
    if (maximized) {
        main_image.removeProperties('width', 'height');
    } else {
        var window_height = window.getSize().y;
        var margin = 50;
        if (image_size.y + margin > window_height)
        {
            image_height = window_height - margin;
            
            if (image_height < 450)
                image_height = 450;
            
            image_width = image_size.x * image_height / image_size.y;
            
            if (image_width > image_size.x || image_height > image_size.y) {
                image_width = image_size.x;
                image_height = image_size.y;
            }

            main_image.setProperties({
                height: image_height,
                width: image_width,
            });
        }
    }
}
</script>
</%def>


<div id="right_col">
  <div id="prevnext">
    % if hasattr(c, 'older') or hasattr(c, 'newer'):
        % if hasattr(c, 'newer'):
            <a href="${c.newer}" id="previous">
              &larr;
            </a>
        % endif             
        % if hasattr(c, 'older'):
            <a href="${c.older}" id="next">
              &rarr;
            </a>
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
    </b>
    <br/>
    ${c.image.day.strftime("%d.%m.%Y")}
    % if c.image.text:
        <br/><span id="descr">${c.image.text}</span>
    % endif
  </div>
</div>

<%
image = h.thumbnailer(c.image.filename, max_width=690, max_height=700)
%>

% if hasattr(c, 'older'):
    <a href="${c.older}">
      <img src="${image}" alt="${c.image.day.strftime('%Y-%m-%d')}" id="main_image" />
    </a>
% else:
    <a href="#">
      <img src="${image}" alt="${c.image.day.strftime('%Y-%m-%d')}" id="main_image" />
    </a>
% endif

<ul id="resize_maximize">
  <li>
    <a href="${c.image.url}" target="_blank">
      <img src="/layout_images/save.png" alt="Save image" />
    </a>
  </li>
</ul>
