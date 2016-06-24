#!/usr/bin/python3
import sqlite3
from tkinter import *
from tkinter import ttk
import time

# SQLite Connection
conn = sqlite3.connect('feeds.db')
c = conn.cursor()

class Filter(Tk):
	def __init__(self):
		Tk.__init__(self)
		
		# toolbar
		self.toolbar = ttk.Frame(self)
		self.toolbar.pack(fill=X, padx=4, pady=4)
		
		# search entry
		self.entry = ttk.Entry(self.toolbar)
		self.entry.bind_all("<KeyPress>", self.get_results)
		self.entry.pack(side=LEFT, padx=4, pady=4)
		
		# refresh button
		self.button = ttk.Button(self.toolbar, text="Refresh", command=self.get_results)
		self.button.pack(side=LEFT, padx=4, pady=4)
		
		# **** AUTOREFRESH TODO!!! *****
		self.autorefresh_var = IntVar()
		self.autorefresh_check = ttk.Checkbutton(self.toolbar, text="Autorefresh", variable=self.autorefresh_var) #command=self.autorefresh)
		self.autorefresh_check.pack(side=RIGHT)
		
		# TreeView
		self.tree = ttk.Treeview(self)
		self.tree["columns"]=("category","date")
		self.tree.column("#0", minwidth=0,width=400)
		self.tree.column("category", minwidth=0,width=140)
		self.tree.column("date", minwidth=0, width=220)
		self.tree.heading("#0", text="Title")
		self.tree.heading("category", text="Category")
		self.tree.heading("date", text="Published")
		self.tree.pack(side=LEFT, expand=YES, fill=BOTH)
			
		# scroll
		self.scrollbar = ttk.Scrollbar(self)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		
		# scroll config
		self.tree.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.tree.yview)
	
	# get results
	def get_results(self, *event):
		self.tree.delete(*self.tree.get_children())
		self.get_entry = self.entry.get()

		if len(self.get_entry) > 2:
			c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' ORDER BY Published DESC'''.format(self.get_entry))
			for row in c.fetchall():
				self.tree.insert("" , 0,    text=row[0], values=(row[1], row[2]))

app = Filter()
app.title("Feedsomnia")
app.minsize(width=400, height=300)
app.mainloop()


