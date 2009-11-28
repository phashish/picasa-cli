#!/usr/bin/python
#
import re
import sys
import getopt
import getpass
import os.path

class Cli(object):

	def __init__(self, user):
		self.user = user
	def _GetCmd(self):
		while True:
			input = raw_input('> ')
			print input
			return str(input)

	def _PrintHelp(self):
		"""Displays help of commands for the user to choose from."""
		print ('\nCurrently supported commands:\n'
			'help, quit, lcwd, lcd\n'
			"Commands yet to be implimented:\n"
			'ls, mkdir, cd, put, get .. and many more\n')

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
					dir = re.findall(r'^lls (\S+)', cmd)[0]
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
	# Parse command line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], '', ['user='])
	except getopt.error, msg:
		print 'python picasa-cli.py --user [username] '
		sys.exit(2)

	user = ''
	key = ''
	# Process options
	for option, arg in opts:
		if option == '--user':
			user = arg

	while not user:
		user = raw_input('Please enter your username: ')
#	while not pw:
#		pw = getpass.getpass()
#		if not pw:
#			print 'Password cannot be blank.'

	try:
		cli = Cli(user)
	except gdata.service.BadAuthentication:
		print 'Invalid user credentials given.'
		return

	print ("Successfully logged in.\n"
		   "Type 'help' for list of available commands.\n")
	cli.Run()

if __name__ == '__main__':
	main()
