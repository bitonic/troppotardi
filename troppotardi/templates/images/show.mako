<%inherit file="/images/base.mako"/>

<%def name="title()">${parent.title()} ${c.image.author}</%def>

<div id="text">
    <b>
    % if c.image.author_url:
        <a href="${c.image.author_url}">${c.image.author}</a>
    % else:
        ${c.image.author}
    % endif
    </b>
     - ${c.image.day.strftime("%d.%m.%Y")}
    % if c.image.text:
        <br/><span id="descr">${c.image.text}</span>
    % endif
</div>

% if hasattr(c, 'older') or hasattr(c, 'newer'):
    <div id="prevnext">
    % if hasattr(c, 'newer'):
        <div id="previous">
            <a href="${h.url(controller='images', action='show', day=c.newer)}">newer</a>
        </div>
    % endif
    % if hasattr(c, 'older'):
        <div id="next">
            <a href="${h.url(controller='images', action='show', day=c.older)}">older</a>
        </div>
    % endif
    </div>
% endif

<div id="img_div">
    <a href="${c.image.url}">
        <img src="${h.thumbnailer(c.image.filename, max_width=590)}" alt="${c.image.day}" id="image" />
    </a>
</div>
