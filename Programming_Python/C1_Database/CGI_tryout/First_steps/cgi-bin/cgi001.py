#!/usr/bin/python3
import cgi, os, sys
form = cgi.FieldStorage()
print('Content-type: text/html\n')
print('<title>Reply Page</title>')

if not 'user' in form:
    print('<h1> Who are you? </h1>')
    print(os.getcwd(), file=sys.stdout)
else:
    print('<h1>Hello %s !</h1>' % cgi.escape(form['user'].value))