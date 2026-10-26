import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class WeddingHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def guess_type(self, path):
        if path.endswith(".js"):
            return "application/javascript; charset=utf-8"
        if path.endswith(".css"):
            return "text/css; charset=utf-8"
        if path.endswith(".html"):
            return "text/html; charset=utf-8"
        if path.endswith(".svg"):
            return "image/svg+xml; charset=utf-8"
        if path.endswith(".mp3"):
            return "audio/mpeg"
        if path.endswith(".webp"):
            return "image/webp"
        if path.endswith(".png"):
            return "image/png"
        if path.endswith(".jpg") or path.endswith(".jpeg"):
            return "image/jpeg"
        return super().guess_type(path)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

def main():
    server_address = ("127.0.0.1", PORT)
    httpd = ThreadingHTTPServer(server_address, WeddingHandler)
    print(f"Bengali Wedding Invitation serving at: http://localhost:{PORT}")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
