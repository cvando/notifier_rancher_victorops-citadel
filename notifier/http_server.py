import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from rancher import routing

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_header("Content-type", "text/html")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self._html("ok"))

    def _html(self, message):
        content = "<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")

    def do_GET(self):
        self._set_response()
        print("GET request "+str(self.path), flush=True)

    def do_POST(self):
        self._set_response()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        routing(post_data)
        print("POST request "+str(self.path), flush=True)

def run(server_class=HTTPServer, handler_class=S, port=8090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n', flush=True)