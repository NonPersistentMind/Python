#!/usr/bin/python3
import cgi
import os
import sys
import shelve

def debug(*vals):
    print('====================================', file=sys.stderr)
    print(*vals, file=sys.stderr)
    print('====================================', file=sys.stderr)
    pass

shelveName = 'class-shelve'
fieldnames = ('name', 'age', 'job', 'pay')

form = cgi.FieldStorage()
print('Content-type: text/html')
# When server launches this script, current WD is the WD of the server
#                                                                       =>
# for script to see Parent class inside this directory, it must be explicitly included
sys.path.insert(0, os.getcwd())


# main HTML template
mainTemplate = """
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>People Input Form</title>
</head>

<body>
    <form method="POST" action="peoplecgi.py">
        <table>
            $ROWS$
        </table>
        <p></p>
        <input type=submit value="Fetch", name=action>
        <input type=submit value="Update", name=action>
    </form>
</body>

</html>
"""

templateRow = '<tr><th>%s<td><input type=text name=%s value="%%(%s)s">\n'
templateRows = ''
for field in (('key',) + fieldnames):
    templateRows += templateRow % ((field, )*3)
# mainTemplate = mainTemplate.replace('$ROWS$', templateRows)


def htmlize(adict):
    new_dict = adict.copy()
    key_val = new_dict['key']
    for key in new_dict:
        value = new_dict[key]
        new_dict[key] = cgi.escape(repr(value))

    new_dict['key'] = key_val
    return new_dict


def fetchRecord(db, form):
    try:
        key = form['key'].value
        record = db[key]
        fields = record.__dict__
        fields['key'] = key
    except:
        fields = dict.fromkeys(fieldnames, '?')
        fields['key'] = 'Missing or invalid key!'

    return fields


def updateRecord(db, form):
    if not 'key' in form:
        fields = dict.fromkeys(fieldnames, '???')
        fields['key'] = 'Missing key argument'
    else:
        key = form['key'].value
        if key in db:
            record = db[key]
        else:
            from person_start import Person
            record = Person('?', '?')

        for field in fieldnames:
            val = form[field].value
            try:
                val = eval(val)
            except:
                pass
            setattr(record, field, val)

        db[key] = record
        fields = record.__dict__
        fields['key'] = key

    return fields


db = shelve.open(shelveName)


action = form['action'].value if 'action' in form else None
if action=='Fetch':
    debug('Goes into Fetch')
    fields = fetchRecord(db, form)
elif action=='Update':
    debug('Goes into Update')
    fields = updateRecord(db, form)
else:
    debug('Goes into None')
    fields = dict.fromkeys(fieldnames, '???')
    fields['key'] = 'Missing or invalid action!'

db.close()
val = templateRows % htmlize(fields)
print(mainTemplate.replace('$ROWS',val))


