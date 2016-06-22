#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
import sqlite3
import os

# SQLite Connection
conn = sqlite3.connect('feeds.db')
c = conn.cursor()

# Functions
def search_filter():
    c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' ORDER BY Published DESC'''.format(search_box.get()))
    for row in c.fetchall():
        search_results.insert(END, row[0])
        print(row[0])

#    for row in c.fetchall():
#        print("Title:", row[0])
#        print("Category:", row[1])
#        print("Link:", row[3])
#        print()

# tkinter GUI
root = Tk()
root.wm_title("Feedsomnia")

# **** Toolbar ****
toolbar = ttk.Frame(root)
search_label = Label(toolbar, text="Filter: ")
search_label.pack(side=LEFT)
search_box = ttk.Entry(toolbar)
search_box.pack(side=LEFT, padx=4, pady=4)
search_button = ttk.Button(toolbar, text="Search", command=search_filter)
search_button.pack(side=LEFT, padx=4, pady=4)
#search_autorefresh = Checkbutton(toolbar, text="Autorefresh")
#search_autorefresh.pack(side=LEFT, padx=4, pady=4)
exit_button = ttk.Button(toolbar, text="Exit", command=root.quit)
exit_button.pack(side=LEFT, padx=4, pady=4)
toolbar.pack(side=TOP, fill=X)

# **** Insomnia Logo ****
img = PhotoImage(file="insomnia.png")
imglabel = Label(root, image=img)
imglabel.pack(pady=10)

# **** Search Results ****
scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
search_results = Listbox(root)
search_results.pack( fill=BOTH, expand=2)
scrollbar.config(command=search_results.yview)

# **** Statusbar ****
status = Label(root, text="Preparing to do nothing!", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
root.mainloop()
