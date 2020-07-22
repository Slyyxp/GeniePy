import os
import logging
from datetime import datetime
from modules.utils import make_dir
from modules.config import prefs

def log_setup():
	# Generate filename
	filename = '{:%H.%M.%S}.log'.format(datetime.now())
	# Create subfolder based on today's date
	folder_name = os.path.join(prefs['log_directory'], '{:%Y-%m-%d}'.format(datetime.now()))
	make_dir(folder_name)
	# Set path of the log file
	log_path = os.path.join(folder_name, filename)
	# Set up logging to file
	logging.basicConfig(level=logging.DEBUG,
	                    handlers=[logging.FileHandler(log_path, 'w', 'utf-8')],
	                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
	                    datefmt='%Y-%m-%d %H:%M:%S')
	# Define a Handler which writes INFO messages or higher to the sys.stderr
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	# Set a format which is simpler for console use
	formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
	# Tell the handler to use this format
	console.setFormatter(formatter)
	# Add the handler to the root logger
	logging.getLogger("").addHandler(console)
	logger_genie = logging.getLogger("Genie")

	return logger_genie
