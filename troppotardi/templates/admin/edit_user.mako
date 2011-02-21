<%inherit file="/admin/base.mako"/>

<%def name="heading()">Editing user ${c.user.username}</%def>

<%def name="title()">${parent.title()} Editing ${c.user.username}</%def>

${h.form(h.url(controller='admin', action='edit_user', id=c.user.id), method='POST')}
Username: ${h.text("username", value=c.user.username)}<br/>
Email: ${h.text("email", value=c.user.email)}<br/>
Role: ${h.select("role", c.user.role, [[role, role] for role in c.roles])}<br/><br/>
Password: ${h.password("password")}</br>
Confirm password: ${h.password("confirm_password")}<br/><br/>
${h.submit('submit', 'Submit')}
${h.end_form()}
<a href="${h.url(controller='admin', action='delete_user', id=c.user.id)}">Delete user</a>
