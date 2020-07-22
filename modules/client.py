#!/usr/bin/env python3

import logging
import requests

import modules.config as cfg
import modules.exceptions as exceptions

logger_client = logging.getLogger("Client")


class Client:

	def __init__(self):
		self.session = requests.Session()
		self.credentials = cfg.credentials
		self.android_ver = "5.1.1"
		self.app_ver = 40807
		self.dev_id = "eb9d53a3c424f961"
		self.dev_model = "SM-G930L"
		self.ims_num = "72c4b5a6d16f65482ccd2657d833b9817329be12a586a7e37e1f602c56bde4c3"
		self.upnm = "MTU4MTEzOTgxNTg="
		self.usr_agent = "genie/ANDROID/5.1.1/WIFI/SM-G930L/dreamqltecaneb9d53a3c424f961/500200714/40807"

		self.session.headers.update({
			"User-Agent": self.usr_agent,
			"Referer": "app.genie.co.kr"
		})

	def make_call(self, sub, epoint, data):
		"""
		:param sub: Url Prefix
		:param epoint: Endpoint
		:param data: Post data
		:return: API Response

		Endpoints used:
			player/j_StmInfo.json - Provides information on the streamed track.
			member/j_Member_Login.json - Authentication.
			song/j_AlbumSongList.json - Provides album information.
		"""
		r = self.session.post("https://{}.genie.co.kr/{}".format(sub, epoint), data=data)
		r.raise_for_status()

		return r.json()

	def auth(self):
		"""
		Authenticate our session appearing as an Android device
		"""
		data = {
			"apvn": self.app_ver,
			"dcd": self.dev_id,
			"dvm": self.dev_model,
			"imsnm": self.ims_num,
			"mts": "Y",
			"ovn": self.android_ver,
			"sign": "Y",
			"svc": "IV",
			"tct": "Android",
			"uip": "172.17.100.15",
			"upnm": self.upnm,
			"uxd": self.credentials['username'],
			"uxx": self.credentials['password']
		}
		r = self.make_call("app", "member/j_Member_Login.json", data)
		if r['Result']['RetCode'] != "0":
			raise exceptions.AuthenticationError("Authentication failed.")
		else:
			logger_client.info("Login Successful.")
		self.usr_num = r['DATA0']['MemUno']
		self.usr_token = r['DATA0']['MemToken']
		self.stm_token = r['DATA0']['STM_TOKEN']


	def get_meta(self, id):
		"""
		:param id: Album ID.
		:return: API Response containing album metadata.
		"""
		data = {
			"apvn": self.app_ver,
			"axnm": id,
			"dcd": self.dev_id,
			"dvm": self.dev_model,
			"mts": "Y",
			"ovn": self.android_ver,
			"pg": 1,
			"pgsize": 100,
			"sign": "Y",
			"stk": self.stm_token,
			"svc": "IV",
			"tct": "Android",
			"uip": "172.17.100.15",
			"unm": self.usr_num,
			"uxtk": self.usr_token
		}
		r = self.make_call("app", "song/j_AlbumSongList.json", data)
		logger_client.debug(r)
		if r['Result']['RetCode'] != "0":
			raise Exception("Failed to get album metadata.")

		return r

	def get_stream_meta(self, id, q):
		"""
		:param id: Album ID
		:param q: Album quality.
		:return: API Response containing metadata for the currently streamed track.

		Quality options:
			1 - MP3
			2 - 16bit FLAC
			3 - 24bit FLAC
		"""
		data = {
			"apvn": self.app_ver,
			"bitrate": q,
			"dcd": self.dev_id,
			"dvm": self.dev_model,
			"mts": "Y",
			"ovn": self.android_ver,
			"sign": "Y",
			"stk": self.stm_token,
			"svc": "IV",
			"tct": "Android",
			"uip": "172.17.100.15",
			"unm": self.usr_num,
			"uxtk": self.usr_token,
			"xgnm": id
		}
		r = self.make_call("stm", "player/j_StmInfo.json", data)
		logger_client.debug(r)
		if r['Result']['RetCode'] == "A00003":
			raise exceptions.NewDeviceError("Device ID has changed since last stream.")
		if r['Result']['RetCode'] != "0":
			raise exceptions.StreamMetadataError("Failed to get stream metadata.")

		return r['DataSet']['DATA'][0]
