from Tkinter import *
import tkFont

root = Tk()

fonts=list(tkFont.families())
fonts.sort()

display = Listbox(root)
display.pack(fill=BOTH, expand=YES, side=LEFT)

scroll = Scrollbar(root)
scroll.pack(side=RIGHT, fill=Y, expand=NO)

scroll.configure(command=display.yview)
display.configure(yscrollcommand=scroll.set)

for item in fonts:
    display.insert(END, item)

root.mainloop()
