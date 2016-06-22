#!/usr/bin/python3
from tkinter import *
import sqlite3
import os

# SQLite Connection
conn = sqlite3.connect('feeds.db')
c = conn.cursor()

# Functions
def search_filter():
    c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' ORDER BY Published ASC'''.format(search_box.get()))
    os.system('clear')

    print("\n******************** Search Results for: {} ********************\n".format(search_box.get()))

    for row in c.fetchall():
        print("Title:", row[0])
        print("Category:", row[1])
        print("Link:", row[3])
        print()

# tkinter GUI
root = Tk()
root.wm_title("Feedsomnia")

# **** Toolbar ****
toolbar = Frame(root, bd=1, relief=SUNKEN)
#search_label = Label(toolbar, text="Filter: ")
#search_label.pack(side=LEFT)
search_box = Entry(toolbar)
search_box.pack(side=LEFT, padx=4, pady=4)
search_button = Button(toolbar, text="Search", command=search_filter)
search_button.pack(side=LEFT, padx=4, pady=4)
#search_autorefresh = Checkbutton(toolbar, text="Autorefresh")
#search_autorefresh.pack(side=LEFT, padx=4, pady=4)
exit_button = Button(toolbar, text="Exit", command=root.quit)
exit_button.pack(side=LEFT, padx=4, pady=4)
toolbar.pack(side=TOP, fill=X)
# Todo: Show me search results here!

img = PhotoImage(file="insomnia.png")
imglabel = Label(root, image=img)
imglabel.pack(pady=10)

# **** Statusbar ****
status = Label(root, text="Preparing to do nothing!", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
root.mainloop()
