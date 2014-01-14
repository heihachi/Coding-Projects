import random, string
import urllib2, urllib, re, urlparse
import webbrowser, os, errno

def require_dir(path):
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno != errno.EEXIST:
            raise

url = raw_input("Enter url: ")

boardsearch = re.compile('org/(.*?)/res')
board = boardsearch.search(url)
board = board.group(1)
thread = url.replace('http://', '')
thread = thread.replace('boards.4chan.org/'+board+"/res/", '')



directory = "D:\Coding\Coding-Projects\python\images\\"+board+"\\"+thread
require_dir(directory)

# webshit
counter = 0

http = "http://boards.4chan.org/"+board+"/res/"+thread
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(http,headers=hdr)
html_content = urllib2.urlopen(req).read()

matches = re.findall('href=[\'"]?([^\'" >]+)', html_content)

for url in matches:    
    if (url.find("i.4cdn.org") != -1):
        path = urlparse.urlparse(url).path
        ext = os.path.splitext(path)[1]

        filename = path.replace("/"+board+"/src/", "")

        if(os.path.isfile(directory+'\\'+filename) == False):
            imagelink = "http://i.4cdn.org/"+board+"/src/"+filename
            print("Opening: "+imagelink)
            save = directory+"/"+filename
            urllib.urlretrieve(imagelink, save)
            counter += 1
    
print("Total Images Downloaded: "+str(counter))
