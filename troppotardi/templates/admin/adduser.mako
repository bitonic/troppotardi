<%inherit file="/admin/base.mako"/>

<%def name="title()">Admin - Add user</%def>

<%def name="heading()">Adding user</%def>


${h.form(h.url(controller='admin', action='adduser'), method='POST')}

Username: ${h.text("username")}<br/>
Email: ${h.text("email")}<br/>
Role: ${h.select("role", c.roles[-1], [[role, role] for role in c.roles])}<br/>
${h.submit('submit', 'Submit')}
${h.end_form()}
