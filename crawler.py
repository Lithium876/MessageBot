import csv
import argparse
import os, re, sys
import time as delay
from time import time
from os import system 
from random import randint
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

arr = []
login_Failed = "http://www.pof.com/viewrespond.aspx?loginError=1"

def delayTime():
	#GENERATE DELAY TIME IN SECONDS. RANDOM VALUES RANGES FROM 0 - MAX WAIT FROM OPTIONS.csv FILE
	return randint(0,int(max_wait))

def getDateTime():
	#GENERATE DATE AND TIME
	date_and_time = datetime.fromtimestamp(time()).strftime('%m/%d/%Y %I:%M:%S %p')
	return date_and_time


def Error_Handler(function, error):
	#ALL ERRORS ARE DISPLAY AND LOG
	print("%s %s Function ERROR: %s"%(getDateTime(), function, error))

	#LOGS ERRORS TO DEBUG LOG IF '--LOG' IS INVOKED
	if LOG:
		with open("DEBUG.log","a") as DEBUG_LOG:
			DEBUG_LOG.write("%s %s Function ERROR: %s\n"%(getDateTime(), function, error))
			DEBUG_LOG.close()
	else:
		#LOGS ERRORS TO ERROR LOG '--LOG' IS NOT INVOKED
		with open("ERROR.log","a") as ERROR_LOG:
			ERROR_LOG.write("%s %s Function ERROR: %s\n"%(getDateTime(), function, error))
			ERROR_LOG.close()

def convert_size(B):
	#GET FILE SIZE IN BYTES AND CONVERTS IT TO KILOBYTES AND MEGABYTES
	try:
	   B = float(B)
	   KB = float(1024)
	   MB = float(KB ** 2)

	   if B < KB:
	      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
	   elif KB <= B < MB:
	      return '{0:.2f} KB'.format(B/KB)
	   elif MB <= B:
	      return '{0:.2f} MB'.format(B/MB)
	except Exception as err:
		Error_Handler("Covert Size", err)

def countContacts():
	#COUNTS THE NUMBER CONTACTS IN THE CONTACT_LOG.txt FILE
	try:
		if os.path.exists("CONTACT_LOG.txt"):
			count = len(open('CONTACT_LOG.txt').readlines( ))
			return count
		else:
			return 0
	except Exception as err:
		Error_Handler("Count Contacts",err)

def checkFile(profile_id):
	#CHECKS TO SEE IF THE PROFILE ID SENT ALREADY EXISTS IN THE CONTACT_LOG.txt FILE
	try:
		if profile_id in open('CONTACT_LOG.txt').read():
			return True
	except Exception as err:
		Error_Handler("Check File", err)

def main():
	#GLOBAL VARIABLES
	global username
	global password
	global contacted
	global options 
	global LOG
	global DEBUG
	#================
	
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument('--username', help='specify the username')
		parser.add_argument('--password', help='specify user password')
		parser.add_argument('--options', dest="optionfile",help="loads program option from CSV file")
		parser.add_argument('--LOG', action='store_true', default=False, dest='LOG', help="Logs program activities to file 'DEBUG.log'")
		parser.add_argument('--DEBUG', action='store_true', default=False, dest='DEBUG', help="Produce verbose output suitable for debugging purposes")
		parser.add_argument('--TOTAL_v_CONTACTED_v_NEW', action='store_true', default=False, dest='contacted', help="Return the number of users that meet the search criteria (TOTAL), the number of those users that have already been contacted (CONTACTED), and the number that have not yet been contacted (NEW)")
		args = parser.parse_args()

		if (args.username == None or args.password == None or args.optionfile == None):
			print("Use -h or --help for help")
		else:
			username = args.username
			password = args.password
			options = args.optionfile
			LOG = args.LOG
			DEBUG = args.DEBUG
			contacted = args.contacted
			if LOG and DEBUG and contacted:
				param = "--LOG --DEBUG --TOTAL_v_CONTACTED_v_NEW"
			elif LOG and contacted:
				param = "--LOG --TOTAL_v_CONTACTED_v_NEW"
			elif LOG and DEBUG:
				param = "--LOG --DEBUG"
			elif LOG:
				param = "--LOG"
			else:
				param = ''
			if LOG:
				if os.path.exists("DEBUG.log"):
					with open("DEBUG.log","a") as DEBUG_LOG:
						DEBUG_LOG.write("\n\n")
						DEBUG_LOG.close()
					size=convert_size(os.path.getsize('DEBUG.log'))
					if float(size.split(' ')[0]) >= 10.00 and size.split(' ')[1] == 'MB':
						print("File Size Limit Reached...\nLOG Stopped.")
						LOG = False
				with open("DEBUG.log","a") as DEBUG_LOG:
					DEBUG_LOG.write("%s %s %s %s %s\n"%(getDateTime(), username, password, options, param))
					DEBUG_LOG.close()
			openFile()
	except Exception as e:
		Error_Handler("Main", e)

def openFile():
	#GLOBAL VARIABLES
	global URL
	global num_matches_to_visit
	global message_string
	global max_wait 
	#==================

	try:
		#OPENS THE 'OPTIONS.csv' FILE
		with open(options,'r') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',')
			for row in csvreader:
				arr.append(row)
			csvfile.close()
		#===============================

		#STORES DATA FROM 'OPTIONS.csv' FILE INTO VARIABLES 
		URL = arr[0][1]
		num_matches_to_visit = arr[1][1]
		message_file = arr[2][1]
		max_wait = arr[3][1]
		#================================

		#GETS THE MESSAGE FROM MESSAGE FILE STORES IT IN VARIABLE
		message = open(message_file,"r")
		message_string = message.read()
		message.close()
		#===============================================

		#WRITES DATA TO DEBUG LOG
		if LOG:
			with open("DEBUG.log","a") as DEBUG_LOG:
				DEBUG_LOG.write("%s Search_URL: %s\n"%(getDateTime(), URL))
				DEBUG_LOG.write("%s Number_of_emails_to_send: %s\n"%(getDateTime(), arr[1][1]))
				DEBUG_LOG.write("%s Message_file: %s\n"%(getDateTime(), arr[2][1]))
				DEBUG_LOG.write("%s Max_wait: %s\n"%(getDateTime(), arr[3][1]))
				DEBUG_LOG.write("%s Number_of_contacts_in_contact_log: %d\n"%(getDateTime(),countContacts()))
				DEBUG_LOG.close()
		#==============================

		#WRITES DATA TO CONSOLE
		if DEBUG:
			print("%s Search_URL: %s"%(getDateTime(), URL))
			print("%s Number_of_emails_to_send: %s"%(getDateTime(), arr[1][1]))
			print("%s Message_file: %s"%(getDateTime(), arr[2][1]))
			print("%s Max_wait: %s"%(getDateTime(), arr[3][1]))
			print("%s Number_of_contacts_in_contact_log: %d\n"%(getDateTime(),countContacts()))
		#===============================
		login() #LOGIN FUNCTION CALLED
	except Exception as err:
		Error_Handler("Open File",err)

def login():
	#GLOBAL VARIABLE
	global browser
	global results
	#===============

	try:
		#SETS UP AND OPEN MAIN BROWSER WINDOW
		browser=webdriver.PhantomJS()
		browser.set_window_size(1024, 768)
		new_tab=webdriver.PhantomJS()
		new_tab.set_window_size(1024, 768)
		#====================================
		if DEBUG:
			print("%s [..] Logging In..."%(getDateTime()))	

		#GOES TO WEBSITE AND LOGS IN
		browser.get("http://www.pof.com/")
		browser.find_element_by_id("logincontrol_username").send_keys(username + Keys.TAB)
		delay.sleep(delayTime())
		browser.find_element_by_id("logincontrol_password").send_keys(password + Keys.RETURN)
		delay.sleep(delayTime())
		#==============================

		#CHECKS IF LOGIN WAS SUCCESSFUL
		valid = browser.current_url
		valid = re.sub("&.*","",valid)
		if valid == login_Failed:
			if DEBUG:
				print("%s [-] Error In Logging In, Incorrect Email or Password\n"%(getDateTime()))
			if LOG:
				with open("DEBUG.log","a") as DEBUG_LOG:
					DEBUG_LOG.write("%s ERROR: Incorrect Email or Password\n"%(getDateTime()))
					DEBUG_LOG.close()
			browser.quit()
			return 0
		if DEBUG:
			print("%s [+] Success! Logged In, Bot Starting!"%(getDateTime()))
		delay.sleep(2)
		#====================================
		results = getSearchResults()
		crawler(URL,0,0,0)
	except Exception as err:
		Error_Handler("Login", err)
		
def openNewTab():
	global new_tab
	try:
		new_tab=webdriver.PhantomJS()
		new_tab.set_window_size(1024, 768)
		new_tab.get("http://www.pof.com/")
		new_tab.find_element_by_id("logincontrol_username").send_keys(username + Keys.TAB)
		delay.sleep(delayTime())
		new_tab.find_element_by_id("logincontrol_password").send_keys(password + Keys.RETURN)
	except Exception as err:
		Error_Handler("Open New Tab", err)

def getSearchResults():
	#GOES TO LAST PAGE AND GET THE NUMBER OF SEARCH RESULTS FOUND
	browser.get(URL)
	try:
		try:
			span = browser.find_element_by_xpath("""//*[@id="searchresults"]/center/span""")
			links = span.find_elements_by_tag_name("a")
			for link in links:
			    last_page=link.get_attribute("href")
			browser.get(last_page)
			search_results = browser.find_element_by_xpath("""//*[@id="results"]""")
			search_results = search_results.get_attribute('innerHTML')
			search_results = search_results.split('\n')
			return search_results[3].strip()
		except:
			search_results = browser.find_element_by_xpath("""//*[@id="results"]""")
			search_results = search_results.get_attribute('innerHTML')
			search_results = search_results.split('\n')
			return search_results[3].strip()
	except Exception as err:
		Error_Handler("Get Search Result", err)

def crawler(url_link,page_num,num,printed,):
	printcount=printed
	n=num
	count=0
	logged=0
	page=page_num
	Already_Contacted = 0

	try:
		#OPEN BROWSER TO LINK IN OPTIONS.csv
		browser.get(url_link)
		#GET ALL LINKS OF PROFILE ON CURRENT PAGE
		links = browser.find_elements_by_class_name('link')
		#'--LOG' ENABLE?
		if LOG and printcount == 0:
			with open("DEBUG.log","a") as DEBUG_LOG:
				DEBUG_LOG.write("%s --- START ----\n"%(getDateTime()))
				DEBUG_LOG.write("%s CONTACT_LOG.txt Loaded. Contacts Found: %s\n"%(getDateTime(), countContacts()))
				DEBUG_LOG.write("%s Number of matching search results: %s\n"%(getDateTime(),results))
				DEBUG_LOG.close()
		#'--DEBUG' ENABLE?
		if DEBUG: 
			if printcount == 0:
				print("%s CONTACT_LOG.txt Loaded. Contacts Found: %s"%(getDateTime(), countContacts()))
				print("%s Number of matching search results: %s"%(getDateTime(),results))
				print("%s [+] Page %d Scraping..."%(getDateTime(), page+1))
			if printcount > 0:
				print("%s [+] Page %d Scraping..."%(getDateTime(), page+1))

		for link in links:
			#GO TO EACH PROFILE LINK FOUND
			#STAYS WITH THE BOUND GIVEN IN THE OPTIONS.csv FILE
			if n == int(num_matches_to_visit) or n == int(results):
				if logged == 0:
					if LOG:
						with open("DEBUG.log","a") as DEBUG_LOG:
							DEBUG_LOG.write("%s --- END ----\n"%(getDateTime()))
							DEBUG_LOG.close()
					if DEBUG:
						print("%s [+] Finished Scraping\n"%(getDateTime()))
				if int(num_matches_to_visit) == 0:
					logged +=1
					pass
				else:
					break
			else:
				#GET PROFILE ID
				profile_link = link.get_attribute("href")
				profile_id = re.sub(".*=","",profile_link)
				#CHECKS IF PROFILE ID EXIST IN THE CONTACT_LOG.txt FILE
				exist = checkFile(profile_id)
				if not exist:
					sendMEsg(message_string,profile_link,profile_id,LOG)
					count += 1
					n += 1
					delay.sleep(delayTime())
				else:
					#IF THE PROFILE ID ALREADY EXIST IN CONTACT_LOG.txt >>
					Already_Contacted +=1
					count += 1
					pass

			#CHECKS ALREADY CONTACTED CONTACTS 		
			if int(num_matches_to_visit) == 0:
				profile_link = link.get_attribute("href")
				profile_id = re.sub(".*=","",profile_link)
				exist = checkFile(profile_id)
				if not exist:
					pass
				else:
					Already_Contacted +=1

			#GOES TO NEXT PAGE WHEN ALL 20 PROFILE LINKS ON EACH PAGE HAS BEEN VISITED
			if count == 20:
				browser.find_element_by_xpath("""//*[@id="searchresults"]/center/span/a["""+str(page+1)+"""]""").click()
				delay.sleep(delayTime())
				new_page = browser.current_url
				if DEBUG:
					print("%s [-] No one new to contact.."%(getDateTime()))
				crawler(new_page,page+1,n,1)

		if int(Already_Contacted) == int(results):
			if LOG:
				with open("DEBUG.log","a") as DEBUG_LOG:
					DEBUG_LOG.write("%s --- END ----\n"%(getDateTime()))
					DEBUG_LOG.close()
			if DEBUG:
				print("%s [+] Finished Scraping\n"%(getDateTime()))

		#'--TOTAL_v_CONTACTED_v_NEW' AND '--LOG' ENABLE
		if contacted and LOG and printcount == 0:
			left_to_contact = int(results) - int(Already_Contacted) - int(count)
			if left_to_contact < 0:
				left_to_contact = 0

			with open("DEBUG.log","a") as DEBUG_LOG:
				DEBUG_LOG.write("%s Total number of Contacts: %s\n"%(getDateTime(), results))
				DEBUG_LOG.write("%s Already Contacted: %s\n"%(getDateTime(), Already_Contacted))
				if int(Already_Contacted) == int(results):
					pass
				else:
					DEBUG_LOG.write("%s Just Contacted: %s\n"%(getDateTime(), count))
				DEBUG_LOG.write("%s Left to Contact: %d\n"%(getDateTime(), left_to_contact))
				DEBUG_LOG.close()
			if DEBUG:
				print("%s Total number of Contacts: %s"%(getDateTime(), results))
				print("%s Already Contacted: %s"%(getDateTime(), Already_Contacted))
				if int(Already_Contacted) == int(results):
					pass
				else:
					print("%s Just Contacted: %s"%(getDateTime(), num_matches_to_visit))
				print("%s Left to Contact: %d"%(getDateTime(), left_to_contact))
		elif contacted and printcount == 0:
			left_to_contact = int(results) - int(Already_Contacted) - int(num_matches_to_visit)
			print("%s Total number of Contacts: %s"%(getDateTime(), results))
			print("%s Already Contacted: %s"%(getDateTime(), Already_Contacted))
			if int(Already_Contacted) == int(num_matches_to_visit):
				pass
			else:
				print("%s Just Contacted: %s"%(getDateTime(), num_matches_to_visit))
			print("%s Left to Contact: %d"%(getDateTime(), left_to_contact))
	except Exception as err:
		Error_Handler("Crawler", err)

def sendMEsg(message_string,profile_link,profile_id,log):
	#OPENS PROFILE IN NEW TAB
	openNewTab()
	delay.sleep(delayTime())
	new_tab.get(profile_link)
	#GETS USERNAME/ACCOUNT NAME
	user = new_tab.find_element_by_id("username")
	username = user.text
	try:
		#SENDS MESSAGE 
		new_tab.find_element_by_xpath("""//*[@id="send-message-textarea"]""").send_keys(message_string)
		delay.sleep(delayTime())
		new_tab.find_element_by_xpath("""//*[@id="send-quick-message-submit"]""").click()
		new_tab.save_screenshot('ScreenShot.png')
		delay.sleep(2)
		new_tab.quit()
		if log:
			with open("DEBUG.log","a") as DEBUG_LOG:
				DEBUG_LOG.write("%s Sent msg to: %s\n"%(getDateTime(), username))
				#CHECK THE SIZE OF THE DEBUG.log FILE TO ENSURE THAT IT DOESN'T GO OVER 10MB
				size=convert_size(os.path.getsize('DEBUG.log'))
				if float(size.split(' ')[0]) >= 10.00 and size.split(' ')[1] == 'MB':
					DEBUG_LOG.write("%s File Size Limit Reached...\nSparse Stopped.\n"%(getDateTime(), user.text))
					print("File Size Limit Reached...\nSparse Stopped.")
					DEBUG_LOG.close()
					log = False
				else:
					DEBUG_LOG.close()
		if DEBUG:
			print("%s [+] Sent msg to: %s"%(getDateTime(), username))
		with open("CONTACT_LOG.txt","a") as contact_log:
			contact_log.write("Profile_ID: %s \tAccount Name: %s\n"%(profile_id, username))
			contact_log.close()			
	except Exception as msgerr:
		Error_Handler("Sending Message", msgerr)

if __name__ == '__main__':
	main()
