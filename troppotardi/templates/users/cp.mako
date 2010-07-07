<%inherit file="/users/base.mako"/>

<%def name="title()">${parent.title()} User CP</%def>
<%def name="heading()">User CP</%def>

${h.form(h.url(controller='users', action='cp'), method='POST')}
<b>Old password</b>: ${h.password("password")}<br/>
${h.hidden('username', value=session['user'].username)}
<hr>
New password: ${h.password("newpassword")}<br/>
Confirm new password: ${h.password("confirmpassword")}<br/>
${h.submit('submit', 'Submit')}
${h.end_form()}
