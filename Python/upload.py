import ClientForm
import urllib2
request = urllib2.Request(
    "http://jamez.dyndns.org/?p=custom&sub=upload")
response = urllib2.urlopen(request)
forms = ClientForm.ParseResponse(response, backwards_compat=False)
response.close()
## f = open("example.html")
## forms = ClientForm.ParseFile(f, "http://example.com/example.html",
##                              backwards_compat=False)
## f.close()
form = forms[0]
print form  # very useful!

# A 'control' is a graphical HTML form widget: a text entry box, a
# dropdown 'select' list, a checkbox, etc.

# Indexing allows setting and retrieval of control values
## original_text = form["comments"]  # a string, NOT a Control instance
## form["comments"] = "Blah."

# Controls that represent lists (checkbox, select and radio lists) are
# ListControl instances.  Their values are sequences of list item names.
# They come in two flavours: single- and multiple-selection:
## form["favorite_cheese"] = ["brie"]  # single
## form["cheeses"] = ["parmesan", "leicester", "cheddar"]  # multi
#  equivalent, but more flexible:
## form.set_value(["parmesan", "leicester", "cheddar"], name="cheeses")

# Add files to FILE controls with .add_file().  Only call this multiple
# times if the server is expecting multiple files.
#  add a file, default value for MIME type, no filename sent to server
## form.add_file(open("data.dat"))
#  add a second file, explicitly giving MIME type, and telling the server
#   what the filename is
## form.add_file(open("data.txt"), "text/plain", "data.txt")

# All Controls may be disabled (equivalent of greyed-out in browser)...
control = form.find_control("comments")
print control.disabled
#  ...or readonly
print control.readonly
#  readonly and disabled attributes can be assigned to
control.disabled = False
#  convenience method, used here to make all controls writable (unless
#   they're disabled):
form.set_all_readonly(False)

control= form.find_control(label="accepted")

print "this is control! "
print control

request2 = form.click()  # urllib2.Request object
try:
    response2 = urllib2.urlopen(request2)
except urllib2.HTTPError, response2:
    pass

print response2.geturl()
print response2.info()  # headers
print response2.read()  # body
response2.close()
