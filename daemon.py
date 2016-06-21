#!/usr/bin/python3
import feedparser
import sqlite3
import time

conn = sqlite3.connect('feeds.db')
c = conn.cursor()

def create_table():
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
create_table()

while True:
	print("Getting RSS")
	get_feeds()
	print("Wait...")
	time.sleep(30)
