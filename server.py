#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        # self.url = "http://127.0.0.1:8080"
        split_data = self.data.decode('utf-8').split(' ')
        method = split_data[0]

        if (len(split_data) > 1):
            filename = split_data[1] # PROBABLY WILL NEED TO CHANGE
            # self.url += "/www" + filename

        # Can only handle GET method, not POST/PUT/DELETE
        if (method != "GET"):
            self.cannot_handle_method()
        elif filename == "/":
            # print("TRUE")
            # directories = os.listdir('www/')
            # for d in directories:
            #     print(d, "\r\n")
            #     self.request.sendall(bytearray(d, 'utf-8'))
            self.send_file("www/index.html")
        elif filename == "/deep/" or filename == "/deep":
            self.send_file("www/deep/index.html")
        else:
            # self.request.sendall(bytearray("200 OK\r\n",'utf-8'))
            self.send_file("www" + filename)

    def redirect(new_location):
        response = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + new_location
        self.request.send(bytearray(response, 'utf-8'))

    def cannot_handle_method(self):
        self.request.send(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n", 'utf-8'))

    def send_file(self, filename):
        # to_send = "Content-Type: text/html\r\n\r\n"
        to_send = ""
        try:
            req_file = open(filename, 'r')

            # if (filename.find('.') != -1):
            split_data = filename.split('.')
            content_type = split_data[1]

            try:
                content_length = os.path.getsize(filename)
            except:
                print("Failed to get length")
                content_length = 0
            else:
                print(content_length)

            to_send = "HTTP/1.1 200 OK\nContent-Type: text/" + content_type + "\r\n\r\n" #"\nContent-Length: " + content_length + 
            self.request.send(bytearray(to_send, 'utf-8'))

            to_send = ""
            for l in req_file:
                to_send += l

            self.request.sendall(bytearray(to_send, 'utf-8'))
            req_file.close()
        except:
            self.request.send(bytearray("HTTP/1.1 404 Not Found\r\n\r\n", 'utf-8'))
            # raise request.HTTPError(url=self.url, code=404, msg="Not Found", hdrs=None, fp=None)
            

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
