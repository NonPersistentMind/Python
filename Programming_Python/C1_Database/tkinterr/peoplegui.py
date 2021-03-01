from tkinter import *
from tkinter.messagebox import showerror
import shelve

shelvename = 'class-shelve'
fieldnames = ('name', 'age', 'job', 'pay')


def makeWidgets(db):
    window = Tk()
    window.title('People Shelve')
    form = Frame(window)
    form.pack()
    entries = {}
    for (index, title) in enumerate(('key', ) + fieldnames):
        label = Label(form, text=title)
        entry = Entry(form)
        label.grid(row=index, column=0)
        entry.grid(row=index, column=1)
        entries[title] = entry
    Button(window, text='Fetch', command=lambda: fetchRecord(
        db, entries)).pack(side=LEFT)
    Button(window, text='Update', command=lambda: updateRecord(
        db, entries)).pack(side=LEFT)
    Button(window, text='Quit', command=lambda: windowQuit(window, db)).pack(side=LEFT)
    return window


def fetchRecord(db, entries):
    key = entries['key'].get()
    try:
        record = db[key]
    except:
        showerror(title='Search Error', message='No such entry!')
    else:
        for field in fieldnames:
            entries[field].delete(0, END)
            entries[field].insert(0, repr(getattr(record, field)))


def updateRecord(db, entries):
    key = entries['key'].get()

    if key in db:
        record = db[key]
    else:
        from person_start import Person
        record = Person('', '')
    for field in fieldnames:
        value = entries[field].get()
        try:
            value = eval(value)
        except:
            pass
        setattr(record, field, value)

    db[key] = record


def windowQuit(window, db):
    window.quit()
    db.close()


if __name__ == "__main__":
    db = shelve.open(shelvename)
    window = makeWidgets(db)
    window.mainloop()
