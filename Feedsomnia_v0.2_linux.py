#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
#import wget
import sqlite3
import webbrowser
import os

os.system("rm feeds.db")
os.system("wget http://212.24.100.49/feedsomnia/feeds.db")
conn = sqlite3.connect('feeds.db')
c = conn.cursor()

class Feedsomnia(Tk):
	def __init__(self):
		Tk.__init__(self)

		# toolbar
		self.toolbar = ttk.Frame(self)
		self.toolbar.pack(fill=X, padx=4, pady=4)

		# search entry
		self.search_label = ttk.Label(self.toolbar, text="Search keyword: ").pack(side=LEFT, padx=4, pady=4)
		self.keyword_entry = ttk.Entry(self.toolbar)
		self.keyword_entry.bind_all("<KeyPress>", self.get_results) # <KeyPress>
		self.keyword_entry.pack(side=LEFT, padx=4, pady=4)

		# category entry
		self.search_label = ttk.Label(self.toolbar, text="in category:").pack(side=LEFT, padx=4, pady=4)
		self.cat_entry = ttk.Entry(self.toolbar)
		self.cat_entry.bind_all("<KeyPress>", self.get_results) # <KeyPress>
		self.cat_entry.pack(side=LEFT, padx=4, pady=4)

		# refresh button
		self.btn_refresh = ttk.Button(self.toolbar, text="Update Feeds", command=self.get_results)
		self.btn_refresh.pack(side=RIGHT, padx=4, pady=4)

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

	# get results
	def get_results(self, *event):
		self.tree.delete(*self.tree.get_children())
		self.get_keyword = self.keyword_entry.get()
		self.get_category = self.cat_entry.get()
		#if len(self.get_entry) >= 1:
		c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' AND Category LIKE '%{}%' ORDER BY Published ASC'''.format(self.get_keyword, self.get_category))
		for row in c.fetchall():
			self.tree.insert("" , 0, text=row[4], values=(' * ' + row[0], row[1], row[2], row[3]))

	#double click on item
	def double_click(self, event):
		item = self.tree.selection()[0]
		print("you clicked on - ", self.tree.item(item,"text"))
		open_url = self.tree.item(item,"text")
		webbrowser.open_new_tab(open_url)
	
	

app = Feedsomnia()
app.title("Feedsomnia v0.2.1")
app.minsize(width=800, height=200)
app.get_results()
#app.update_db() #get new feeds at startup
app.mainloop()
