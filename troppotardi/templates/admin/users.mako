<%inherit file="/admin/base.mako"/>

<%def name="heading()">Users</%def>

<%def name="title()">${parent.title()} Users</%def>

% if c.users:
    <% users = list(c.users) %>
    <table border=1>
        <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
        </tr>
    % for user in users:
        <tr>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
            <td>
                <a href="${url(controller='admin', action='edit_user', id=user.id)}">
                    Edit</a>
            </td>
        </tr>
    % endfor
    </table>
% endif
