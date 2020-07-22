import os
import re
import platform
import logging

logger_utilities = logging.getLogger("Utilities")


def print_title():
	print("""
 _______               __         ______        
|     __|.-----.-----.|__|.-----.|   __ \.--.--.
|    |  ||  -__|     ||  ||  -__||    __/|  |  |
|_______||_____|__|__||__||_____||___|   |___  |
                                         |_____|

   """)


def allowed_check(allowed):
	if allowed == "Y":
		return True
	print("Track is not allowed to be streamed.")


def parse_specs(type, br):
	return {
		"MP3": "MP3 " + br,
		"FLA": "16-bit / 44.1 kHz FLAC",
		"F44": "24-bit / 44.1 kHz FLAC",
		"F48": "24-bit / 48 kHz FLAC",
		"F88": "24-bit / 88.2 kHz FLAC",
		"F96": "24-bit / 96 kHz FLAC",
		"F192": "24-bit / 192 kHz FLAC"
	}[type]


def get_ext(type):
	if type == "MP3":
		return "mp3"
	else:
		return "flac"


def make_dir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)


def exist_check(abs):
	"""
	:param abs: Absolute path
	:return: If path exists.
	"""
	if os.path.isfile(abs):
		logger_utilities.info("{} already exists locally.".format(os.path.basename(abs)))
		return True


def _is_win():
	if platform.system() == 'Windows':
		return True


def sanitize(fn):
	"""
	:param fn: Filename
	:return: Sanitized string

	Removes invalid characters in the filename dependant on Operating System.
	"""
	if _is_win():
		return re.sub(r'[\/:*?"><|]', '_', fn)
	else:
		return re.sub('/', '_', fn)


def check_url(url):
	"""
	:param url: Genie url
	:return: Album ID
	"""
	expression = "https://www\.genie\.co\.kr/detail/albumInfo\?axnm=(\d{8})$"
	match = re.match(expression, url)
	if match:
		return match.group(1)
	logger_utilities.critical("Invalid URL: {}".format(url))
