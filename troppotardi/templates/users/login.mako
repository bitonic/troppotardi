<%inherit file="/base.mako"/>

<%def name="title()">${parent.title()} Login</%def>

<%def name="heading()">Login</%def>

${h.form(h.url(controller="users", action="login"), method="POST")}
Username: ${h.text("username")}<br/>
Password: ${h.password("password")}<br/>
${h.submit("submit", "Login")}
${h.end_form()}

