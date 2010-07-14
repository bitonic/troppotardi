<%inherit file="/base.mako"/>

${next.body()}

<%def name="title()">${parent.title()}</%def>

<%def name="footer()">
<a href="${h.url(controller='images', action='months')}">Archive</a> &middot;
<a href="${h.url(controller='images', action='submit')}" class="submitlink">Submit Image</a> &middot;
<a href="${h.url(controller='pages', action='index', page='about')}">About</a> &middot;
<a href="http://bitbucket.org/rostayob/troppotardi/" target="_blank">Source</a> &middot;
<a href="${h.url('home')}">Home</a>
</%def>

<%def name="head()">
${parent.head()}
<link href="${h.url('feed', qualified=True)}" rel="alternate" title="troppotardi.com Image Feed" type="application/atom+xml" /> 
<script src="/js/cufon-yui.js" type="text/javascript"></script>
<script src="/js/Consolas_400-Consolas_700-Consolas_italic_400.font.js" type="text/javascript"></script>
<script type="text/javascript">
Cufon.replace('#about');
Cufon.replace('#text');
Cufon.replace('#submit-form');
Cufon.replace('#previous');
Cufon.replace('#next');
Cufon.replace('#footer');
Cufon.replace('#months');
Cufon.replace('#flash');
</script>
${h.stylesheet_link('/css/base.css')}
${h.google_analytics()}
</%def>
