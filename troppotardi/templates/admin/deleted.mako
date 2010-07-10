<%inherit file="/admin/base.mako"/>

<%def name="title()">${parent.title()} Deleted images</%def>

<%def name="heading()">Review deleted images</%def>

% if c.images:
    <% images = list(c.images) %>
    ${h.form(h.url(controller='admin', action='deleted'), method='POST')}
    <table border=1>
        <tr>
            <th>Image</th>
            <th>Author</th>
	    <th>Author Email</th>
            <th>Submitted on</th>
            <th>Text</th>
	    % if session['user'].has_permission('delete_images'):
                <th>Delete permanently</th>
            % endif
        </tr>
    % for image in images:
        <tr>
            <td>${image.admin_thumb(max_width=200)}</td>
            <td>
	        % if image.author_url:
	            <a href="${image.author_url}">${image.author}</a></td>
	        % else:
	            ${image.author}
	        % endif
	    </td>
	    <td>${image.author_email}</td>
            <td>${image.submitted.ctime()}</td>
            <td>${image.text}</td>
            <td>${h.checkbox('delete', value=image.id, checked=False)}</td>
            <td><a href="${h.url(controller='admin', action='edit', id=image.id)}">Edit</a></td>
        </tr>
    % endfor
    </table>
    ${h.submit('submit', 'Delete')}
    ${h.end_form()}
% else:
    No images to display.
% endif
