import optparse
import csv
import time, os, re
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

arr = []
login_Failed = "http://www.pof.com/viewrespond.aspx?loginError=1"
browser=webdriver.PhantomJS()
browser.set_window_size(1024, 768)
new_tab=webdriver.PhantomJS()
new_tab.set_window_size(1024, 768)

def checkFile(profile_id):
	if profile_id in open('CONTACT_LOG.txt').read():
		return True

def crawler(url_link,page_num,num):
	n=num
	count=0
	page=page_num
	contact_log = open("CONTACT_LOG.txt","a")
	browser.get(url_link)
	links = browser.find_elements_by_class_name('link')
	os.system('cls')
	print("[+] Page: %d"%(page+1))
	print("[+] Scraping...")
	for link in links:
		if n == int(num_matches_to_visit):
			break
		else:
			profile_link = link.get_attribute("href")
			profile_id = re.sub(".*=","",profile_link)
			exist = checkFile(profile_id)
			if not exist:
				new_tab.get(profile_link)
				user = new_tab.find_element_by_id("username")
				print("Profile_ID: %s \tAccount Name: %s\n"%(profile_id,user.text))
				contact_log.write("Profile_ID: %s \tAccount Name: %s\n"%(profile_id,user.text))
				count += 1
				n += 1
			else:
				count += 1
				pass
		if count == 20:
			browser.find_element_by_xpath("""//*[@id="searchresults"]/center/span/a["""+str(page+1)+"""]""").click()
			new_page = browser.current_url
			crawler(new_page,page+1,n) 
				
def login():
	try:
		os.system('cls')
		print("[+] Logging In...")	
		browser.get("http://www.pof.com/")
		browser.find_element_by_id("logincontrol_username").send_keys(username + Keys.TAB)
		time.sleep(1)
		browser.find_element_by_id("logincontrol_password").send_keys(password + Keys.RETURN)
		browser.save_screenshot('screenie.png')
		time.sleep(1)
		valid = browser.current_url
		valid = re.sub("&.*","",valid)
		if valid == login_Failed:
			print("[-] Error In Logging In, Incorrect Email or Password\n")
			browser.close()
			exit(0)
		else:
			print("\n[+] Success! Logged In, Bot Starting!")
			time.sleep(2)
			browser.save_screenshot('screenie2.png')
			crawler(URL,0,0)
	except Exception as err:
		print(err)

def openFile(options):
	global URL
	global num_matches_to_visit
	global message_file
	global max_wait 
	try:
		with open(options,'r') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',')
			for row in csvreader:
				arr.append(row)
		URL = arr[0][1]
		num_matches_to_visit = arr[1][1]
		message_file = arr[2][1]
		max_wait = arr[3][1]
		login()
	except Exception as err:
		print(err)

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
		username = options.username
		password = options.password
		options = options.options
		openFile(options)

if __name__ == '__main__':
	main()