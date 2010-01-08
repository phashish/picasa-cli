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
		self.gd_client.ClientLogin(email, password, source=source)
	#	self.gd_client = ''
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
				retur
		else:
			output = os.popen(line).read()
			print output

	def do_EOF(self, line):
		print "Good Bye"
		return True

	def postloop(self):
		print

	def emptyline(self):
		print ''

	def getAlbumList(self):
			self.albums = self.gd_client.GetUserFeed()
			for album in self.albums.entry:
				self.albumDict[album.title.text] = ':'.join([album.gphoto_id.text, album.numphotos.text])
		
	def do_ls(self, line):
		"""List albums or photos in an album"""
		if self.currAlbum:
			print "Getting list of photos in the album: ", self.currAlbum
			photos = self.gd_client.GetFeed(
				'/data/feed/api/user/default/albumid/%s?kind=photo' % (
				self.albumDict[self.currAlbum].split(':')[0]))
			for photo in photos.entry:
				print 'Photo title:', photo.title.text
		else:
			print "Getting the list of albums"
			self.getAlbumList()
			print "%19s : Album Title (Num of Pics)" % "Album ID"
			for album in self.albumDict:
				albumID, albumPics = self.albumDict[album].split(':')
				print '%s : %s (%s)' % (albumID, album, albumPics)

	def do_cd(self, line):
		"""Change to an album or use this album
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
		"""Creating new album"""
		self.getAlbumList()
		while not line:
			line = raw_input('Album Title [Required]: ')
		if self.albumDict.has_key(line.strip()):
			print "Error: Album name already exists."
		else:
			summary = raw_input('Album Summary [Optional]: ')
			if not summary: summary = 'Created from picasa-cli'
			self.gd_client.InsertAlbum(title=line, summary=summary)
			print "Created new album:", line, ":"
	
	def do_rm(self, line):
		"""Remove an album"""
		while not line:
			line = raw_input('Album Title [Required]: ')
		if self.albumDict.has_key(line.strip()):
			self.gd_client.Delete(line)
			print "Deleted album: ", line
		else:
			print "No such album: ", line


def main():
	"""FTP like cli for picasa web albums."""
	# Parse command line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw='])
	except getopt.error, msg:
		print 'python picasa-cli.py --user [username] --pw [password] '
		sys.exit(2)

	user = ''
	pw = ''

	# Process options
	for option, arg in opts:
		if option == '--user':
			user = arg
		elif option == '--pw':
			pw = arg

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

	print ("Successfully logged in to Picasa Web.\n"
		   "Type 'help' for list of available commands.\n")
	cli.cmdloop()

if __name__ == '__main__':
	main()
