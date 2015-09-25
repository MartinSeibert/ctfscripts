import base64

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
			if end == -1:
				print text[start:]
			else:
				print text[start:end + 1]
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
#checkKeywords('asdfflag{broha}m')

def checkKeywords_test():
	print "Case 1: asfdasfnnfnasdfon:"
	checkKeywords('asfdasfnnfnasdfon')
	print "\n\n"
	print "Case 2: asdfnainfflag{br0Ham}"
	checkKeywords("asdfnainfflag{br0Ham}")
	print "\n\n"
	print "Case 3: plaintext == fgughasnasdfflag{dudebro} "
	print "test runs base64encoded == " + base64.b64encode('fgughasnasdfflag{dudebro}')
	checkKeywords(base64.b64encode('fgughasnasdfflag{dudebro}'))
	
	return
	
	
	
checkKeywords_test()
