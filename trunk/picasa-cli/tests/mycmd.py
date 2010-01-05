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
				retur
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
			"Album01": "00001:10",
			"Album02": "00002:20",
			"Album03": "00003:30",
			"Album04": "00004:40"
			}
#			self.albums = self.gd_client.GetUserFeed()
#			for album in self.albums.entry:
#				self.albumDict[album.title.text] = ':'.join([album.gphoto_id.text, album.numphotos.text])
		
	def do_ls(self, line):
		"""List albums or photos in an album"""
		if self.currAlbum:
			print "Getting list of photos in the album: ", self.currAlbum
#			photos = self.gd_client.GetFeed(
#				'/data/feed/api/user/default/albumid/%s?kind=photo' % (
#				album_id))
		else:
			print "Getting the list of albums"
			self.getAlbumList()
			print "%19s : Album Title (Num of Pics)" % "Album ID"
			for album in self.albumDict:
				albumID, albumPics = self.albumDict[album].split(':')
				print '%19s : %s (%s)' % (albumID, album, albumPics)

	def completedefault(self, text, line, bigidx, endidx):
		self.getAlbumList()
		list2Return = []
		for i in self.albumDict.keys():
			if i.startswith(text):
				list2Return.append(i)
		return list2Return
				
	def do_cd(self, line):
		"""Change to an album or use this album.
You can use 'cd ..' or simple 'cd' to go to base dir."""
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

	def do_mkdir(self, line):
		"""Create a new album"""
		print "Creating new album: ", line
	
	def do_rm(self, line):
		"""Remove an album"""
		print "Removing:", line

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
