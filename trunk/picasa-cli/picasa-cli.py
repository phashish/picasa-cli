#!/usr/bin/python
#
# picasa-cli
# Ashish Disawal
# I have modified the google docs example, available at:
# http://gdata-python-client.googlecode.com/svn/trunk/samples/docs/docs_example.py (r882)
# which was licensed under the Apache License, Version 2.0.
# I have licensed this code under GPL v2.
# Thanks to Jeff Fisher and Eric Bidelman for docs_example.py
# For more info go to : http://ashish.disawal.blogspot.com

import re
import sys
import getopt
import getpass
import os.path
import gdata.geo
import gdata.media
import gdata.photos.service

class PicasaCli(object):
	"""A picasa web photo list feed."""

	def __init__(self, email, password):
		"""Constructor for the PicasaCli object.
		Takes an email and password corresponding to a gmail account.
		Args:
		  email: [string] The e-mail address of the account to use for the sample.
		  password: [string] The password corresponding to the account specified by
		  the email parameter.
		Returns:
		  A PicasaCli object.
		"""
		source = 'PicasaCli'
		self.gd_client = gdata.photos.service.PhotosService()
		self.gd_client.ClientLogin(email, password, source=source)
		self.albums = ''

	def _GetCmd(self):
		""" Gets user input and returns a list"""
		input = ''
		while input == '':
			input = raw_input('> ')
		return input.split()

	# cmd 01: help
	def _PrintHelp(self):
		print ('\nCurrently supported commands:\n'
			'help, quit\n'
			'Local commands: lcwd, lcd, lls\n'
			'PicasaWeb commands: lsalbums, mkalbum\n'
			"Commands yet to be implimented:\n"
			'put, get .. and many more\n')

	# cmd 02: lcwd
	def _LocalCWD(self):
		"""Prints current local working directory"""
		print os.getcwd()

	# cmd 03: lcd
	def _LocalCD(self, cmd):
		"""Changes the local working directory"""
		try:
			dir = cmd[1]
		except IndexError:
			print "Usage: lcd /local/path/to/cd"
			return
		try:
			os.chdir(dir)
		except OSError:
			print "No such directory or you don't have permissions to access it."
			return
		print "Current local dir: ", os.getcwd()

	# cmd 04: lls
	def _LocalList(self, cmd):
		"""Lists contents on a local directory"""
		try:
			dir = cmd[1]
		except IndexError:
			dir = '.'
		for file in os.listdir(dir):
			print file

	# cmd 05: lsalbums
	def _ListAlbums(self):
		print "Getting the list of albums ... "
		self.albums = self.gd_client.GetUserFeed()
		print "%19s : Album Title (Num of Pics)" % "Album ID"
		for self.album in self.albums.entry:
			print '%s : %s (%s)' % (self.album.gphoto_id.text, self.album.title.text, self.album.numphotos.text)
	
	# cmd 06: mkalbum
	def _MakeAlbum(self):
		title = ''
		while not title:
			title = raw_input('Album Title [Required]: ')
		summary = raw_input('Album Summary [Optional]: ')
		if not summary: summary = 'Created from picasa-cli'
		new_album = self.gd_client.InsertAlbum(title=title, summary=summary)
		print "New album %s created" % title

	# cmd 07: rmalbum
	def _RemoveAlbum(self):
		self.albums = self.gd_client.GetUserFeed()
		print "Title of the album to delete:"
		title = raw_input('Title: ')
		for self.album in self.albums.entry:
			if self.album.title.text == title:
				album_found = 1
				print "Deleting album : %s" % title
				self.gd_client.Delete(self.album)
				break
			else:
				album_found = 0
		if album_found == 0:
			print "No such album: %s" % title

	# cmd 08: lspics
	def _ListPics(self, cmd):
		print "Listing pics from album"
		
	def Run(self):
		"""Prompts the user to choose funtionality to be demonstrated."""
		try:
			while True:
				cmd = self._GetCmd()
				# cmd 01:
				if   cmd[0] == 'help':
					self._PrintHelp()
				# Commands for local system.
				# cmd 02:
				elif cmd[0] == 'lcwd':
					self._LocalCWD()
				# cmd 03:
				elif cmd[0] == 'lcd':
					self._LocalCD(cmd)
				# cmd 04:
				elif cmd[0] == 'lls':
					self._LocalList(cmd)
				# Commands for picasaweb
				# cmd 05:
				elif cmd[0] == 'lsalbums':
					self._ListAlbums()
				# cmd 06:
				elif cmd[0] == 'mkalbum':
					self._MakeAlbum()
				# cmd 07:
				elif cmd[0] == 'rmalbum':
					self._RemoveAlbum()
				# cmd 08:
				elif cmd[0] == 'lspics':
					self._ListPics(cmd)
				elif cmd[0] == 'quit':
					print '\nGoodbye.'
					return
		except KeyboardInterrupt:
			print '\nGoodbye.'
			return

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
	key = ''
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

	try:
		cli = PicasaCli(user, pw)
	except gdata.service.BadAuthentication:
		print 'Invalid user credentials given.'
		return

	print ("Successfully logged in to Picasa Web.\n"
		   "Type 'help' for list of available commands.\n")
	cli.Run()

if __name__ == '__main__':
	main()
