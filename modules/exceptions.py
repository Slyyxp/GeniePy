import logging

logger_exceptions = logging.getLogger("Exceptions")

class AuthenticationError(Exception):
	def __init__(self, message):
		logger_exceptions.debug(message)
		super().__init__(message)

class TrackRenameError(Exception):
	def __init__(self, message):
		logger_exceptions.debug(message)
		super().__init__(message)

class StreamMetadataError(Exception):
	def __init__(self, message):
		logger_exceptions.debug(message)
		super().__init__(message)

class NewDeviceError(Exception):
	def __init__(self, message):
		logger_exceptions.debug(message)
		super().__init__(message)
