#!/usr/bin/python

import re, sys, cmd
import getopt
import getpass, os.path
import gdata.geo, gdata.media
import gdata.photos.service

INTRO = '-- PicasaCli --'
HELP = '-- Help --'

class PicasaCli(cmd.Cmd):
	def authenticate(self, email, password):
		source = 'PicasaCli'
		self.gd_client = gdata.photos.service.PhotosService()
#		self.gd_client.ClientLogin(email, password, source=source)
		self.gd_client = ''
		self.albums = ''
		self.currAlbum = ''
		self.prompt = ' > '
		self.albumDict = {}

	def do_shell(self, line):
		"Run shell commands"
		if re.match("cd", line):
			dir = line.split()[1]
			try:
				os.chdir(dir)
				print "PWD: ", dir
			except OSError:
				print "No such file/dir :", dir
				return
		else:
			output = os.popen(line).read()
			print output

	def do_EOF(self, line):
		"""Good Bye"""
		print "Good Bye"
		return True

	def postloop(self):
		print

	def emptyline(self):
		print ''

	def getAlbumList(self):
		self.albumDict = {
			"Album 01": ["00001", 10, 'alb01'],
			"Album 02": ["00002", 20, 'alb02'],
			"Album 03": ["00003", 30, 'alb03'],
			"Photo 05": ["00005", 40, 'alb04']
			}
#		self.albums = self.gd_client.GetUserFeed()
#		for album in self.albums.entry:
#			self.albumDict[album.title.text] = [str(album.gphoto_id.text), album.numphotos.text, album]
		
	def do_ls(self, line):
		"""List albums or photos in an album"""
		if self.currAlbum:
			print "Getting list of photos in the album: ", self.currAlbum
#			photos = self.gd_client.GetFeed(
#				'/data/feed/api/user/default/albumid/%s?kind=photo' % (
#				album_id))
#			for photo in photos.entry:
#				print 'Photo title:', photo.title.text
		else:
			print "Getting the list of albums"
			self.getAlbumList()
			print "%19s : Album Title (Num of Pics)" % "Album ID"
			for album in self.albumDict:
				albumID, albumPics = self.albumDict[album][0:2]
				print '%19s : %s (%s)' % (albumID, album, albumPics)

	def do_cd(self, line):
		"""Change to an album or use this album.
Album name can be auto-completed using 'tab', but it has
an issue if the album name has a space.
You can use 'cd ..' or simple 'cd' to go to base dir."""
		self.getAlbumList()
		if line == '..' or line == '':
			print "Going to base dir"
			self.currAlbum = ''
			self.prompt = '> '
		else:
			print "Using the album: ", line
			if self.albumDict.has_key(line.strip()):
				self.currAlbum = line
				self.prompt = '%s> ' % line
			else:
				print "No such album", line

	def complete_cd(self, text, line, begidx, endidx):
		self.getAlbumList()
		if not text:
			List2Return = self.albumDict.keys()[:]
		else:
			List2Return = [ f
							for f in self.albumDict.keys()
							if f.startswith(text)
						]
		return List2Return

	def do_mkdir(self, line):
		"""Create a new album"""
		self.getAlbumList()
		while not line:
			line = raw_input('Album Title [Required]: ')
		if self.albumDict.has_key(line.strip()):
			print "Error: Album name already exists."
		else:
			summary = raw_input('Album Summary [Optional]: ')
			if not summary: summary = 'Created from picasa-cli'
#			self.gd_client.InsertAlbum(title=line, summary=summary)
			print "Created new album:", line

	def do_rm(self, line):
		"""Remove an album"""
		self.getAlbumList()
		if self.albumDict.has_key(line.strip()):
			self.gd_client.Delete(self.albumDict[line][2])
			print "Album:", line, "deleted"
		else:
			print "No such album", line
	
	def do_put(self, line):
		"""Copy photos into an album"""
		pass
	
	def complete_cp(self, text, line, begidx, endidx):
		pass

def main():
	"""FTP like cli for picasa web albums."""
	# Parse command line options
	try:
		opts, files = getopt.getopt(sys.argv[1:], '', ['user=', 'pw=', 'list', 'albumID='])
	except getopt.error, msg:
		print '''
Usage:
	python picasa-cli.py <Options>
Options:
	--user=username		; Use this picasa username
	--pw=password
	--list			; List the albums in picasa-web account
	--albumID=album ID		; Can be found by running only --list

Sample usage:
	bash$ python picasa-cli.py --username=picasa-user --list
	Password: 
	Getting the list of albums
           Album ID : Album Title (Num of Pics)
              00005 : Photo 05 (40)
              00004 : Album 04 (40)
              00003 : Album 03 (30)
              00002 : Album 02 (20)
	
	bash$ python picasa-cli.py --username=picasa-user --albumID=00005 *jpg
	Password:
	Uploading file : pic-01.jpg
	Uploading file : pic-02.jpg
	Uploading file : pic-03.jpg
'''
		sys.exit(2)

	user = ''
	pw = ''
	list = ''
	albumID = ''

	# Process options
	for option, arg in opts:
		if option == '--user':
			user = arg
		elif option == '--pw':
			pw = arg
		elif option == '--list':
			list = 1
		elif option == '--albumID':
			albumID = arg

	if list and albumID:
		print "Error: --list and --aid cannot be used at the same time"
		sys.exit(2)
	if list and files:
		print "Error: --list and --files cannot be used at the same time"
		sys.exit(2)
	if albumID and not files:
		print "Error: you forgot to give the list of files to upload"
		sys.exit(2)
	if not albumID and files:
		print "Error: you forgot to give the album ID to upload the files to"
		sys.exit(2)
		
	while not user:
		user = raw_input('Please enter your username: ')
	while not pw:
		pw = getpass.getpass()
		if not pw:
			print 'Password cannot be blank.'

	cli = PicasaCli()
	try:
		cli.authenticate(user, pw)
	except gdata.service.BadAuthentication:
		print 'Invalid user credentials given.'
		return

	print ("Successfully logged in to Picasa Web.\n")
	if list:
		line = ''
		cli.do_ls(line)
	elif albumID:
		print albumID, files
	else:
		cli.cmdloop()
	
if __name__ == '__main__':
	main()
