import poplib
import re
import os
import time
from datetime import date

path = "C:\\Users\\paula\\Desktop\\emailDump\\"
passwordFilename = "emailPassword.txt"

# Uses Gmail
class EmailFetcher(object):
	def __init__(self):
		global path,passwordFilename
		self.path = path
		
		self.user = "paularelt@gmail.com"
		self.password = ""
		with open(passwordFilename, "r") as f:
			self.password = f.read()
		
		self.Mobj = poplib.POP3_SSL('pop.googlemail.com','995')
		self.Mobj.user(self.user)
		self.Mobj.pass_(self.password)
		
		self.numMessages = len(self.Mobj.list()[1])

	def convertToMessageObject(self, text, file):
		d=0
		
	def retrieveEmails(self,date):
		for i in range(self.numMessages):
			filename = self.path+"Message"+str(i+1)+".txt"
			print("Opening '{0}'".format(filename))
			with open(filename, 'w') as f:
				try:
					for j in self.Mobj.retr(i+1)[1]:
						decoded = str(j.decode("utf-8"))
						f.write(decoded)
						f.write('\n')
				except:
					f.write('\n')
					continue
		print("Retrieving Complete!\n")

	def clearEmailDirectory(self):
		for p,d,files in os.walk(self.path):
			for f in files:
				os.remove(self.path+str(f))
		print("Clearing Complete!\n")
			
	def deleteEmail(self,emailNumber):
		for p,d,files in os.walk(self.path):
			for f in files:
				M = re.match(r"[mM]essage(\d+)[.][tT][xX][tT]", f, re.M|re.I)
				if M:
					if M.group(1) == emailNumber:
						print("Deleting file",M.group(1))
						os.remove(self.path+M.group(0))
						print("Deleted")
						return 0
		return -1

	def quit(self):
		self.Mobj.quit()
		print("Goodbye!")
		time.sleep(2)


# Date Format:
# Fri, 28 Sep 2012 21:47:37 -0700 (PDT)
class EmailMenu(object):
	def __init__(self, emFetch):
		self.exitCode = 6
		self.emailFetcher = emFetch
		self.path = self.emailFetcher.path #inherit path from writer/reader
		self.todaysDate = date.today()
		
		self.day = str(self.todaysDate.strftime("%d"))
		self.month = str(self.todaysDate.strftime("%m"))
		self.year = str(self.todaysDate.strftime("%Y"))
		
		print("{0} - Starting EmailMenu".format(str(self.todaysDate)))
		
	def run(self):
		inputSelection = -1
		while 1:
			self.displayChoices()
			try:
				inputSelection = int(input())
			except:
				break
			if inputSelection == self.exitCode:
				break
			elif inputSelection == 1:
				self.emailFetcher.retrieveEmails(self.year)
			elif inputSelection == 2:
				self.displayEmails()
			elif inputSelection == 3:
				self.emailFetcher.clearEmailDirectory()
			elif inputSelection == 4:
				self.chooseDeleteDisplay()
				numb = str(input())
				print("Deleting {0}".format(numb))
				if self.emailFetcher.deleteEmail(numb) != 0:
					print("Could not find email to be deleted")
					continue
			elif inputSelection == 5:
				os.system("cls")
			else:
				print("Invalid Selection.")
				continue
		self.emailFetcher.quit()

	def displayChoices(self):
		print("-----------------------------------")
		print("-----------------------------------")
		print("Choose An Option Below:")
		print("1. Retrieve Emails")
		print("2. Display Emails in email folder")
		print("3. Clear Emails(this will delete all emails in the email folder!!!)")
		print("4. Delete Email(choose email number)")
		print("5. Clear Terminal")
		print("6. Exit")
		print("-----------------------------------")
		print("-----------------------------------\n")
		
	def displayEmails(self):
		print("-----------------------------------")
		print("-----------------------------------")
		for p,d,files in os.walk(self.path):
			for f in files:
				print(str(f))
		print("-----------------------------------")
		print("-----------------------------------\n")
		
	def chooseDeleteDisplay(self):
		print("-----------------------------------")
		print("-----------------------------------")
		print("Enter the Number of the email you want to delete:")
		print("-----------------------------------")
		print("-----------------------------------\n")


emenu = EmailMenu(EmailFetcher())
emenu.run()
