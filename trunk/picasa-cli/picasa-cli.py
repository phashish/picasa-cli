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

	def _GetCmd(self):
		input = ''
		while input == '':
			input = raw_input('> ')
		return input.split()

	# cmd 01: help
	def _PrintHelp(self):
		"""Displays help of commands for the user to choose from."""
		print ('\nCurrently supported commands:\n'
			'help, quit, lcwd, lcd, lls, ls, cd\n'
			"Commands yet to be implimented:\n"
			'list, mkalbm, put, get .. and many more\n')

	# cmd 02: lcwd
	def _LocalCWD(self):
		print os.getcwd()

	# cmd 03: lcd
	def _LocalCD(self, cmd):
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
		try:
			dir = cmd[1]
		except IndexError:
			dir = '.'
		for file in os.listdir(dir):
			print file

	# cmd 05: lsalbums
	def _ListAlbums(self):
		print "Getting the list of albums ... "
		albums = self.gd_client.GetUserFeed()
		for album in albums.entry:
			print 'Title: %-40s, Photos: %4s, ID: %19s' % (album.title.text, album.numphotos.text, album.gphoto_id.text)
	
	# cmd 06: mkalbum
	def _MakeAlbum(self, cmd):
		try:
			opts, args = getopt.getopt(cmd[1:], 't:s:', ['title=', 'summary='])
		except getopt.error, msg:
			print "Usage: mkalbm -t='title here' -s='summary here'"
			return
		title = ''
		sumry = 'Created from picasa-cli'

		for opt, arg in opts:
			if opt in ("-t", "--title"):
				title = arg
			elif opt in ("-s", "--summary"):
				sumry = arg

		print "Trying to create '%s' album .." % title

		new_album = self.gd_client.InsertAlbum(title=title, summary=sumry)
		print "New album %s created" % title

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
				elif cmd[0] == 'lsalbum':
					self._ListAlbums()
				# cmd 06:
				elif cmd[0] == 'mkalbum':
					self._MakeAlbum(cmd)
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
