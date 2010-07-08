<%inherit file="/admin/base.mako"/>

<%def name="title()">Admin - Accepted images</%def>

<%def name="heading()">Review accepted images</%def>

% if c.images:
    <% images = list(c.images) %>
    ${h.form(h.url(controller='admin', action='edit_list'), method='POST')}
    <table border=1>
        <tr>
            <th>Image</th>
            <th>Author</th>
            <th>Day</th>
        	<!--<th>Submitted on</th>-->
	        <th>Text</th>
        </tr>
        % for image in images:
        <tr>
            <td>${image.admin_thumb(max_width=200)}</td>
            <td><a href="${image.author_url}">${image.author}</a></td>
            <td>${image.day.strftime("%d-%m-%Y")}</td>
            <!--<td>image.submitted.ctime()</td>-->
            <td>${image.text}</td>
            <td><a href="${h.url(controller='admin', action='edit', id=image.id)}">Edit</a></td>
        </tr>
        % endfor
% else:
    No images to display.
% endif
</table>
