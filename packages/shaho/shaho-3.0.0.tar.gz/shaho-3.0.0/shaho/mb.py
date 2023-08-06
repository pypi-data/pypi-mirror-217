import base64
from json import dumps, loads
from random import randint,choice
import datetime
import math
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from requests import post
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
from json import dumps, loads
import random
from requests import post, get
import urllib
import io
from urllib import request
from pathlib import Path
from re import findall
from PIL import Image , ImageFont, ImageDraw
from tinytag import TinyTag
class encryption:
	def __init__(self, auth:str, private_key:str=None):

		self.key = bytearray(self.secret(auth), "UTF-8")
		self.iv = bytearray.fromhex('00000000000000000000000000000000')
		if private_key:
			self.keypair = RSA.import_key(private_key.encode("utf-8"))

	def replaceCharAt(self, e, t, i):
		return e[0:t] + i + e[t + len(i):]

	def changeAuthType(auth_enc):
		"""this function lines 78511 to 78746 and decode it very hard about 3 ,4 hour 
			\nmake key of encryption to key of request 
		"""
		n = ""
		lowercase = "abcdefghijklmnopqrstuvwxyz"
		uppercase = "abcdefghijklmnopqrstuvwxyz".upper()
		digits = "0123456789"
		for s in auth_enc:
			if s in lowercase:
				n += chr(((32 - (ord(s) - 97)) % 26) + 97)
			elif s in uppercase:
				n += chr(((29- (ord(s) - 65)) % 26) + 65)
			elif s in digits:
				n += chr(((13 - (ord(s)- 48)) % 10) + 48)
			else:
				n += s
		return n
	
	def secret(self, e):
		t = e[0:8]
		i = e[8:16]
		n = e[16:24] + t + e[24:32] + i
		s = 0
		while s < len(n):
			e = n[s]
			if e >= '0' and e <= '9':
				t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
				n = self.replaceCharAt(n, s, t)
			else:
				t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
				n = self.replaceCharAt(n, s, t)
			s += 1
		return n

	def encrypt(self, text):
		raw = pad(text.encode('UTF-8'), AES.block_size)
		aes = AES.new(self.key, AES.MODE_CBC, self.iv)
		enc = aes.encrypt(raw)
		result = base64.b64encode(enc).decode('UTF-8')
		return result

	def decrypt(self, text):
		aes = AES.new(self.key, AES.MODE_CBC, self.iv)
		dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8')))
		result = unpad(dec, AES.block_size).decode('UTF-8')
		return result

	def makeSignFromData(self, data_enc:str):
		"""2000 line of rubika web encoded source 
		  \ndecoded and cleaned and summarized using pycryptodome
		"""
		sha_data = SHA256.new(data_enc.encode("utf-8"))
		signature = pkcs1_15.new(self.keypair).sign(sha_data)
		return base64.b64encode(signature).decode("utf-8")

	def decryptRsaOaep(private:str,data_enc:str):
		keyPair = RSA.import_key(private.encode("utf-8"))
		return PKCS1_OAEP.new(keyPair).decrypt(base64.b64decode(data_enc)).decode("utf-8")
class Bot:
	def __init__(self, auth, private_key=None,is_auth_send=True,base64decode_private=False,useragent=None):	
		if is_auth_send:
			self.auth = encryption.changeAuthType(auth)
			self.auth_send = auth
		else:
			self.auth = auth
			self.auth_send = encryption.changeAuthType(auth)
		if base64decode_private:
			private_key = loads(base64.b64decode(private_key).decode("utf-8"))['d']
		self.enc = encryption(self.auth,private_key if private_key else None)
		self.default_client = {
							"app_name":"Main",
							"app_version":"4.3.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
							}
		self.default_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0" if not useragent else useragent
	def get_url(self):
		p = None
		while 1:
			try:
				datax = {"api_version":"4","method":"getDCs","client":{"app_name":"Main","app_version":"4.3.1","platform":"Web","package":"web.rubika.ir","lang_code":"fa"}}
				p = post(json=datax,url='https://getdcmess.iranlms.ir/',headers={
        			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
					'Origin':'https://web.rubika.ir',
					'Referer':'https://web.rubika.ir/',
					'Host':'getdcmess.iranlms.ir'
        		}).json()
				break
			except Exception as e:
				print(e)
				continue
		p = p['data']['default_api_urls'][1]
		return p
	
	def send_data(self,input,method,client=None,api_version="6",tmp=False):
		p = None
		while 1:
			try:
				data_ = {
					"api_version":api_version,
					"auth" if not tmp else "tmp_session":self.auth_send if not tmp else self.auth,
					"data_enc":self.enc.encrypt(dumps({
						"method":method,
						"input":input,
						"client": client if client else self.default_client
					})),
				}
				if api_version == "6" and tmp == False:
					data_["sign"] = self.enc.makeSignFromData(data_["data_enc"])
				url:str = "https://messengerg2c"+str(randint(1,69))+".iranlms.ir/"
				p = post(json=data_,url=url,headers={'User-Agent': self.default_agent,
                    'Origin':'https://web.rubika.ir',
					'Referer':'https://web.rubika.ir/',
					'Host':url.replace("https://","").replace("/","")})
				p = p.json()
				break
			except Exception as e:
				print(e)
				continue
		p = loads(self.enc.decrypt(p["data_enc"]))
		return p
	
	def sendMessage(self, chat_id,text,metadata=[],message_id=None):
		input = {
			"object_guid":chat_id,
                "rnd":f"{randint(100000,999999999)}",
                "text":text,
                "reply_to_message_id":message_id
		}
		if metadata != [] : input["metadata"] = {"meta_data_parts":metadata}
		method = "sendMessage"
		return self.send_data(input,method)
	
	def makeRandomTmpSession():
		chars = "abcdefghijklmnopqrstuvwxyz"
		tmp = ""
		for i in range(32):
			tmp += choice(chars)
		return tmp
	
	def sendCode(phone:str,pass_key=None,type="SMS"):
		input = {
      		"phone_number":phone,
        	"send_type":"SMS"
        }
		if pass_key:
			input['pass_key'] = pass_key
		method = "sendCode"
		tmp = Bot.makeRandomTmpSession()
		b = Bot(tmp,False)  
		return tmp , b.send_data(input,method,tmp=True)
	
	def rsaKeyGenrate():
		keyPair = RSA.generate(1024)
		public = encryption.changeAuthType(base64.b64encode(keyPair.publickey().export_key()).decode("utf-8"))
		privarte = keyPair.export_key().decode("utf-8")
		return public,privarte
	
	def signIn(tmp,phone,phone_code,hash,public_key=None):
		public , private = Bot.rsaKeyGenrate()
		input = {
			"phone_number":phone,
			"phone_code_hash":hash,
			"phone_code":str(phone_code),
			"public_key":public if not public_key else public_key
		}
		method = "signIn"
		b = Bot(tmp,is_auth_send=False)  
		request = b.send_data(input,method,tmp=True)
		print(request)
		if request['status'] == "OK" and request['data']['status'] == "OK":
			auth = encryption.decryptRsaOaep(private,request['data']['auth'])
			guid = request['data']['user']['user_guid']	
			return auth , guid, private
		else:
			return None
	
	def registerDevice(self,systemversion,device_model,device_hash):
		input = {
			"token_type":"Web",
			"token":"",
			"app_version":"WB_4.3.1",
			"lang_code": "fa",
			"system_version": systemversion,
			"device_model": device_model,
			"device_hash" : device_hash
		}
		print(input)
		method = "registerDevice"
		return self.send_data(input,method)
	
	def getMyStickerSets(self):
		input = {}
		method = "getMyStickerSets"
		return self.send_data(input,method)
		
	def getChatsUpdate(self):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		input = {"state":time_stamp}
		method = "getChatsUpdates"
		return self.send_data(input,method)

	def deleteMessages(self, chat_id, message_ids):
		input = {
		"object_guid":chat_id,
		"message_ids":message_ids,
		 "type":"Global"}
		method = "deleteMessages"
		return self.send_data(input,method)

	def getMessages(self, chat_id, min_id):
		input = {
		"object_guid":chat_id,
		"middle_message_id":min_id}
		method = "getMessagesInterval"
		return self.send_data(input,method)

	def getChats(self, start_id=None):
		input = {
		"start_id":start_id}
		method = "getChats"
		return self.send_data(input,method)

	def getInfoByUsername(self, username):
		input = {"username":username}
		method = "getObjectByUsername"
		return self.send_data(input,method)

	def banGroupMember(self, chat_id, user_id):
		input = {
		"group_guid": chat_id,
		"member_guid": user_id,
		 "action":"Set"}
		method = "banGroupMember"
		return self.send_data(input,method)

	def unbanGroupMember(self, chat_id, user_id):
		input = {
		"group_guid": chat_id,
		"member_guid": user_id,
		"action":"Unset"}
		method = "banGroupMember"
		return self.send_data(input,method)

	def getGroupInfo(self, chat_id):
		input = {"group_guid": chat_id}
		method = "getGroupInfo"
		return self.send_data(input,method)

	def invite(self, chat_id, user_ids):
		input = {
		"group_guid": chat_id,
		"member_guids": user_ids}
		method = "addGroupMembers"
		return self.send_data(input,method)

	def getMessagesInfo(self, chat_id, message_ids):
		input = {
		"object_guid": chat_id,
		"message_ids": message_ids}
		method = "getMessagesByID"
		return self.send_data(input,method)

	def setMembersAccess(self, chat_id, access_list):
		input = {
		"access_list": access_list,
		"group_guid": chat_id}
		method = "setGroupDefaultAccess"
		return self.send_data(input,method)

	def getGroupMembers(self, chat_id, start_id=None):
		input = {
		"group_guid": chat_id,
		"start_id": start_id}
		method = "getGroupAllMembers"
		return self.send_data(input,method)

	def forwardMessages(self, From, message_ids, to):
		input = {
		"from_object_guid": From,
		"message_ids": message_ids,
		"rnd": f"{randint(100000,999999999)}",
		"to_object_guid": to}
		method = "forwardMessages"
		return self.send_data(input,method)

	def joinGroup(self, link):
		hashLink = link.split("/")[-1]
		input = {
		"hash_link": hashLink}
		method = "joinGroup"
		return self.send_data(input,method)

	def deleteChatHistory(self, chat_id, msg_id):
		input = {
		"last_message_id": msg_id,
		"object_guid": chat_id}
		method = "deleteChatHistory"
		return self.send_data(input,method)

	def leaveGroup(self,chat_id):
		if "https://" in chat_id:
			guid = Bot.joinGroup(self,chat_id)["data"]["group"]["group_guid"]
		else:
			guid = chat_id
		input = {"group_guid": guid}
		method = "leaveGroup"
		return self.send_data(input,method)

	def getChannelMembers(self, channel_guid, text=None, start_id=None):
		input = {
		"channel_guid":channel_guid,
		"search_text":text,
		"start_id":start_id,}
		method = "getChannelAllMembers"
		return self.send_data(input,method)

	def startVoiceChat(self, chat_id):
		input = {
		"chat_guid":chat_id}
		method = "createGroupVoiceChat"
		return self.send_data(input,method)

	def getUserInfo(self, chat_id):
		input = {
		"user_guid":chat_id}
		method = "getUserInfo"
		return self.send_data(input,method)

	def finishVoiceChat(self, chat_id, voice_chat_id):
		input = {
		"chat_guid":chat_id,
		"voice_chat_id" : voice_chat_id}
		method = "discardGroupVoiceChat"
		return self.send_data(input,method)

	def getMessagesChats(self, start_id=None):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		input = {
		"start_id":start_id}
		method = "getChats"
		return self.send_data(input,method)

	def _requestSendFile(self, file):
		input = {
		"file_name": str(file.split("/")[-1]),
		"mime": file.split(".")[-1],
		"size": Path(file).stat().st_size}
		method = "requestSendFile"
		return self.send_data(input,method)

	def _uploadFile(self, file):
		if not "http" in file:
			REQUES = Bot._requestSendFile(self, file)
			print(REQUES)
			bytef = open(file,"rb").read()
			hash_send = REQUES["data"]["access_hash_send"]
			file_id = REQUES["data"]["id"]
			url = REQUES["data"]["upload_url"]
			header = {
                'auth':self.auth,
                'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
                'chunk-size':str(Path(file).stat().st_size),
                'file-id':str(file_id),
                'access-hash-send':hash_send,
                "content-type": "application/octet-stream",
                "content-length": str(Path(file).stat().st_size),
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.12.1"
            }
			if len(bytef) <= 131072:
				header["part-number"], header["total-part"] = "1","1"
				while True:
					try:
						j = post(data=bytef,url=url,headers=header).text
						j = loads(j)['data']['access_hash_rec']
						break
					except Exception as e:
						continue
				return [REQUES, j]
			else:
				t = round(len(bytef) / 131072 + 1)
				for i in range(1,t+1):
					if i != t:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
								o = post(data=bytef[k:k + 131072],url=url,headers=header).text
								o = loads(o)['data']
								break
							except Exception as e:
								continue
					else:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
								p = post(data=bytef[k:],url=url,headers=header).text
								p = loads(p)['data']['access_hash_rec']
								break
							except Exception as e:
								continue
						return [REQUES, p]
		else:
			input = {
			"file_name": file.split("/")[-1],
			"mime": file.split(".")[-1],
			"size": len(get(file).content)}
			method = "requestSendFile"
			REQUES = self.send_data(input,method)
			hash_send = REQUES["data"]["access_hash_send"]
			file_id = REQUES["data"]["id"]
			url = REQUES["data"]["upload_url"]
			bytef = get(file).content
			header = {
                'auth':self.Auth,
                'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
                'chunk-size':str(len(get(file).content)),
                'file-id':str(file_id),
                'access-hash-send':hash_send,
                "content-type": "application/octet-stream",
                "content-length": str(len(get(file).content)),
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.12.1"
            }
			if len(bytef) <= 131072:
				header["part-number"], header["total-part"] = "1","1"
				while True:
					try:
						j = post(data=bytef,url=url,headers=header).text
						j = loads(j)['data']['access_hash_rec']
						break
					except Exception as e:
						continue
				return [REQUES, j]
			else:
				t = round(len(bytef) / 131072 + 1)
				for i in range(1,t+1):
					if i != t:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
								o = post(data=bytef[k:k + 131072],url=url,headers=header).text
								o = loads(o)['data']
								break
							except Exception as e:
								continue
					else:
					    k = i - 1
					    k = k * 131072
					    while True:
					    	try:
					    		header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
					    		p = post(data=bytef[k:],url=url,headers=header).text
					    		p = loads(p)['data']['access_hash_rec']
					    		break
					    	except Exception as e:
					    	  continue
					    return [REQUES, p]
            

	def getChatGroup(self,guid_gap):
		while 1:
			try:
				lastmessages = Bot.getGroupInfo(self, guid_gap)["data"]["chat"]["last_message_id"]
				messages = Bot.getMessages(self, guid_gap, lastmessages)
				return messages
				break
			except:
				continue

	def sendDocument(self, chat_id, file, caption=None, message_id=None):
		uresponse = Bot._uploadFile(self, file)
		print(uresponse)
		file_id = str(uresponse[0]["data"]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["data"]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))
		input = {
		"object_guid":chat_id,
		"reply_to_message_id":message_id,
		"rnd":f"{randint(100000,999999999)}",
		"file_inline":{
		"dc_id":str(dc_id),
		 "file_id":str(file_id),
		 "type":"File",
		 "file_name":file_name,
		 "size":size,
		 "mime":mime,
		 "access_hash_rec":access_hash_rec}}
		if caption != None: input["text"] = caption
		method = "sendMessage"
		return self.send_data(input,method)

	def sendVoice(self, chat_id, file, time, caption=None, message_id=None):
	       uresponse = Bot._uploadFile(self, file)
	       file_id = str(uresponse[0]["data"]["id"])
	       mime = file.split(".")[-1]
	       dc_id = uresponse[0]["data"]["dc_id"]
	       access_hash_rec = uresponse[1]
	       file_name = file.split("/")[-1]
	       size = str(len(get(file).content if "http" in file else open(file,"rb").read()))
	       input = {
			"file_inline": {
			"dc_id": dc_id,
			"file_id": file_id,
			"type":"Voice",
			"file_name": file_name,
			"size": size,
			"time": time,
			"mime": mime,
			"access_hash_rec": access_hash_rec},
			"object_guid":chat_id,
			"rnd":f"{randint(100000,999999999)}",
			"reply_to_message_id":message_id}
	       method = "getChannelAllMembers"
	       if caption != None: input["text"] = caption
	       return self.send_data(input,method)

	def getGroupAdmins(self, chat_id):
		input = {
		"group_guid":chat_id}
		method = "getGroupAdminMembers"
		return self.send_data(input,method)

	def getChannelMembers(self, channel_guid, text=None, start_id=None):
		input = {
		"channel_guid":channel_guid,
		"search_text":text,
		"start_id":start_id,}
		method = "getChannelAllMembers"
		return self.send_data(input,method)
	
	def getGroupLink(self, chat_id):
		input = {
		"group_guid":chat_id}
		method = "getGroupLink"
		return self.send_data(input,method)
		
	def requestFile(self, name, size , mime):
		input = {
		"file_name":name,
		"size":size,
		"mime":mime}
		method = "requestSendFile"
		return self.send_data(input,method)
		
		
	def fileUpload(self, bytef ,hash_send ,file_id ,url):
		if len(bytef) <= 131072:
			h = {
				'auth':self.auth,
				'chunk-size':str(len(bytef)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				'total-part':str(1),
				'part-number':str(1)
			}
			t = False
			while t == False:
				try:
					j = post(data=bytef,url=url,headers=h).text
					j = loads(j)['data']['access_hash_rec']
					t = True
				except:
					t = False
			
			return j
		else:
			t = len(bytef) / 131072
			t += 1
			t = math.floor(t)
			for i in range(1,t+1):
				if i != t:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							o = post(data=bytef[k:k + 131072],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(131072),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							o = loads(o)['data']
							t2 = True
						except:
							t2 = False
					j = k + 131072
					j = round(j / 1024)
					j2 = round(len(bytef) / 1024)
					print(str(j) + 'kb / ' + str(j2) + ' kb')                
				else:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							p = post(data=bytef[k:],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(len(bytef[k:])),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							p = loads(p)['data']['access_hash_rec']
							t2 = True
						except:
							t2 = False
					j2 = round(len(bytef) / 1024)
					print(str(j2) + 'kb / ' + str(j2) + ' kb') 
					return p
					
	
	def sendImage(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, thumb_inline , width , height, text=None, message_id=None):
		input = {
		"object_guid":chat_id,
		"rnd":f"{randint(100000,900000)}",
		"file_inline":{
		"dc_id":str(dc_id),
		"file_id":str(file_id),
		"type":"Image",
		"file_name":file_name,
		"size":size,
		"mime":mime,
		"access_hash_rec":access_hash_rec,
		'thumb_inline':thumb_inline,
		'width':width,
		'height':height}}
		method = "sendMessage"
		if text != None: input["text"] = text
		if message_id != None: input["reply_to_message_id"] = message_id
		return self.send_data(input,method)
		
	
	def getImageSize(self,image_bytes:bytes):
		im = Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return width , height
		
		
	
	def getThumbInline(self,image_bytes:bytes):
		im = Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)
		
		
		
	def sendVoice1(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, duration, text=None, message_id=None):
		input = {
		"object_guid":chat_id,
		"rnd":f"{randint(100000,900000)}",
		"file_inline":{
		"dc_id":str(dc_id),
		"file_id":str(file_id),
		"type":"Voice",
		"file_name":file_name,
		"size":size,
		"mime":mime,
		"access_hash_rec":access_hash_rec,
		'time':duration,}}
		method = "sendMessage"
		if text != None: input["text"] = text
		if message_id != None: input["reply_to_message_id"] = message_id
		return self.send_data(input,method)