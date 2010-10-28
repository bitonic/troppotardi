%if c.images:
<?xml version="1.0" encoding="UTF-8" ?>
<images>
%for image in list(c.images):
    <image>
        <image_url>${h.url('/', qualified=True)[:-1]}${image.url}</image_url>
        <author>${image.author}</author>
        <author_url>${image.author_url}</author_url>
        <date>${image.day.strftime("%Y-%m-%d")}</date>
    </image>
%endfor
</images>
%endif
