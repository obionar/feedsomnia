#!/usr/bin/python3
import time
import feedparser
import sqlite3
import webbrowser
from tkinter import *
from tkinter import ttk
from datetime import datetime
from time import gmtime, strftime

url = 'http://www.insomnia.gr/index.php?app=core&module=global&section=rss&type=classifieds&wanted=0'

# SQLite Connection
conn = sqlite3.connect('feeds.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Feeds(item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
			Title TEXT, Category TEXT, Published TEXT UNIQUE, Link TEXT)''')


class Feedsomnia(Tk):
	def __init__(self):
		Tk.__init__(self)
		
		# toolbar
		self.toolbar = ttk.Frame(self)
		self.toolbar.pack(fill=X, padx=4, pady=4)

		# search entry
		self.entry = ttk.Entry(self.toolbar)
		self.entry.bind_all("<KeyPress>", self.get_results) # <KeyPress>
		self.entry.pack(side=LEFT, padx=4, pady=4)

		# refresh button
		self.btn_refresh = ttk.Button(self.toolbar, text="Update Feeds", command=self.update_db)
		self.btn_refresh.pack(side=LEFT, padx=4, pady=4)

		# quit button
		self.button = ttk.Button(self.toolbar, text="Quit", command=self.quit)
		self.button.pack(side=RIGHT, padx=4, pady=4)


		# middle area
		self.content = ttk.Frame(self)
		self.content.pack(expand=YES, fill=BOTH)

		# TreeView
		self.tree = ttk.Treeview(self.content)
		self.tree.pack(side=LEFT, expand=YES, fill=BOTH)
		self.tree["columns"]=("title", "category","date")

		self.tree.column("#0", width=0, stretch=NO) #Hidden URL
		self.tree.column("title", minwidth=300, width=400)
		self.tree.column("category", width=170, stretch=NO)
		self.tree.column("date", width=150, stretch=NO)

		self.tree.heading("#0", text="")
		self.tree.heading("title", text="Title")
		self.tree.heading("category", text="Category")
		self.tree.heading("date", text="Published")

		# double click on item to open it in web browser
		self.tree.bind("<Double-1>", self.double_click)

		# scrollbar
		self.scrollbar = ttk.Scrollbar(self.content)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		self.tree.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.tree.yview)
		
		# statusbar
		self.labelvar = StringVar()
		self.statusbar = Label(self, textvariable = self.labelvar, bd=1, relief=SUNKEN, anchor=W, pady=4, padx=8)
		self.statusbar.pack(side=BOTTOM, fill=X)

	#double click on item
	def double_click(self, event):
		item = self.tree.selection()[0]
		print("you clicked on - ", self.tree.item(item,"text"))
		open_url = self.tree.item(item,"text")
		webbrowser.open_new_tab(open_url)

	# update db
	def update_db(self):
		print("getting feeds.. ")
		self.tree.delete(*self.tree.get_children())
		feed = feedparser.parse(url)
		for key in feed['entries']:
			Title = key['title']
			Category = key['category']
			Published = datetime.strptime(key['published'], '%a, %d %b %Y %H:%M:%S +0000')
			Link = key['link']
			#print(Title)
			c.execute ('''INSERT OR IGNORE INTO Feeds(Title, Category, Published, Link) VALUES (?, ?, ?, ?)''', 
				(Title, Category, Published, Link))
		c.execute('''SELECT * FROM Feeds''')
		self.itemscount = len(c.fetchall())
		print (self.itemscount)
		self.labelvar.set("Currently {} Items in database".format(self.itemscount))
		conn.commit()
		
		print("\n({}) Database updated \n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
		self.get_results()
		self.after(600000, self.update_db) #auto update db every 10 minutes

	# get results
	def get_results(self, *event):
		self.tree.delete(*self.tree.get_children())
		self.get_entry = self.entry.get()
		if len(self.get_entry) > 0:
			c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' ORDER BY Published ASC'''.format(self.get_entry))
			for row in c.fetchall():
				self.tree.insert("" , 0, text=row[4], values=(' * ' + row[1], row[2], row[3]))
			



app = Feedsomnia()
app.title("Feedsomnia v0.1")
app.minsize(width=800, height=400)
app.update_db() #get new feeds at startup
app.mainloop()
