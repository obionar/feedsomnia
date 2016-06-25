#!/usr/bin/python3
import sqlite3
from tkinter import *
from tkinter import ttk
import webbrowser
import time
from datetime import datetime

# SQLite Connection
conn = sqlite3.connect('feeds.db')
c = conn.cursor()

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
		self.button = ttk.Button(self.toolbar, text="Refresh", command=self.get_results)
		self.button.pack(side=LEFT, padx=4, pady=4)

		# quit button
		self.button = ttk.Button(self.toolbar, text="Quit", command=self.quit)
		self.button.pack(side=RIGHT, padx=4, pady=4)

		# **** AUTOREFRESH TODO!!! *****
		#self.autorefresh_var = IntVar()
		#self.autorefresh_check = ttk.Checkbutton(self.toolbar, text="Autorefresh", ) #variable=self.autorefresh_var, command=self.autorefresh)
		#self.autorefresh_check.pack(side=RIGHT)

		# TreeView
		self.tree = ttk.Treeview(self)
		self.tree.pack(side=LEFT, expand=YES, fill=BOTH)
		self.tree["columns"]=("item_id", "title", "category","date")

		self.tree.column("#0", width=0, stretch=NO) #Hidden URL
		self.tree.column("item_id", width=0, stretch=NO)
		self.tree.column("title", width=500)
		self.tree.column("category", width=180, stretch=NO)
		self.tree.column("date", width=150, stretch=NO)

		self.tree.heading("#0", text="")
		self.tree.heading("item_id", text="ID")
		self.tree.heading("title", text="Title")
		self.tree.heading("category", text="Category")
		self.tree.heading("date", text="Published")

		# double click on item to open it in web browser
		self.tree.bind("<Double-1>", self.double_click)

		# scrollbar
		self.scrollbar = ttk.Scrollbar(self)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		self.tree.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.tree.yview)

	#double click on item
	def double_click(self, event):
		item = self.tree.selection()[0]
		print("you clicked on", self.tree.item(item,"text"))
		open_url = self.tree.item(item,"text")
		webbrowser.open_new_tab(open_url)

	# get results
	def get_results(self, *event):
		self.after(120000, self.get_results) # list autorefresh every 2 minutes
		self.tree.delete(*self.tree.get_children())
		self.get_entry = self.entry.get()
		if len(self.get_entry) > 0:
			c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' ORDER BY Published ASC'''.format(self.get_entry))
			for row in c.fetchall():
				self.tree.insert("" , 0, text=row[4], values=(row[0], row[1], row[2], row[3]))

		

app = Feedsomnia()
app.title("Feedsomnia")
app.minsize(width=400, height=300)
app.mainloop()

update_clock(self)
