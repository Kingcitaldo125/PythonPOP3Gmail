import poplib
import re
import os
import time
from datetime import date

path = ""
with open("dumpPath.txt", "r") as f:
	path = f.read()

print("Using email path:", path)
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
		
	def getMessageTextFromMIME(self, mText):
		messageParams=[]

		# Date is like: Date: Sun, 2 Dec 2018 19:30:06 +0000 (UTC)
		dateM = re.search(r"\b([dD]ate:\s+.+\d{2}:\d{2}:\d{2})\s+.+\b", mText, re.I|re.M)
		fromM = re.search(r"\b([fF]rom:\s+.+)\b", mText, re.I|re.M)
		toM = re.search(r"\b([tT][oO]:\s+.+[@].+[.][cC][oO][mM])", mText, re.I|re.M)
		subM = re.search(r"\b([sS]ubject:\s+.+)\b", mText, re.I|re.M)
		
		if dateM:
			messageParams.append(dateM.group(1))
		if fromM:
			messageParams.append("From: "+fromM.group(1))
		if toM:
			messageParams.append(toM.group(1))
		if subM:
			messageParams.append(subM.group(1))

		return messageParams
		
	def retrieveEmails(self):
		allMessageParams = []
		for i in range(self.numMessages):
			fileBuffer = ""
			filename = self.path+"Message"+str(i+1)+".txt"
			print("Opening '{0}'".format(filename))
			with open(filename, 'w') as f:
				try:
					for j in self.Mobj.retr(i+1)[1]:
						decoded = str(j.decode("utf-8"))
						
						fileBuffer+=decoded
						fileBuffer+=" \n"
						
						f.write(decoded)
						f.write('\n')
				except:
					f.write('\n')
					continue
			
			#print("FileBuffer:",fileBuffer)
			mParams = self.getMessageTextFromMIME(fileBuffer)
			allMessageParams.append(mParams)
			
		#print("Retrieving Complete!\n")
		return allMessageParams

	def quit(self):
		self.Mobj.quit()
		print("Goodbye!")
		time.sleep(2)


class EmailMenu(object):
	def __init__(self, emFetch):
		self.emailFetcher = emFetch
			
	def run(self,timeout=0):
		while 1:
			for ii in self.emailFetcher.retrieveEmails():
				for jj in ii:
					print(jj)
				print("----------------\n")
			time.sleep(timeout)
			
		self.emailFetcher.quit()

emenu = EmailMenu(EmailFetcher())
emenu.run(5)
