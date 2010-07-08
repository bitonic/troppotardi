<%inherit file="/base.mako"/>

${next.body()}

<%def name="title()">${parent.title()}</%def>

<%def name="footer()">
<a href="${h.url(controller='images', action='months')}">Archive</a> &middot;
<a href="${h.url(controller='images', action='submit')}" class="submitlink">Submit Image</a> &middot;
<a href="${h.url(controller='pages', action='index', page='about')}">About</a> &middot;
<a href="http://bitbucket.org/rostayob/troppotardi/">Source</a> &middot;
<a href="/">Home</a>
</%def>
