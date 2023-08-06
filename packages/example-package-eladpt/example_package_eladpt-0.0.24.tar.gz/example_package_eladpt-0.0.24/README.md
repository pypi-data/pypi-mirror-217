# Testing


<a href="javascript:alert(document.location);">XSS</a> // or
<b style="width: expression(alert(document.location));">XSS</b> // or
<form action="javascript:alert(document.location);"><input type="submit" /></form>