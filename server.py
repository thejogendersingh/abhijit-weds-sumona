from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import socket
import threading
import os
import time

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(SimpleHTTPRequestHandler):
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
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

class ServerV6(ThreadingHTTPServer):
    address_family = socket.AF_INET6

def start_server():
    servers = []
    
    # IPv4 server (covers 127.0.0.1 and network IP)
    try:
        s4 = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
        servers.append(s4)
        threading.Thread(target=s4.serve_forever, daemon=True).start()
    except Exception as e:
        print(f"IPv4 server notice: {e}")

    # IPv6 server (covers localhost resolving to ::1 on Windows)
    try:
        s6 = ServerV6(("::1", PORT), Handler)
        servers.append(s6)
        threading.Thread(target=s6.serve_forever, daemon=True).start()
    except Exception as e:
        pass

    print(f"Serving wedding invitation at http://127.0.0.1:{PORT} and http://localhost:{PORT}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        for s in servers:
            s.shutdown()

if __name__ == "__main__":
    start_server()
