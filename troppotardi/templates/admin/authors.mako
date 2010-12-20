<%inherit file="/admin/base.mako"/>

<%def name="heading()">Authors</%def>

<%def name="title()">${parent.title()} Authors</%def>

% if c.images:
    <% images = list(c.images) %>
    % for image in images:
        ${image.author}
        % if image.author:
            - ${image.author_email}
        % endif
        <br/>
    % endfor
% endif
