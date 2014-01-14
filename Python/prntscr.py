import random, string
import urllib2, urllib, re, urlparse
import webbrowser, os, errno

def require_dir(path):
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno != errno.EEXIST:
            raise
def url_contruct():
    string = []
    for x in range(0,5):
        test = randpart()
        string.append(test)
    return ''.join(string)
def randpart():
    r = random.randint(1,1001)
    if(r > 500):
        r1 = str(random.randint(0,9))
    else:
        r1 = str(random.choice(string.letters))
    return r1

#folder
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/")
require_dir(directory)

# webshit
counter = 0
while(counter != 50):
    test = url_contruct()
    http = "http://prntscr.com/"+test
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(http,headers=hdr)
    html_content = urllib2.urlopen(req).read()

    matches = re.findall('src=[\'"]?([^\'" >]+)', html_content)
    
    #print(len(matches))
    for url in matches:
        if (url.find("imageshack.") != -1 or url.find("imgur") != -1):
            #webbrowser.open_new_tab(url)

            path = urlparse.urlparse(url).path
            ext = os.path.splitext(path)[1]

            urllib.urlretrieve(url, directory+test+ext)
            print("Opening: "+http)
            counter += 1
    
