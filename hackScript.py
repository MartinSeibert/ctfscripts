import sys, urllib, re, urlparse, base64
from bs4 import BeautifulSoup

# -*- coding: utf-8 -*-


'''
Searches text for flag{ or key{, or any specified keywords and prints the substring
It attempts to print everything from the found keyword to an endbracket '}'.
If no '}' is present, it prints the remainder of the text.

If no matches are found, it decodes the text in base64 and checks again.
If no matches are found  again, it decodes the text in base32 and checks again.
NOTE: the base encodings seem to pop up a lot in hacking challenges.
'''
def checkKeywords(text):
	keywords = ['flag', 'key']
	foundSomething = False
	for keyword in keywords:
		if keyword in text:
			foundSomething = True
			print "Found '" + keyword + "'"
			start = text.find(keyword)
			end = text.find('}')
			if end == -1 or end < start:
			
				print text[start:]
			else:
				print "end not -1 or less than"
				print text[start:end]
	if foundSomething == False:
		print "No matches found, trying base64 decoding"
		try:
			b64Text = base64.b64decode(text)
			for keyword in keywords:
				if keyword in b64Text:
					foundSomething = True
					print "Found '" + keyword + "'"
					start = b64Text.find(keyword)
					end = b64Text.find('}')
					if end == -1:
						print b64Text[start:]
					else:
						print b64Text[start:end + 1]
		except:
			print "Base64 doesn't work, it's doubtful that the text was base64 encrypted."
	if foundSomething == False:
		print "No matches found, trying base32 decoding"
		try:
			b32Text = base64.b32decode(text)
			for keyword in keywords:
				if keyword in b32Text:
					foundSomething = True
					print "Found '" + keyword + "'"
					start = b32Text.find(keyword)
					end = b32Text.find('}')
					if end == -1:
						print b32Text[start:]
					else:
						print b32Text[start:end + 1]
		except:
			print "Base32 doesn't work, it's doubtful that the text was base32 encrypted."
	return

def checkWebpageForKeywords(url):
	
	# create beautifulSoup object for parsing the page
	f = urllib.urlopen(url)
	soup = BeautifulSoup(f, "html.parser")
	
	#check for keywords in the text of the page
	text = soup.get_text().encode('utf-8')
	#checkKeywords(text)
	
	
	
	for i in soup.findAll('img', attrs={'src': re.compile('(?i)(jpg|png)$')}):
		full_url = urlparse.urljoin(url, i['src'])
		print "image URL: ", full_url
    
	for i in soup.findAll('script', attrs={'src': re.compile('(?i)(js)$')}):
		full_url = urlparse.urljoin(url, i['src'])
		print "script URL: ", full_url
		
	for link in soup.find_all('a'):
		print "link: ", (link.get('href'))
	return

#checkWebpageForKeywords('http://www.reddit.com')


'''
A class that takes in a url and exposes details about that webpage
'''
class Webpage:
	def __init__(self, url):
		self.url = url
		f = urllib.urlopen(url)
		self.soup = BeautifulSoup(f, "html.parser")
	def checkText(self):
		#check for keywords in the text of the page
		text = self.soup.get_text().encode('utf-8')
		checkKeywords(text)

	def listImages(self):
		# list all of the images referenced on the URL
		for i in self.soup.findAll('img', attrs={'src': re.compile('(?i)(jpg|png)$')}):
			full_url = urlparse.urljoin(self.url, i['src'])
			print "image URL: ", full_url

	def listScripts(self):
		# list all of the scripts referenced by the URL
		for i in self.soup.findAll('script', attrs={'src': re.compile('(?i)(js)$')}):
			full_url = urlparse.urljoin(self.url, i['src'])
			print "script URL: ", full_url

	def listLinks(self):
		# list all of the links from the URL
		for link in self.soup.find_all('a'):
			print "link: ", (link.get('href'))






# TESTS
def checkKeywords_test():
	print "Testing checkKeywords()"
	print "Case 1: asfdasfnnfnasdfon:"
	checkKeywords('asfdasfnnfnasdfon')
	print "\n\n"
	print "Case 2: asdfnainfflag{br0Ham}"
	checkKeywords("asdfnainfflag{br0Ham}")
	print "\n\n"
	print "Case 3: plaintext == fgughasnasdfflag{dudebro} "
	print "test runs base64encoded == " + base64.b64encode('fgughasnasdfflag{dudebro}')
	checkKeywords(base64.b64encode('fgughasnasdfflag{dudebro}'))
	print "\n\n"
	print "Case 4: plaintext == asdfkeydudebroasfnas;idnf"
	checkKeywords('asdfkeydudebroasfnas;idnf')
	print "-------------------------------------------------------------"
	return

def webpage_test(url):
	webpage = Webpage(url)
	webpage.checkText()
	webpage.listImages()
	webpage.listScripts()
	webpage.listLinks()


	
def testAll():
	checkKeywords_test()
	webpage_test('http://www.reddit.com')
	return
	
#testAll()
