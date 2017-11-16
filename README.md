# Message Bot

Functional description:
Each time the program is run, it shall perform the following tasks

1) Log in to the website using the username and password specified at the command line

2) Perform a member-search using the match-search URL specified in the OPTIONS_FILE.csv

3) Load the first profile returned by the search that has not been emailed previously

4) Send a message to the loaded profile (Message_file)

5) Add the account name and profile ID# of the loaded profile to CONTACT_LOG.txt

6) Close the open profile 

7) Repeat steps 3-6 XX times (XX = Number_of_matches_to_email)

 8) Gracefully exit

Specifications:
* It shall run from the DOS command line on Windows XP and Windows 10
* It shall run as a background task; without opening any new browser windows that are visible to or interact with the user
* Windows Task Scheduler shall be capable of running this program whether user is logged in or not
* It shall be possible to run the tool many times and unattended without user interaction
* It shall log activity in a first-in/First-out log file (e.g, DEBUG.log), with a maximum file-size of 10MB 
* It shall accept a command line parameter (e.g., -DEBUG) which will cause it to produce detailed verbose output suitable for debugging purposes. 
* It shall accept a command line parameter (e.g., -SPARSE) which will cause it to produce sparse output suitable for sparse logging of activity (e.g., only Logins, emails sent, system error messages)
* It shall accept a command line parameter (e.g., -TOTAL_v_CONTACTED_v_NEW) which will cause it to perform a search and return the number of users that meet the search criteria (TOTAL), the number of those users that have already been contacted (CONTACTED), and the number that have not yet been contacted (NEW)
* The program shall delay a random number of seconds (between 0-to-Max_wait seconds) before each page load/URL query
