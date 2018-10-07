#!/usr/bin/python2
print("content-type: text/html")
print("")

import commands as sp
import os
import cgi

form=cgi.FormContent()
fh=open('hosts','w')
fi=open('ips','w')
fh.write("[master]\n")
for i in form.keys():
	if 'mip' in i:
                fi.write(i+':' + " " + form[i][0] + "\n")
		fh.write(form[i][0] + ' ansible-ssh-user=root ' + "\n")
		
fh.write("[slave]\n")

for j in form.keys():
	if 'sip' in j:
		fh.write(form[j][0] + "\n")
fh.close()
fi.close()
a=sp.getoutput("sudo ansible-playbook nm.yml -i hosts")
b=sp.getoutput("sudo ansible-playbook sm.yml -i hosts")
print("<pre>")
print(a)
print(b)
print("</pre>")
