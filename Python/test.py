import urllib2
from bs4 import BeautifulSoup

site = "http://funnyjunk.com"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(site,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)
soup.findAll('img')
print soup
