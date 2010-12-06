## -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>${self.title()}</title>
    ${self.head()}
</head>
<body>
<div id="wrapper"><div id="container">
    <% flashes = h.flash.pop_messages() %>
    % if flashes:
        % for flash in flashes:
            <div id="flash">
                <span class="message">${flash}</span>
            </div>
        % endfor
    % endif

    ${next.body()}
</div>
<div id="push"></div>
</div>
<div id="footer">${self.footer()}</div>
</body>
</html>

<%def name="title()">troppo tardi - </%def>

<%def name="heading()"></%def>

<%def name="head()">
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="shortcut icon" href="/favicon.ico" />
</%def>
<%def name="footer()"></%def>
