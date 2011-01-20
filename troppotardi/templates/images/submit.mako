<%inherit file="/layout.mako"/>

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
   theme : 'custom',
   custom_theme_widget: 'recaptcha_widget'
};
</script>
</%def>

<div id="submit-form">
  ${h.form(h.url(controller="images", action="submit"), method="post", multipart=True)}
  <ul>
    <li><b>bold</b> = required field<br/></li>
    <li><b>Max image size: 3MB</b></li>
    <li class="mandatory">Image to submit: ${h.file("image_file")}</li>
    <li class="mandatory">Your name: ${h.text("author")}</li>
    <li>Your website: ${h.text("author_url")}</li>
    <li>Short description/title about the image:<br/>
      ${h.text("text", id="textinput")}</li>
    <li>Email: ${h.text("email")}<br/>If you want to be notified that your image has been accepted</li>
    <li class="mandatory">
      By hitting "submit", you certify that you have the rights
      to publish the image you are uploading.</li>
    
    <li id="recaptcha_widget" style="display:none">
      
      <div class="recaptcha_only_if_incorrect_sol" style="color:red">Incorrect please try again</div>
      <span class="recaptcha_only_if_image">Type the two words on the right:</span>
      <span class="recaptcha_only_if_audio">Input the numbers you hear:</span>
      <div id="recaptcha_image" style="float:right"></div>
      
      <input type="text" id="recaptcha_response_field" name="recaptcha_response_field" />
      
      <div id="captcha_links">
	<span><a href="javascript:Recaptcha.reload()">Reload</a> - </span>
	<span class="recaptcha_only_if_image"><a href="javascript:Recaptcha.switch_type('audio')">Audio</a></span>
	<span class="recaptcha_only_if_audio"><a href="javascript:Recaptcha.switch_type('image')">Image</a></span>
      </div>
    </li>
    
    <script type="text/javascript"
	    src="http://www.google.com/recaptcha/api/challenge?k=${c.recaptcha_key}">
    </script>
    <noscript>
      <iframe src="http://www.google.com/recaptcha/api/noscript?k=${c.recaptcha_key}"
	      height="300" width="500" frameborder="0"></iframe><br>
      <textarea name="recaptcha_challenge_field" rows="3" cols="40">
      </textarea>
      <input type="hidden" name="recaptcha_response_field"
	     value="manual_challenge">
    </noscript>
    
    <li id="submit_button">
      <input type="image" src="/layout_images/submit.png" alt="Submit" />
    </li>
  </ul>
  ${h.end_form()}
</div>
