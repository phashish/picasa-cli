#!/usr/bin/python
import re
import sys
import getopt
import getpass
import os.path

class Cli(object):
	def __init__(self, user):
		self.user = user
	def _GetCmd(self):
		input = ''
		while input == '':
			input = raw_input('> ')
		return input.split()

	def _PrintHelp(self):
		"""Displays help of commands for the user to choose from."""
		print ('\nCurrently supported commands:\n'
			'help, quit, lcwd, lcd\n'
			"Commands yet to be implimented:\n"
			'ls, mkdir, cd, put, get .. and many more\n')

	def _MakeAlbum(self):
		# cmd 06: mkalbum
		title = raw_input('Album Title: ')
		summary = raw_input('Album Summary: ')

		print "Final - Title: ", title, "Summary: ", summary
		
	def Run(self):
		try:
			while True:
				cmd = self._GetCmd()
				if cmd[0] == 'help':
					self._PrintHelp()
				elif re.match("^mkalbum", cmd[0]):
					self._MakeAlbum(cmd)
				elif cmd[0] == 'quit':
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

	cli = Cli(user)
	print ("Successfully logged in.\n"
		   "Type 'help' for list of available commands.\n")
	cli.Run()

if __name__ == '__main__':
	main()
