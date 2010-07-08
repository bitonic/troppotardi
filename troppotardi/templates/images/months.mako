<%inherit file="/images/base.mako"/>

<%def name="title()">${parent.title()} Images by month</%def>

% if c.images:
    <div id="months">
    <%
    images = list(c.images)
    month = None
    %>
        <ul>
        % for image in images:
            % if (not month) or (image.day.month != month) or (image.day.year != year):
                <%
                month = image.day.month
                year = image.day.year
                %>
                <li class="month">
                ${image.day.strftime('%B %Y')}
                </li>
            % endif
        <li>
            <a href="${h.url(controller='images', action='show', day=h.day_to_str(image.day))}">
            ${image.day.strftime('%d')}
            </a>
        </li>
        % endfor
    </ul>
    </div>
% endif
  
