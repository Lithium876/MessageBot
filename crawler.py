import optparse

def main():
	parser = optparse.OptionParser('--username <USERNAME> --password <PASSWORD> --options <OPTIONFILENAME.CSV>', version="%prog 1.0")
	parser.add_option('--username',dest='username', type='string', help='specify the username')
	parser.add_option('--password', dest='password', type='string', help='specify user password')
	parser.add_option('--options', dest='options', type='string', help="loads program option from CSV file")
	(options, args) = parser.parse_args()
	if (options.username == None or options.password == None or options.options == None):
		print(parser.usage)
		exit(0)
	else:
		username = options.username
		password = options.password
		options = options.options
		print("\nUsername: %s \nPassword: %s \nOption: %s"%(username, password, options))

if __name__ == '__main__':
	main()