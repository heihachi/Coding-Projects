#import urllib2
#import bs4
#page = bs4.BeautifulSoup(urllib2.urlopen("http://www.truewow.org"))
#page.findAll('img')


import HTMLParser
class MyParse(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="img":
            print(dict(attrs)["src"])

h=MyParse()
page=open("truewow.org").read()
h.feed(page)