<%inherit file="/base.mako"/>

<h2>${self.heading()}</h2>

<div id="container">
${next.body()}
</div>

<%def name="head()">${h.stylesheet_link('/css/admin.css')}</%def>

<%def name="title()">${parent.title()} Admin - </%def>

<%def name="footer()">
Logged in as ${session['user'].username}.
<a href="${h.url(controller='users', action='logout')}">Logout</a>
${parent.footer()} <br/>
<a href="${url(controller='admin', action='pending')}">Review pending images</a> | 
<a href="${url(controller='admin', action='accepted')}">Review accepted images</a>
% if session['user'].role == 'Admin':
| <a href="${url(controller='admin', action='adduser')}">Add an user</a> |
<a href="${url(controller='admin', action='users')}">Manage users</a>
% endif
</%def>
