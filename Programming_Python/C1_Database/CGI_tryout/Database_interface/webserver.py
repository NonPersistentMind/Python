import sys, os
from http.server import HTTPServer, CGIHTTPRequestHandler

webdir = '.'
port=8080

os.chdir(webdir)
srvrAddr = ('',port)
srvrObj = HTTPServer(srvrAddr, CGIHTTPRequestHandler)
srvrObj.serve_forever()