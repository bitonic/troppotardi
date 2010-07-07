<%inherit file="/base.mako"/>

${next.body()}

<%def name="title()">${parent.title()}</%def>
<%def name="footer()">${parent.footer()}</%def>
