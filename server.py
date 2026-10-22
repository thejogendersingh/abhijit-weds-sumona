from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import socket
import os

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

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
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

class DualStackServer(ThreadingHTTPServer):
    address_family = socket.AF_INET6
    def server_bind(self):
        try:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except (AttributeError, OSError):
            pass
        return super().server_bind()

if __name__ == "__main__":
    try:
        server = DualStackServer(("", PORT), Handler)
    except Exception:
        # Fallback to standard IPv4 if IPv6 not supported
        server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    
    print(f"Serving wedding invitation at http://127.0.0.1:{PORT} and http://localhost:{PORT}")
    server.serve_forever()
