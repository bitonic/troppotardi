<%inherit file="/base.mako"/>

${next.body()}

<%def name="title()">${parent.title()}</%def>

<%def name="footer()">
<a href="${h.url(controller='images', action='submit')}" class="submitlink">Submit Image</a> &middot;
<a href="${h.url(controller='images', action='months')}">Archive</a> &middot;
<!--<a href="${h.url(controller='pages', action='index', page='about')}">Join us</a> &middot;-->
<a href="${h.url(controller='pages', action='index', page='joinus')}">Join us</a> &middot;
<a href="http://bitbucket.org/rostayob/troppotardi/" target="_blank">Source</a> &middot;
<a href="${h.url('index')}">Home</a>
</%def>

<%def name="head()">
${parent.head()}
<link href="${h.url('feed', qualified=True)}" rel="alternate" title="troppotardi.com Image Feed" type="application/atom+xml" /> 
${h.stylesheet_link('/css/base.css')}
${h.google_analytics()}
</%def>
