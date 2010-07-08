## -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
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
<script src="/js/Courier_400-Courier_700-Courier_italic_400.font.js" type="text/javascript"></script>
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
</%def>
<%def name="footer()"></%def>
