#!/usr/bin/python3
import feedparser
import sqlite3
import time

conn = sqlite3.connect('feeds.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Feeds(Title TEXT, Category TEXT, Published TEXT UNIQUE, Link TEXT)')

def get_feeds():
	feed = feedparser.parse('http://www.insomnia.gr/index.php?app=core&module=global&section=rss&type=classifieds&wanted=0')
	for key in feed['entries']:
		Title = key['title']
		Category = key['category']
		Published = key['published']
		Link = key['link']
		#items.append([title, category, published, link])
		c.execute ('INSERT OR IGNORE INTO Feeds VALUES(?, ?, ?, ?)', (Title, Category, Published, Link))
		conn.commit()

while True:
	print("Getting new items every 5 min ...")
	get_feeds()
	time.sleep(300)
