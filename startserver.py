import os
import socket


class TCPServer:
    host = '127.0.0.1'
    port = 8888

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        print('Server is listening on port {} at {}'.format(self.port, s.getsockname()))

        while True:
            conn, addr = s.accept()
            print("Connected by {}".format(addr))
            data = conn.recv(1024)

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

    def handle_request(self, data):
        return data


class HTTPServer(TCPServer):
    headers = {
        'Server': 'DaxWebServer',
        'Content-Type': 'text/html; charset=utf-8',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        500: 'Internal Server Error',
        501: 'Not Implemented',
    }

    def handle_request(self, data):

        request = HTTPRequest(data)

        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)

        return response

    def response_line(self, status_code):
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 {} {}\r\n".format(status_code, reason)
        return line.encode('utf-8')

    def response_headers(self, extra_headers=None):
        headers_copy = self.headers.copy()

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "{}: {}\r\n".format(h, headers_copy[h])

        return headers.encode()

    def handle_GET(self, request):
        filename = request.uri.strip('/')

        if filename == "":
            response_line = self.response_line(200)
    
            response_headers = self.response_headers()
    
            with open("index.html", 'rb') as f:
                response_body = f.read()

        elif not filename.endswith('.html'):
            response_line = self.response_line(501)
            response_headers = self.response_headers()
            response_body = b"<h1>Not Implemented</h1>"

        elif os.path.exists(filename):
            response_line = self.response_line(200)
            response_headers = self.response_headers()

            with open(filename, 'rb') as f:
                response_body = f.read()
        
        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = b"<h1>404 Not Found</h1>"

        blank_line = b"\r\n"

        return b"".join([response_line, response_headers, blank_line, response_body])

    def HTTP_501_handler(self, request):
        response_line = self.response_line(501)

        response_headers = self.response_headers()

        blank_line = b"\r\n"

        response_body = b"<h1>501 Not Implemented</h1>"

        return b"".join([response_line, response_headers, blank_line, response_body])


class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = "1.1"

        self.parse(data)

    def parse(self, data):
        lines = data.split(b"\r\n")

        request_line = lines[0]

        words = request_line.split(b" ")

        self.method = words[0].decode()

        if len(words) > 1:
            self.uri = words[1].decode()

        if len(words) > 2:
            self.http_version = words[2]


if __name__ == '__main__':
    server = HTTPServer()
    server.start()
