from tkinter import *
import random

fontsize = 25
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'cyan', 'purple']


def onSpam():
    popup = Toplevel()
    color = random.choice(colors)
    Label(popup, text='Popup', bg='black', fg=color).pack(fill=BOTH)
    mainLabel.config(fg=color)


def onFlip():
    mainLabel.config(fg=random.choice(colors))
    main.after(100, onFlip)


def onGrow():
    global fontsize
    fontsize +=3
    mainLabel.config(font=('arial', fontsize, 'italic'))
    main.after(100, onGrow)


main = Tk()
mainLabel = Label(main, text='Fun GUI!', relief=RAISED)
mainLabel.config(font=('arial', fontsize, 'italic'), fg='cyan', bg='navy')
mainLabel.pack(side=TOP, expand=YES, fill=BOTH)

Button(main, text='Spam', command=onSpam).pack(fill=X)
Button(main, text='Flip', command=onFlip).pack(fill=X)
Button(main, text='Grow', command=onGrow).pack(fill=X)

main.mainloop()
