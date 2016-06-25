#!/usr/bin/python3
import feedparser
import sqlite3
import time
from datetime import datetime

conn = sqlite3.connect('feeds.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Feeds(item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Title TEXT, Category TEXT, Published TEXT UNIQUE, Link TEXT)''')
def get_feeds():

	feed = feedparser.parse('http://www.insomnia.gr/index.php?app=core&module=global&section=rss&type=classifieds&wanted=0')
	for key in feed['entries']:
		
		Title = key['title']
		Category = key['category']
		Published = datetime.strptime(key['published'], '%a, %d %b %Y %H:%M:%S +0000')
		Link = key['link']
		print(Title)
		#items.append([title, category, published, link])
		c.execute ('''INSERT OR IGNORE INTO Feeds(Title, Category, Published, Link) VALUES (?, ?, ?, ?)''', (Title, Category, Published, Link))
		conn.commit()


while True:
	print("Getting new items every 5 min ...")
	print("*****")
	get_feeds()
	print("*****")
	time.sleep(300)
