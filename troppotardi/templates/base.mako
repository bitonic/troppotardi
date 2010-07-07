## -*- coding: utf-8 -*-

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
  "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
  <title>${self.title()}</title>
  ${self.head()}
</head>
<body>
<div id="container">
  <% flashes = h.flash.pop_messages() %>
  % if flashes:
    % for flash in flashes:
        <div id="flash">
          <span class="message">${flash}</span>
        </div>
    % endfor
  % endif

  ${next.body()}
  <div id="footer">${self.footer()}</div>
</div>
</body>
</html>

<%def name="title()">troppo tardi - </%def>
<%def name="heading()"></%def>
<%def name="head()">
<link rel="shortcut icon" href="/favicon.ico" />
<script src="/js/cufon-yui.js" type="text/javascript"></script>
<!--<script src="/js/VeraMono_400-VeraMono_700-VeraMono_oblique_400.font.js" type="text/javascript"></script>-->
<script src="/js/Courier_400-Courier_700-Courier_italic_400.font.js" type="text/javascript"></script>
<script type="text/javascript">
Cufon.replace('#about');
Cufon.replace('#text');
Cufon.replace('#submit-form');
Cufon.replace('#previous');
Cufon.replace('#next');
Cufon.replace('#footer');
Cufon.replace('#months');
</script>
<!--
<script src="/js/mootools-1.2.4-core-nc.js" type="text/javascript"></script>
<script src="/js/mootools-1.2.4.4-more.js" type="text/javascript"></script>
<script src="/js/main.js" type="text/javascript"></script>
-->
${h.stylesheet_link('/css/base.css')}
</%def>
<%def name="footer()"></%def>
