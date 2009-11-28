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
		while True:
			input = raw_input('> ')
			return str(input)

	def _PrintHelp(self):
		"""Displays help of commands for the user to choose from."""
		print ('\nCurrently supported commands:\n'
			'help, quit, lcwd, lcd, lls, ls, cd\n'
			"Commands yet to be implimented:\n"
			'list, mkalbm, put, get .. and many more\n')

	def _LocalCWD(self):
		print os.getcwd()

	def _LocalCD(self, dir):
		try:
			os.chdir(dir)
		except OSError:
			print "No such directory or you don't have permissions to access it."
			return
		print "Current local dir: ", os.getcwd()

	def _LocalList(self, dir):
		for dirname in os.listdir(dir):
			print dirname

	def _ListAlbums(self):
		print "Getting the list of albums ... "
	
	def _ListPics(self, albumid):
		print "List of photos in ", albumid

	def Run(self):
		"""Prompts the user to choose funtionality to be demonstrated."""
		try:
			while True:
				cmd = self._GetCmd()
				if cmd == 'help':
					self._PrintHelp()
				# Commands for local system.
				elif cmd == 'lcwd':
					self._LocalCWD()
				elif re.match("^lcd", cmd):
					dir = re.findall(r'^lcd (\S+)', cmd)[0]
					self._LocalCD(dir)
				elif re.match("^lls", cmd):
					try:
						dir = re.findall(r'^lls (\S+)', cmd)[0]
					except IndexError:
						dir = '.'
					self._LocalList(dir)
				# Commands for picasaweb
				elif cmd == 'lsalbm':
					self._ListAlbums()
				elif re.match("^lspics", cmd):
					albumid = re.findall(r'^lspics (\S+)', cmd)[0]
					self._ListPics(albumid)
				elif cmd == 'quit':
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
