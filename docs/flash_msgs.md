Message Flashing
flask.flash(message, category='message')
Flashes a message to the next request. In order to remove the flashed message from the session and to display it to the user, the template has to call get_flashed_messages().

Parameters:
*message* (str) – the message to be flashed.

*category* (str) – the category for the message, any kind of string can be used as category. The following values are recommended:   
**message** for any kind of message   
**error** for errors   
**info** for information messages   
**warning** for warnings   

Return type:
None

