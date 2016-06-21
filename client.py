#!/usr/bin/python3
import sqlite3

conn = sqlite3.connect('feeds.db')
c = conn.cursor()

while True:
	print("*********************")
	keyword = input("enter keyword or press ENTER to show all: ")
	print("*********************")
	c.execute('''SELECT * FROM Feeds WHERE Title LIKE '%{}%' ORDER BY Published DESC'''.format(keyword))
	for row in c.fetchall():
		print("Title:", row[0])
		print("Category:", row[1])
		print("Link:", row[3])
		print()
