#!/usr/bin/python3
#
#  Feedsomnia.py
#  
#  Copyright 2017 Yiannis Souchis <obionar@gmail.com>

version = '0.3.1' 

from tkinter import *
from tkinter import ttk
import sqlite3, os, platform, webbrowser, requests, io, wget

root = Tk()

## Functions ###########################################################

if not os.path.exists('feedsomnia.db'):
	print("First time RUN. Getting latest feeds:")
	wget.download('http://feedsomnia.online/feedsomnia.db')


conn = sqlite3.connect('feedsomnia.db')
c = conn.cursor()


def go(*event):
	global count
	count = 0
	site = ''
	keyword = entry_keyword.get()
	category = entry_category.get()
	desc = entry_desc.get()
	tree.delete(*tree.get_children())
	
	if v.get() == 1:
		site = 'aggeliopolis'
	if v.get() == 2:
		site = 'car'
	if v.get() == 3:
		site = 'insomnia'
	if v.get() == 4:
		site = 'noiz'

	fetch = c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' AND Category LIKE '%{}%' AND Site LIKE '%{}%' AND Desc LIKE '%{}%' ORDER BY Date ASC'''.format(keyword, category, site, desc))

	for r in fetch:
		tree.insert("" , 0, text=r[6], values=(r[1], r[3], r[2], r[5], r[7]))
		count += 1
	var.set(str(count) + " latest items in list")


def click(*event):
	item = tree.selection()[0]
	url = tree.item(item, "text")
	f = c.execute('''SELECT * FROM Feeds WHERE Link LIKE '%{}%' '''.format(url))
	for r in f:
		description = r[9]
	insert_log(description)


def insert_log(what):
	logs.config(state="normal")
	logs.delete(1.0, END)
	logs.insert(END, what)
	logs.insert(END, '\n\n')
	logs.config(state="disabled")


def doubleclick(*event):
	item = tree.selection()[0]
	url = tree.item(item, "text")
	webbrowser.open_new_tab(url)


def db():
	def get_db():
		global conn, c
		try:
			print()
			conn.close()
			os.remove('feedsomnia.db')
		except:
			pass
		
		wget.download('http://feedsomnia.online/feedsomnia.db')
		conn = sqlite3.connect('feedsomnia.db')
		c = conn.cursor()
		insert_log("Database updated!")
		go()
	root.after(1000, get_db)

## Interface ###########################################################

# Toolbar
toolbar = ttk.Frame(root)
toolbar.pack(fill=X, padx=8, pady=8)

# Search Entry
Label(toolbar, text=" Find: ").pack(side="left")
entry_keyword = ttk.Entry(toolbar)
entry_keyword.bind("<KeyRelease>", go)
entry_keyword.pack(side=LEFT)

# Category Entry
Label(toolbar, text=" in category: ").pack(side="left")
entry_category = ttk.Entry(toolbar)
entry_category.bind("<KeyRelease>", go)
entry_category.pack(side=LEFT)

# Category Entry
Label(toolbar, text=" in description: ").pack(side="left")
entry_desc = ttk.Entry(toolbar)
entry_desc.bind("<KeyRelease>", go)
entry_desc.pack(side=LEFT)

toolbar2 = ttk.Frame(root)
toolbar2.pack(fill=X)

# Site Selector
v = IntVar()
Label(toolbar2, text=" Site: ").pack(side="left")
ttk.Radiobutton(toolbar2, text=" ALL ", variable=v, value=0, command=go).pack(side=LEFT)
ttk.Radiobutton(toolbar2, text=" aggeliopolis.gr ", variable=v, value=1, command=go).pack(side=LEFT)
ttk.Radiobutton(toolbar2, text=" car.gr ", variable=v, value=2, command=go).pack(side=LEFT)
ttk.Radiobutton(toolbar2, text=" insomnia.gr ", variable=v, value=3, command=go).pack(side=LEFT)
ttk.Radiobutton(toolbar2, text=" smart.noiz.gr ", variable=v, value=4, command=go).pack(side=LEFT)

ttk.Button(toolbar2, text="Update Feeds", command=db).pack(side=RIGHT)

# middle container
mid = ttk.Frame(root)

# Tree
tree = ttk.Treeview(mid)
tree["columns"]=("title", "price", "category", "date", "site")
tree.pack(side=LEFT, expand=YES, fill=BOTH)

tree.column("#0", width=0, stretch=NO) #Hidden URL
tree.column("title", minwidth=300, width=400)
tree.column("price", width=90, stretch=NO)
tree.column("category", width=170, stretch=NO)
tree.column("date", width=130, stretch=NO)
tree.column("site", width=100, stretch=NO)

tree.heading("#0", text="url")
tree.heading("title", text="Title")
tree.heading("price", text="Price")
tree.heading("category", text="Category")
tree.heading("date", text="Published")
tree.heading("site", text="in Site")
tree.insert("" , 0, text="dummy", values=())
tree.bind("<Double-1>", doubleclick)
tree.bind('<ButtonRelease-1>', click)

# Scroll
scrollbar = ttk.Scrollbar(mid)
scrollbar.pack(side=LEFT, fill=Y)
tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

# Notificator Sidebar
sidebar = ttk.Frame(mid, relief=SUNKEN)


logs = Text(sidebar, state=DISABLED, wrap=WORD, height=20, width=40)
logs.pack(side="top")

ttk.Button(sidebar, text="Open in Browser", command=doubleclick).pack(side="bottom")


sidebar.pack(side="left", padx=4, pady=4, fill=BOTH)
mid.pack(expand=YES, fill=BOTH)

# Statusbar
statusbar = ttk.Frame(root,height=20)
var = StringVar()
Label(statusbar, textvariable=var).pack(side="left")
statusbar.pack(fill=X, padx=4, pady=4)
go()

insert_log("Hello!")

root.title("Feedsomnia v0.3.1")
root.minsize(700, 300)
root.mainloop()

########################################################################
