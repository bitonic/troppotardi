<%inherit file="/layout.mako"/>

<%def name="title()">${parent.title()} ${c.image.author}</%def>

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
