<%inherit file="/layout.mako"/>

<%def name="title()">${parent.title()} ${c.image.author}</%def>

<%def name="head()">
${parent.head()}
<link href="/css/show.css" media="screen" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="/js/mootools-core-1.3-full-compat-yc.js"></script>
<script type="text/javascript">
var maximized = false;
var main_image;

window.addEvent('domready', function() {
    main_image = $('main_image');

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
    var image_links = $('resize_maximize');
    var width = window.getSize().x - $('right_col').getSize().x;
    var url = '${url(controller='images', action='display_thumb', image=c.image.filename)}';
    url += '&max_width=' + (width - 40);

    var maximize_image = new Element('li');
    maximize_image.grab(
        new Element('img', {
            src: '/layout_images/maximize.png',
            alt: 'Maximize',
            styles: {
                cursor: 'pointer',
            },
            events: {
                click: function() {toggle_maximize(url, width)},
            }
        }));

    image_links.grab(maximize_image);

    // If the image is not bigger than the layout, remove the maximize button
    var big_img = new Element('img', {src: url});
    big_img.addEvent('load', function(event) {
        if (big_img.width <= 690)
            maximize_image.setStyle('display', 'none');
    });
});

function toggle_maximize(url, width) {
    if (maximized)
        main_image.set(
            'src', 
            '${h.thumbnailer(c.image.filename, max_width=690, max_height=700)}');
    else
        main_image.set('src', url);

    maximized = !maximized;
}
</script>
</%def>


<div id="right_col">
  <div id="prevnext">
    % if hasattr(c, 'older') or hasattr(c, 'newer'):
        % if hasattr(c, 'newer'):
            <a href="${h.url(controller='images', action='show', day=c.newer)}" id="previous">
              &larr;
            </a>
        % endif             
        % if hasattr(c, 'older'):
            <a href="${h.url(controller='images', action='show', day=c.older)}" id="next">
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

<ul id="resize_maximize">
  <li>
    <a href="${c.image.url}" target="_blank">
      <img src="/layout_images/save.png" alt="Save image" />
    </a>
  </li>
</ul>

% if hasattr(c, 'older'):
    <a href="${h.url(controller='images', action='show', day=c.older)}">
      <img src="${h.thumbnailer(c.image.filename, max_width=690, max_height=700)}" alt="${c.image.day.strftime('%Y-%m-%d')}" id="main_image" />
    </a>
% else:
    <a href="#">
      <img src="${h.thumbnailer(c.image.filename, max_width=690, max_height=700)}" alt="${c.image.day.strftime('%Y-%m-%d')}" id="main_image" />
    </a>
% endif
