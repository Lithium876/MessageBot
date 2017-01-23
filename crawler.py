import argparse
import csv
import os, re, sys
import time as delay
from datetime import datetime
from time import time 
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

arr = []
login_Failed = "http://www.pof.com/viewrespond.aspx?loginError=1"

def getDateTime():
	date_and_time = datetime.fromtimestamp(time()).strftime('%m/%d/%Y %I:%M:%S %p')
	return date_and_time

def convert_size(B):
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2)

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B:
      return '{0:.2f} MB'.format(B/MB)

def countContacts():
	try:
		count = len(open('CONTACT_LOG.txt').readlines(  ))
		return count
	except Exception as error:
		print(error)

def checkFile(profile_id):
	if profile_id in open('CONTACT_LOG.txt').read():
		return True

def crawler(url_link,page_num,num,log,debug,count):
	printcount = count
	n=num
	count=0
	page=page_num
	try:
		if log:
			DEBUG_LOG = open("DEBUG.log","a")
		contact_log = open("CONTACT_LOG.txt","a")
		message = open(message_file,"r")
		message_string = message.read()
		browser.get(url_link)
		links = browser.find_elements_by_class_name('link')
		search_results = browser.find_element_by_xpath("""//*[@id="results"]""")
		search_results = search_results.get_attribute('innerHTML')
		search_results = search_results.split(' ')
		if log and printcount == 0:
			DEBUG_LOG.write("%s --- START ----\n"%(getDateTime()))
			DEBUG_LOG.write("%s CONTACT_LOG.txt Loaded. Contacts Found: %d\n"%(getDateTime(), countContacts()))
			DEBUG_LOG.write("%s Number of matching search results: %s\n"%(getDateTime(),search_results[2]))
		if debug: 
			if printcount == 0:
				print("%s CONTACT_LOG.txt Loaded. Contacts Found: %d"%(getDateTime(), countContacts()))
				print("%s Number of matching search results: %s"%(getDateTime(),search_results[2]))
				print("%s [+] Page %d Scraping..."%(getDateTime(), page+1))
			if printcount > 0:
				print("%s [+] Page %d Scraping..."%(getDateTime(), page+1))
		if contacted and log and printcount == 0:
			try:
				Total_Contacts =  search_results[2].split('+')
				plus='+'
			except:
				Total_Contacts =  search_results[2]
				plus=''
			Contact = countContacts()
			left_to_contact = int(Total_Contacts[0]) - int(Contact)
			DEBUG_LOG.write("%s Total number of Contacts: %s\n"%(getDateTime(), search_results[2]))
			DEBUG_LOG.write("%s Already Contacted: %s\n"%(getDateTime(), countContacts()))
			DEBUG_LOG.write("%s Left to Contact: %d%s\n"%(getDateTime(), left_to_contact,plus))
		elif contacted and printcount == 0:
			try:
				Total_Contacts =  search_results[2].split('+')
				plus='+'
			except:
				Total_Contacts =  search_results[2]
				plus=''
			Contact = countContacts()
			left_to_contact = int(Total_Contacts[0]) - int(Contact)
			print("%s Total number of Contacts: %s"%(getDateTime(), search_results[2]))
			print("%s Already Contacted: %s"%(getDateTime(), countContacts()))
			print("%s Left to Contact: %d%s"%(getDateTime(), left_to_contact,plus))
		
		for link in links:
			if n == int(num_matches_to_visit):
				if log:
					DEBUG_LOG.write("%s --- END ----\n"%(getDateTime()))
					DEBUG_LOG.close()
				if debug:
					print("%s [+] Finished Scraping\n"%(getDateTime()))
				break
			else:
				profile_link = link.get_attribute("href")
				profile_id = re.sub(".*=","",profile_link)
				exist = checkFile(profile_id)
				if not exist:
					new_tab.get(profile_link)
					user = new_tab.find_element_by_id("username")
					if log:
						DEBUG_LOG.write("%s Sent msg to: %s\n"%(getDateTime(), user.text))
						size=convert_size(os.path.getsize('DEBUG.log'))
						if float(size.split(' ')[0]) >= 10.00 and size.split(' ')[1] == 'MB':
							DEBUG_LOG.write("%s File Size Limit Reached...\nSparse Stopped.\n"%(getDateTime(), user.text))
							print("File Size Limit Reached...\nSparse Stopped.")
							DEBUG_LOG.close()
							log = False
					if debug:
						print("%s [+] Sent msg to: %s"%(getDateTime(), user.text))
					#new_tab.find_element_by_class_name("profile").send_keys(message_string)
					#new_tab.save_screenshot('message.png')
					contact_log.write("Profile_ID: %s \tAccount Name: %s\n"%(profile_id,user.text))
					count += 1
					n += 1
				else:
					count += 1
					pass
			if count == 20:
				browser.find_element_by_xpath("""//*[@id="searchresults"]/center/span/a["""+str(page+1)+"""]""").click()
				new_page = browser.current_url
				if log:
					DEBUG_LOG.close()
				contact_log.close()
				if debug:
					print("%s [-] No one new to contact.."%(get_attribute()))
				crawler(new_page,page+1,n,log,debug,1)
	except Exception as er:
		if log:
			DEBUG_LOG.open("DEBUG.log","a")
			DEBUG_LOG.write("%s ERROR: %s"%(getDateTime(), er))
			DEBUG_LOG.close()
		print(er)
	new_tab.quit() 
	browser.quit()
				
def login(log, debug):
	global browser
	global new_tab
	if log:
		DEBUG_LOG = open("DEBUG.log","a")
	try:
		browser=webdriver.PhantomJS()
		browser.set_window_size(1024, 768)
		new_tab=webdriver.PhantomJS()
		new_tab.set_window_size(1024, 768)
		if debug:
			print("%s [..] Logging In..."%(getDateTime()))	
		browser.get("http://www.pof.com/")
		browser.find_element_by_id("logincontrol_username").send_keys(username + Keys.TAB)
		delay.sleep(1)
		browser.find_element_by_id("logincontrol_password").send_keys(password + Keys.RETURN)
		delay.sleep(1)
		valid = browser.current_url
		valid = re.sub("&.*","",valid)
		if valid == login_Failed:
			if debug:
				print("%s [-] Error In Logging In, Incorrect Email or Password\n"%(getDateTime()))
			if log:
				DEBUG_LOG.write("%s ERROR: Incorrect Email or Password\n"%(getDateTime()))
				DEBUG_LOG.close()
			browser.close()
			exit(0)
		else:
			if debug:
				print("%s [+] Success! Logged In, Bot Starting!"%(getDateTime()))
			delay.sleep(2)
			crawler(URL,0,0,log,debug,0)
	except Exception as err:
		print("%s %s"%(getDateTime(), err))
		if log:
			DEBUG_LOG.write("%s ERROR: %s"%(getDateTime(), err))
			DEBUG_LOG.close()

def openFile(options,log,debug):
	global URL
	global num_matches_to_visit
	global message_file
	global max_wait 
	if log:
		DEBUG_LOG = open("DEBUG.log","a")
	try:
		with open(options,'r') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',')
			for row in csvreader:
				arr.append(row)
		URL = arr[0][1]
		num_matches_to_visit = arr[1][1]
		message_file = arr[2][1]
		max_wait = arr[3][1]
		if log:
			DEBUG_LOG.write("%s Search_URL: %s\n"%(getDateTime(), URL))
			DEBUG_LOG.write("%s Number_of_emails_to_send: %s\n"%(getDateTime(), arr[1][1]))
			DEBUG_LOG.write("%s Message_file: %s\n"%(getDateTime(), arr[2][1]))
			DEBUG_LOG.write("%s Max_wait: %s\n"%(getDateTime(), arr[3][1]))
			DEBUG_LOG.close()
		if debug:
			print("%s Search_URL: %s"%(getDateTime(), URL))
			print("%s Number_of_emails_to_send: %s"%(getDateTime(), arr[1][1]))
			print("%s Message_file: %s"%(getDateTime(), arr[2][1]))
			print("%s Max_wait: %s"%(getDateTime(), arr[3][1]))
		login(log,debug)
	except Exception as err:
		print(err)
		if log:
			DEBUG_LOG.write("%s ERROR: %s\n"%(getDateTime(), err))
			DEBUG_LOG.close()

def main():
	global username
	global password
	global contacted
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument('--username', help='specify the username')
		parser.add_argument('--password', help='specify user password')
		parser.add_argument('--options', dest="optionfile",help="loads program option from CSV file")
		parser.add_argument('--SPARSE', action='store_true', default=False, dest='SPARSE', help="Logs program activities to file 'DEBUG.log'")
		parser.add_argument('--DEBUG', action='store_true', default=False, dest='DEBUG', help="Produce verbose output suitable for debugging purposes")
		parser.add_argument('--TOTAL_v_CONTACTED_v_NEW', action='store_true', default=False, dest='contacted', help="Return the number of users that meet the search criteria (TOTAL), the number of those users that have already been contacted (CONTACTED), and the number that have not yet been contacted (NEW)")
		args = parser.parse_args()

		if (args.username == None or args.password == None or args.optionfile == None):
			print("Use -h or --help for help")
		else:
			username = args.username
			password = args.password
			options = args.optionfile
			SPARSE = args.SPARSE
			DEBUG = args.DEBUG
			contacted = args.contacted
			if SPARSE and DEBUG:
				param = "--SPARSE --DEBUG"
			elif SPARSE and contacted:
				param = "--SPARSE --TOTAL_v_CONTACTED_v_NEW"
			elif SPARSE:
				param = "--SPARSE"
			else:
				param = ''
			if SPARSE:
				DEBUG_LOG = open("DEBUG.log","a")
				size=convert_size(os.path.getsize('DEBUG.log'))
				if float(size.split(' ')[0]) >= 10.00 and size.split(' ')[1] == 'MB':
					print("File Size Limit Reached...\nSparse Stopped.")
					DEBUG_LOG.close()
					SPARSE = False
				else:
					DEBUG_LOG.write("%s %s %s %s %s\n"%(getDateTime(), username, password, options, param))
					DEBUG_LOG.close()
			openFile(options,SPARSE,DEBUG)
	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()
