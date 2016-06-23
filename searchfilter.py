#!/usr/bin/python3
import sqlite3
from tkinter import *
from tkinter import ttk

# SQLite Connection
conn = sqlite3.connect('feeds.db')
c = conn.cursor()

class Filter(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.toolbar = ttk.Frame(self)
		self.toolbar.pack(fill=X, padx=4, pady=4)
		self.entry = ttk.Entry(self.toolbar)
		self.entry.bind_all("<KeyPress>", self.on_button)
		self.button = ttk.Button(self.toolbar, text="Exit", command=self.quit)
		self.entry.pack(side=LEFT, padx=4, pady=4)
		self.button.pack(side=LEFT, padx=4, pady=4)
		
		self.listbox = Listbox(self)
		self.listbox.pack(side=LEFT, fill=BOTH, expand=2)
		self.scrollbar = ttk.Scrollbar(self)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)

	def on_button(self, event):
		self.listbox.delete(0,END)
		c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' ORDER BY Published DESC'''.format(self.entry.get()))
		for row in c.fetchall():	
			self.listbox.insert(END, row[0])

app = Filter()
app.mainloop()


