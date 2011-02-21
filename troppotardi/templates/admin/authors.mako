<%inherit file="/admin/base.mako"/>

<%def name="heading()">Authors</%def>

<%def name="title()">${parent.title()} Authors</%def>

% if c.images:
    <% images = list(c.images) %>
    % for image in images:
        % if image.author_url:
            <a href="${image.author_url}">${image.author}</a>
        % else:
            ${image.author}
        % endif
        % if image.author_email:
            - <a href="mailto:${image.author_email}">${image.author_email}</a>
        % endif
        <br/>
    % endfor
% endif
