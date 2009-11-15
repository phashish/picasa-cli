#!/usr/bin/python

import gdata.photos.service
import gdata.media
import gdata.geo
import getopt
import getpass
import sys
import os.path

email = raw_input('Please enter your username: ')
pw = getpass.getpass()

gd_client = gdata.photos.service.PhotosService()
gd_client.email = email		# Set your Picasaweb e-mail address...
gd_client.password = pw		# ... and password
gd_client.source = 'api-sample-google-com'
gd_client.ProgrammaticLogin()

print "Logged in .."
if sys.argv[1] == 'list':
	print "Getting the list ... "
	albums = gd_client.GetUserFeed()
	print "List of current albums :"
	for album in albums.entry:
		print 'title: %-45s, num of pics: %-4s, id: %s' % (album.title.text, album.numphotos.text, album.gphoto_id.text)
	sys.exit(0)

aid = sys.argv[1]
files = sys.argv[2:]

album_url = '/data/feed/api/user/%s/albumid/%s' % (gd_client.email, aid)
for file in files:
	print file, os.path.basename(file)
	name = os.path.basename(file)
	f = open(file)
	photo = gd_client.InsertPhotoSimple(album_url, name,'', f, content_type='image/jpeg')
	f.close()
