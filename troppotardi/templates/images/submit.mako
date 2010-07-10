<%inherit file="/images/base.mako"/>

<%def name="title()">${parent.title()} Submit an image</%def>

<%def name="head()">${parent.head()}
<style type="text/css">
/* reCAPTCHA styling */
.error-message {
    float:right;
    color:red;
    font-size:80%;
    font-weight:bold;
    position:relative;
    margin-left:-100px;
}
</style>
<script type="text/javascript">
var RecaptchaOptions = {
   theme : 'white'
};
</script>
</%def>

<div id="submit-form">
    ${h.form(h.url(controller="images", action="submit"), method="post", multipart=True)}
    <ul>
        <li><b>bold</b> = required field<br/></li>
        <li class="mandatory">Image to submit: ${h.file("image_file")}</li>
        <li class="mandatory">Your name: ${h.text("author")}</li>
        <li>Your website: ${h.text("author_url")}</li>
        <li>Short description/title about the image:<br/>
            ${h.text("text", id="textinput")}</li>
	<li>Email: ${h.text("email")}<br/>If you want to be notified that your image has been accepted</li>
	<li class="mandatory">
	    By hitting "submit", you certify that you have the rights
	    to publish the image you are uploading.</li>
        <li class="captcha">
            <script type="text/javascript" src="http://api.recaptcha.net/challenge?k=${c.recaptcha_key}"></script>
            <noscript>
                <iframe src="http://api.recaptcha.net/noscript?k=${c.recaptcha_key}" height="300" width="500" frameborder="0"></iframe><br/>
                <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
                <input type="hidden" name="recaptcha_response_field" value="manual_challenge"/>
            </noscript>
        </li>
        <li id="submit_button">
            <input type="image" src="/layout_images/submit.png" alt="Submit" />
        </li>
    </ul>
    ${h.end_form()}
</div>
