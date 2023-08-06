import socket
from .data import ThermostatData

class Trane:

	def __init__(self, host: str, port:int):#timeout=socket._GLOBAL_DEFAULT_TIMEOUT
		self.host = host
		self.port = port
		# self.timeout = timeout

	def validate(self):
		"""Validates whether the given host and port can be connected to.

		Returns:
			bool: whether or not the given host and port could successfully connect
		"""
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((self.host, self.port))
		except ConnectionRefusedError:
			return False
		finally:
			sock.close()
		
		return True



	def listen(self, bufsize=128):
		# set up TCP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sock.connect((self.host, self.port))
		# print(f"Connected to {self.ip}:{self.port}")
		try:
			while True:
				data = sock.recv(bufsize)
				if not data:
					break
				# strip newline and trailing null
				data = data[:-2]
				yield ThermostatData.from_data(data)
		except (TimeoutError, ConnectionAbortedError, ConnectionResetError) as e:
			# sockets generally either time out, close, or reset.
			# https://stackoverflow.com/a/15175067/
			print("Connection Error")
			print(e)
		finally:
			sock.close()