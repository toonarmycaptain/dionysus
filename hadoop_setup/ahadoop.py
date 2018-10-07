#!/usr/bin/python2
print("content-type: text/html")
print("")

print("""
<form action=ahadoop_details.py>
How Many Masters Do You Want?
<br />
<input type='text' name='mno'>
<br />
How Many Slaves Do You Want?
<br />
<input type='text' name='sno'>
<br />
<input type='submit'>
</form>"""
)
