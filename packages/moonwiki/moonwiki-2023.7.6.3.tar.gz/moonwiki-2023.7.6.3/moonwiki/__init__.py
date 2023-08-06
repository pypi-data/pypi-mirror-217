class moonwiki(object): # A bit of support 4 2.0
	def __init__(self, wD):
		import os
		if str(wD) != wD:
			wD = "wiki"
		if not os.path.isdir(wD):
			raise TypeError(f"\"{wD}\" is not a directory")
		self.wD = wD
	def run(self, host, port):
		from http.server import HTTPServer, BaseHTTPRequestHandler
		import socket
		from configparser import ConfigParser as Inifile
		import os
		cfg = Inifile()
		if not os.path.isfile(os.path.join(wD, "settings.ini")):
			raise RuntimeError(f"Cannot get {os.path.join(wD, 'settings.ini')}")
		class moonwikiRequestHandler(BaseHTTPRequestHandler):
			def do_GET(self):
				if self.path == "/":
					self.send_response(200)
					self.send_header("Content-type", "text/html")
					self.end_headers()
					self.wfile.write("Test server".encode())
			def log_message(self, format, *args):
				pass
		serv = HTTPServer((host, port), moonwikiRequestHandler)
		print (f"moonwiki running @ http://{host}:{port}/")
		serv.serve_forever()