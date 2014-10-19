##############################################################################################################
#                       #   Parachat logging software AKA: "R3D3Y3"                                          #
#  \                 /  #   Version 2.0                                                                      #
#   \      ( )      /   #   June 13, 2014                                                                    #
#    \             /    #   Author: William J. Appleton (Mephistopheles)                                     #
#     \           /     ######################################################################################
#  --------------/----  #            *           Copyright 2014, William J. Appleton           *             #
#       \       /    |  #   This program is distributed under the terms of the GNU General Public License.   #
#        \     /     |  #                                                                                    #
#         \   /      |  #   This program is free software: you can redistribute it and/or modify             #
#          \ /       |  #   it under the terms of the GNU General Public License as published by             #
#           V        |  #   the Free Software Foundation.                                                    #
#                    |  #                                                                                    #
#                    |  #   This program is distributed in the hope that it will be useful,                  #
#  -------------------  #   but WITHOUT ANY WARRANTY; without even the implied warranty of                   #
#                       #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                    #
#  Copyright (C) 2011   #   GNU General Public License for more details.                                     #
#  William J. Appleton  #                                                                                    #
#                       #   You should have received a copy of the GNU General Public License                #
#                       #   along with this program.  If not, see <http://www.gnu.org/licenses/>.            #
##############################################################################################################
import httplib ,urllib, time, re, datetime, json, random, bleach, unicodedata, codecs
from random import randint
from HTMLParser import HTMLParser
def REPORTER(FileName, Message):
	try:
		Reporter = open(FileName, "a")
		Reporter.write(unicode(datetime.datetime.now().date()) + u'~' + unicode(datetime.datetime.now().time()) + u'>>' + unicode(Message) + u'\n')
		Reporter.close()
	except Exception:
		Reporter = open(FileName, "w+")
		Reporter.close()
		Reporter = open(FileName, "a")
		Reporter.write(unicode(datetime.datetime.now().date()) + u'~' + unicode(datetime.datetime.now().time()) + u'>>' + unicode(Message) + u'\n')
		Reporter.close()
def USERNAME_GENERATOR(UserName_Length, UserName_ValidChars):
	return ''.join(random.choice(UserName_ValidChars) for _ in range(UserName_Length))
def LOGIN():
	LoginFailed = 1
	while LoginFailed:
		try:
			UserName_Length = randint(6,9)
			UserName_ValidChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
			UserName = str(USERNAME_GENERATOR(UserName_Length, UserName_ValidChars))
			Login_URL = "http://members.parachat.com:8080/basic/wap/auth.jsp?site=iPhone&room=Lobby-2&user=" + UserName + "&Col.MainBg=EEEEEE&Col.MainFg=000000&downloadpath=http://chat.parachat.com/applet&pass="
			Login_Site_Reply = urllib.urlopen(Login_URL)
			Login_Raw_Reply = Login_Site_Reply.read()
			Chat_Key = str(re.search("key=(.*)&room=Lobby-2&user=" + UserName, re.search("<a href=\"(.*)\">Go to mobile chat room</a>",Login_Raw_Reply).group(1)).group(1))
			REPORTER("R3D3Y3.log", "Initiated new session with username \"" + UserName + "\" and session key \"" + Chat_Key + "\"")
			LoginFailed = 0
			return str("http://members.parachat.com:8080/basic/wap/reqpub.jsp?site=iPhone&key=" + Chat_Key + "&room=iPhone&user=" + UserName)
		except Exception:
			REPORTER("R3D3Y3.log", "Failed to initiate a new session.")
			time.sleep(120)
def MAIN():
	NoHTMLEscape = HTMLParser()
	MessageURL = str(LOGIN())
	MessageSuccess = 0
	ProperMessage = re.compile(ur'(.*):(.*)', re.UNICODE)
	PrivateMessage = re.compile(ur'^\[Private\]?', re.UNICODE)
	while 1:
		try:
			Site_Reply = urllib.urlopen(MessageURL)
			Messages = json.loads(Site_Reply.read())
			if Messages['success']:
				if MessageSuccess < 3:
					REPORTER("R3D3Y3.log", "Successfully gathered new messages.")
					MessageSuccess += 1
				elif MessageSuccess == 3:
					REPORTER("R3D3Y3.log", "...")
					MessageSuccess += 1
				try:
					for x in range(len(Messages['messages'])):
						SingleMessage = NoHTMLEscape.unescape(bleach.clean(Messages['messages'][x].rstrip(), tags=[], strip=True)).strip()
						if ProperMessage.match(SingleMessage) and not PrivateMessage.match(SingleMessage):
							try:
								StringMessage = str(SingleMessage)
								if StringMessage != "":
									with codecs.open("parachat.log", "a", encoding="utf-8") as ParachatLog:
										LogMessage = re.sub(u'&amp;', u'&', re.sub(u'&gt;', u'>', re.sub(u'&lt;', u'<', re.sub(u'&quot;', u'"', SingleMessage, re.UNICODE), re.UNICODE), re.UNICODE), re.UNICODE)
										ParachatLog.write(unicode(datetime.datetime.now().date()) + u'~' + unicode(datetime.datetime.now().time()) + u'>>' + LogMessage + u'\r\n')
							except Exception:
								with codecs.open("parachat.log", "a", encoding="utf-8") as ParachatLog:
									LogMessage = re.sub(u'&amp;', u'&', re.sub(u'&gt;', u'>', re.sub(u'&lt;', u'<', re.sub(u'&quot;', u'"', SingleMessage, re.UNICODE), re.UNICODE), re.UNICODE), re.UNICODE)
									ParachatLog.write(unicode(datetime.datetime.now().date()) + u'~' + unicode(datetime.datetime.now().time()) + u'>>' + LogMessage + u'\r\n')
				except Exception:
					time.sleep(0)
			else:
				REPORTER("R3D3Y3.log", "Failed to gather new messages. Error {" + str(Messages['error']) + "}")
				MessageSuccess = 0
				MessageURL = str(LOGIN())
		except Exception:
			REPORTER("R3D3Y3.log", "Failied to connect to site or site returned unexpected data.")
			MessageSuccess = 0
			MessageURL = str(LOGIN())
MAIN()
