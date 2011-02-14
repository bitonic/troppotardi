<%inherit file="/admin/base.mako"/>

<%def name="head()">
${parent.head()}
<script type="text/javascript" src="http://mazzo.li/jslibs/mootools-1.3-yc.js"></script>
<script type="text/javascript">
function checkAll() {
    $$('.del_checkbox').each(function(el) {
        el.checked = true;
    });
}

function uncheckAll() {
    $$('.del_checkbox').each(function(el) {
        el.checked = false;
    });
}
</script>
</%def>

<%def name="title()">${parent.title()} Deleted images</%def>

<%def name="heading()">Review deleted images</%def>

% if c.images:
    <p>
      <a href="javascript:checkAll();">Check all</a> &middot; <a href="javascript:uncheckAll();">Uncheck all</a>
    </p>

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
            <td><a href="${image.url}"><img src="${h.thumbnailer(image.filename, max_width=200)}" /></a></td>
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
            <td><input name="delete" type="checkbox" value="${image.id}" class="del_checkbox" /></td>
            <td><a href="${h.url(controller='admin', action='edit', id=image.id)}">Edit</a></td>
        </tr>
    % endfor
    </table>
    ${h.submit('submit', 'Delete')}
    ${h.end_form()}
% else:
    <p>No images to display.</p>
% endif
