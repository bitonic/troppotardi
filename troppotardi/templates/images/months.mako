<%inherit file="/layout.mako"/>

<%def name="title()">${parent.title()} Images by month</%def>

% if c.images:
    <div id="months">
    <%
    images = list(c.images)
    month = None
    year = None
    %>
        <ul>
        % for image in images:
	    % if (not year) or (image.day.year != year):
                <%
                year = image.day.year
                %>
                <li class="month">
                    ${image.day.strftime('%Y')}
                </li>
            % endif
            % if (not month) or (image.day.month != month):
                <%
                month = image.day.month
                %>
                <li class="month">
                    ${h.literal(image.day.strftime('%B'))}
                </li>
            % endif
        <li>
            <a href="${h.url(controller='images', action='show', day=h.day_to_str(image.day))}"><img src="${h.thumbnailer(image.filename, max_width=122, max_height=122, crop=True)}" alt="${image.author} - ${image.day.strftime('%d-%m-%Y')}"/></a>
        </li>
        % endfor
    </ul>
    <hr/>
    </div>
% endif
  
