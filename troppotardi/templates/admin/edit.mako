<%inherit file="/admin/base.mako"/>

<%def name="title()">Admin - Editing image ${c.image.id}</%def>

<%def name="heading()">Editing image ${c.image.id}</%def>

${h.form(h.url(controller='admin', action='edit', id=c.image.id), method='POST')}

Text:<br/>${h.textarea("text", cols=50, rows=10, content=c.image.text)}<br/>
Author: ${h.text("author", value=c.image.author)}<br/>
Author website: ${h.text("author_url", value=c.image.author_url)}<br/>
<hr/>

<%
if c.image.day:
    state = 'accepted'
else:
    state = 'pending'
%>

State of the image: ${h.select("state", state, [['pending', 'Pending'], ['accepted', 'Accepted']])}
<br/>

${h.submit("submit", "Submit")}
${h.end_form()}
${h.image(c.image.url, None)}
