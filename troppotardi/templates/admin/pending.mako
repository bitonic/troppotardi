<%inherit file="/admin/base.mako"/>

<%def name="title()">${parent.title()} Pending images</%def>

<%def name="heading()">Review pending images</%def>

% if c.images:
    <span class="warning">Delete will have priority, so if you tick accept AND delete, the image will be deleted.</b></span> <br/>
    <% images = list(c.images) %>
    ${h.form(h.url(controller='admin', action='pending'), method='POST')}
    <table border=1>
        <tr>
            <th>Image</th>
            <th>Author</th>
	    <th>Author Email</th>
            <th>Submitted on</th>
            <th>Text</th>
            <th>Delete</th>
            <th>Accept</th>
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
            <td>${h.checkbox('accept', value=image.id, checked=False)}</td>
            <td><a href="${h.url(controller='admin', action='edit', id=image.id)}">Edit</a></td>
        </tr>
    % endfor
    </table>
    ${h.submit('submit', 'Save')}
    ${h.end_form()}
% else:
    No images to display.
% endif

