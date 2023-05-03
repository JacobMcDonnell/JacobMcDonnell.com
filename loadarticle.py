import db
import sys
import datetime

path = input("Enter path to db entry backup: ")
sys.path.append(path)
import dbbak

r = db.DB()
r.add_article(dbbak.db_entry)
print(r.get_all_keys())
print(r.get_article(dbbak.db_entry['url']))

def gen_item(article):
    date = article["date"].split("/")
    date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
    item = [ '<item>', f'<title>{article["title"]}</title>', f'<guid>https://jacobmcdonnell.com/articles/{article["url"]}/</guid>', f'<link>https://jacobmcdonnell.com/articles/article["url"]/</link>', f'<pubDate>{date.strftime("%d %b %Y")} 00:00:00 -0500</pubDate>', '<description><![CDATA[', article["desc"],']]></description>', '</item>' ]
    return "\n".join(item)

def gen_rss():
    rss = ['<?xml version="1.0" encoding="utf-8"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', '<channel>', '<title>Jacob McDonnell</title>', '<description>Articles from Jacob McDonnell.</description>', '<language>en-us</language>', '<link>https://jacobmcdonnell.com/rss.xml</link>', '<atom:link href="https://jacobmcdonnell.com/rss.xml" rel="self" type="application/rss+xml" />', '<image>', '<title>Jacob McDonnell</title>', '<url>https://jacobmcdonnell.com/favicon.ico</url>', '<link>https://jacobmcdonnell.com/rss.xml</link>', '</image>' ]
    articles = sorted(r.get_all_articles(), reverse=True, key=lambda d: d['id'])
    for article in articles:
        rss.append(gen_item(article))
    rss.append("</channel></rss>")
    rss = "\n".join(rss)
    file = open("static/rss.xml", "w")
    file.write(rss)
    file.close()

rss = input("Do you want to generate a new rss file? [y or n]: ")
if rss == 'y':
    gen_rss()

