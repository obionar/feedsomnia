#!/usr/bin/python3
import sqlite3
import os

conn = sqlite3.connect('feeds.db')
c = conn.cursor()
search_keyword = ''
search_category = ''

def get_help():
	print("""Usage:
Enter to show all content or some keyword to search for items and press Enter
h to show this help.
x to exit""")

def search_filter(search_keyword):
	c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%'
				ORDER BY Published DESC'''.format(search_keyword))
	for row in c.fetchall():
		print("Title:", row[0])
		print("Category:", row[1])
		print("Link:", row[3])
		print()

def cli():
	print("\n Hi! Enter your search term or press h to Help.")
	while True:
		command = input("command: ")
		os.system('clear')
		print("\n**************************************** \n")
		if command == 'c':
			c.execute('''SELECT Category FROM Feeds ORDER BY Category''')
			print("All Categories:")
			for row in c.fetchall():
				print(row[0])
		elif command == 'h':
			get_help()
		elif command == 'x':
			print("Bye!")
			break
		else:
			search_filter(command)
		print("\n**************************************** \n")

cli()
