##############################################################################################################
#                       #   Parachat logging software AKA: "R3D3Y3"                                          #
#  \                 /  #   Version 1.1.a                                                                    #
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
import httplib ,urllib, time, re, datetime, json, sys, string, random
from random import randint
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
			try:
				R3D3Y3Log = open('R3D3Y3.log', 'a')
				R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Initiated new session with username \"" + UserName + "\" and session key \"" + Chat_Key + "\"\n")
				R3D3Y3Log.close()
			except Exception:
				R3D3Y3Log = open('R3D3Y3.log', 'w+')
				R3D3Y3Log.close()
				R3D3Y3Log = open('R3D3Y3.log', 'a')
				R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Initiated new session with username \"" + UserName + "\" and session key \"" + Chat_Key + "\"\n")
				R3D3Y3Log.close()
			LoginFailed = 0
			return str("http://members.parachat.com:8080/basic/wap/reqpub.jsp?site=iPhone&key=" + Chat_Key + "&room=iPhone&user=" + UserName)
		except Exception:
			try:
				R3D3Y3Log = open('R3D3Y3.log', 'a')
				R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Failed to initiate a new session." + "\n")
				R3D3Y3Log.close()
				time.sleep(30)
			except Exception:
				R3D3Y3Log = open('R3D3Y3.log', 'w+')
				R3D3Y3Log.close()
				R3D3Y3Log = open('R3D3Y3.log', 'a')
				R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Failed to initiate a new session." + "\n")
				R3D3Y3Log.close()
				time.sleep(30)
def MESSAGE_HANDLER(Messages):
	Messages_Unformatted = re.search("(.*)</a>:(.*)",Messages)
	try:
		Messages_Divided = re.sub('" >', '\n', Messages_Unformatted.group())
		Messages_ChatOnly = re.sub("(.*)javascript:paraShowOne(.*)", "\n", Messages_Divided) 
		Messages_Formatted = str(re.sub("&amp;quot;", "\"", str(re.sub("&amp;amp;", "&", str(re.sub("&amp;lt;", "<", str(re.sub("&amp;gt;", ">", str(re.sub("<(.*?)>", "", str(re.sub('\n', '', str(re.sub('</a>: ',": ", str(re.sub("']", "", str(re.sub("', u'(.*)", "", Messages_ChatOnly)))))))))))))))))).decode('string_escape')
		Messages_LogEntry = str(datetime.datetime.now().date()) + "~" + str(datetime.datetime.now().time()) + ">> " + str(Messages_Formatted) + "\n"
		try:
			ChatLogFile = open('ParachatLog.txt', 'a')
			ChatLogFile.write(Messages_LogEntry)
			ChatLogFile.close()
		except Exception:
			ChatLogFile = open('ParachatLog.txt', 'w+')
			ChatLogFile.close()
			ChatLogFile = open('ParachatLog.txt', 'a')
			ChatLogFile.write(Messages_LogEntry)
			ChatLogFile.close()
	except Exception:
		time.sleep(0)
def MAIN():
	MessageURL = str(LOGIN())
	MessageSuccess = 0 
	while 1:
		try:
			Site_Reply = urllib.urlopen(MessageURL)
			Raw_Messages = Site_Reply.read()
			Messages = json.loads(Raw_Messages)
			if Messages['success']:
				try:
					R3D3Y3Log = open('R3D3Y3.log', 'a')
					if MessageSuccess < 3:
						R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Successfully gathered new messages." + "\n")
						R3D3Y3Log.close()
						MessageSuccess += 1
					elif MessageSuccess == 3:
						R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "..." + "\n")
						R3D3Y3Log.close()
						MessageSuccess += 1
				except Exception:
					R3D3Y3Log = open('R3D3Y3.log', 'w+')
					R3D3Y3Log.close()
					if MessageSuccess < 3:
						R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Successfully gathered new messages." + "\n")
						R3D3Y3Log.close()
						MessageSuccess += 1
					elif MessageSuccess == 3:
						R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "..." + "\n")
						R3D3Y3Log.close()
						MessageSuccess += 1
				MESSAGE_HANDLER(str(Messages['messages']))
			else:
				try:
					R3D3Y3Log = open('R3D3Y3.log', 'a')
					R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Failed to gather new messages. Error returned: \"" + str(Messages['error']) + "\"\n")
					R3D3Y3Log.close()
				except Exception:
					R3D3Y3Log = open('R3D3Y3.log', 'w+')
					R3D3Y3Log.close()
					R3D3Y3Log = open('R3D3Y3.log', 'a')
					R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Failed to gather new messages. Error returned: \"" + str(Messages['error']) + "\"\n")
					R3D3Y3Log.close()
				MessageSuccess = 0
				MessageURL = str(LOGIN())
		except Exception:
			try:
				R3D3Y3Log = open('R3D3Y3.log', 'a')
				R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Failied to connect to site or site returned unexpected data." + "\n")
				R3D3Y3Log.close()
			except Exception:
				R3D3Y3Log = open('R3D3Y3.log', 'w+')
				R3D3Y3Log.close()
				R3D3Y3Log = open('R3D3Y3.log', 'a')
				R3D3Y3Log.write(str(datetime.datetime.now().date()) + "," + str(datetime.datetime.now().time()) + "," + "Failied to connect to site or site returned unexpected data." + "\n")
				R3D3Y3Log.close()
			MessageSuccess = 0
			MessageURL = str(LOGIN())
MAIN()
