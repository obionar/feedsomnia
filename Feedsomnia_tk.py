#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import time
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
			Title TEXT, Price TEXT, Category TEXT, Published TEXT, Link TEXT UNIQUE)''')

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
		self.tree["columns"]=("title", "price", "category", "date")

		self.tree.column("#0", width=0, stretch=NO) #Hidden URL
		self.tree.column("title", minwidth=300, width=400)
		self.tree.column("price", width=90, stretch=NO)
		self.tree.column("category", width=170, stretch=NO)
		self.tree.column("date", width=150, stretch=NO)

		self.tree.heading("#0", text="")
		self.tree.heading("title", text="Title")
		self.tree.heading("price", text="Price")
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

	def update_db(self):
		print("getting feeds.. ")
		self.tree.delete(*self.tree.get_children())
		page_source = requests.get('http://www.insomnia.gr/classifieds/latest/')
		soup = BeautifulSoup(page_source.text)
		table = soup.find("table")
		for row in table.findAll("tr"):
			col	 = row.findAll("td")
			if len(col) == 4:
				Title = col[1].find("a").text
				Link = col[1].find('a')["href"]
				Price = col[3].text
				Category = col[1].findAll('li')[3].text
				Published = strftime("%Y-%m-%d %H:%M:%S", gmtime())
				c.execute ('''INSERT OR IGNORE INTO Feeds(Title, Price, Category, Published, Link) VALUES (?, ?, ?, ?, ?)''', 
				(Title, Price, Category, Published, Link))
		# show number of items
		c.execute('''SELECT * FROM Feeds''')
		self.itemscount = len(c.fetchall())
		self.labelvar.set("Currently {} Items in database".format(self.itemscount))
		conn.commit()	
		print("\n({}) Database updated. {} items in\n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), self.itemscount))
		self.get_results()
		
		#auto update db every 10 minutes
		self.after(600000, self.update_db) 

	# get results
	def get_results(self, *event):
		self.tree.delete(*self.tree.get_children())
		self.get_entry = self.entry.get()
		if len(self.get_entry) >= 0:
			c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' ORDER BY Published ASC'''.format(self.get_entry))
			for row in c.fetchall():
				self.tree.insert("" , 0, text=row[5], values=(' * ' + row[1], row[2], row[3], row[4]))

app = Feedsomnia()
app.title("Feedsomnia v0.1")
app.minsize(width=800, height=400)
app.update_db() #get new feeds at startup
app.mainloop()
