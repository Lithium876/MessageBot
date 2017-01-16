import optparse
import csv
import time, os, re
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

login_Failed = "http://www.pof.com/viewrespond.aspx?loginError=1&usr=RkFGQkNDQzYxQTA0Qzk5RDc5MUM2NjM2MzJFNEU4MUMzNUM0OTI4RkM5NjlDM0U4OEFCMEZFOTlCNzZEOEUxOTc1QkQ2OERBMThBM0RCREUxNEJBQzEwOENBRjc3QUYyQkE2NDhDOTZGQTkwMEIzNERGRDgzREUwOTQ4NUYwOUQzNTVCNTVCNDQyNDcwRTI2MTM0QkJERjg1RjU1MzU2MUY1NEFBMzQ5NTMwNDMzMDI0RDU2M0Y4MUNBRTU1MDFENkFEMDRFOEFFQkJCREQ0RTdGMzQ4OTAxODA2QzQyM0Y1MDBENDU3OTg3Mzk4QjVCQzVDMDUxMDI0MTY4REVBNkE4MDNDNjUzM0Y2QzQyNUYyM0YyM0JBNUE1REU4NzlC0"
arr = []
browser=webdriver.PhantomJS()
browser.set_window_size(1024, 768)

def crawler():
	try:
		n=0
		contact_log = open("CONTACT_LOG.txt","a")
		browser.get("http://www.pof.com/")
		os.system('cls')
		print("[+] Logging In...")	
		browser.find_element_by_id("logincontrol_username").send_keys(username + Keys.TAB)
		time.sleep(1)
		browser.find_element_by_id("logincontrol_password").send_keys(password + Keys.RETURN)
		browser.save_screenshot('screenie.png')
		time.sleep(1)
		browser.get(URL)
		if browser.current_url == login_Failed:
			print("[-] Error In Login, Incorrect Email or Password\n")
			browser.close()
			exit(0)
		else:
			print("\n[+] Success! Logged In, Bot Starting!")
			time.sleep(2)
			os.system('cls')
			browser.save_screenshot('screenie2.png')
			links = browser.find_elements_by_class_name('link')
			for link in links:
				if n == int(num_matches_to_visit):
					break
				else:
					string = link.get_attribute("href")
					string = re.sub(".*=","",string)
					print(string)
					n += 1
			    

	except Exception as err:
		print(err)

def openFile(options):
	global URL
	global num_matches_to_visit
	global message_file
	global max_wait 
	with open(options,'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			arr.append(row)
	URL = arr[0][1]
	num_matches_to_visit = arr[1][1]
	message_file = arr[2][1]
	max_wait = arr[3][1]
	#print("\nURL: %s\n\nNumber of Matches to Vist: %s\nMassage File: %s\nMax Wait: %s"%(URL,num_matches_to_visit,message_file,max_wait))
	crawler()

def main():
	global username
	global password
	parser = optparse.OptionParser('--username <USERNAME> --password <PASSWORD> --options <OPTIONFILENAME.CSV>', version="%prog 1.0")
	parser.add_option('--username',dest='username', type='string', help='specify the username')
	parser.add_option('--password', dest='password', type='string', help='specify user password')
	parser.add_option('--options', dest='options', type='string', help="loads program option from CSV file")
	(options, args) = parser.parse_args()
	if (options.username == None or options.password == None or options.options == None):
		print(parser.usage)
		exit(0)
	else:
		print("[+] Warming Up...")
		username = options.username
		password = options.password
		options = options.options
		#print("\nUsername: %s \nPassword: %s \nOption: %s"%(username, password, options))
		openFile(options)

if __name__ == '__main__':
	main()