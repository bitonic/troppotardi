<%inherit file="/admin/base.mako"/>

<%def name="title()">Admin - Accepted images</%def>

<%def name="heading()">Review accepted images</%def>

% if c.images:
    <% images = list(c.images) %>
    ${h.form(h.url(controller='admin', action='accepted'), method='POST')}
    <table border=1>
        <tr>
            <th>Image</th>
            <th>Author</th>
	    <th>Author Email</th>
            <th>Day</th>
            <th>Submitted on</th>
            <th>Text</th>
	    <th>Edit</th>
	    <th>Delete</th>
        </tr>
        % for image in images:
        <tr>
            <td><img src="${h.thumbnailer(image.filename, max_width=200)}"/></td>
            <td><a href="${image.author_url}">${image.author}</a></td>
	    <td>${image.author_email}</td>
            <td>${image.day.strftime("%d-%m-%Y")}</td>
            <td>${image.submitted.ctime()}</td>
            <td>${image.text}</td>
            <td><a href="${h.url(controller='admin', action='edit', id=image.id)}">Edit</a></td>
            <td>${h.checkbox('delete', value=image.id, checked=False)}</td>
        </tr>
        % endfor
</table>
	${h.submit('submit', 'Delete')}
	${h.end_form()}
% else:
    No images to display.
% endif
