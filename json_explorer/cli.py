import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("json_explorer/template.html") as infile:
            html = infile.read()
        self.wfile.write(bytes(html, "utf-8"))


def start_browser(server_ready_event, url):
    server_ready_event.wait()
    webbrowser.open(url)


def main(ip="localhost", port=8001):
    name = "JSON Explorer"
    instruction = "press Control+C to stop"
    url = f"http://{ip}:{port}"

    server_ready = threading.Event()
    browser_thread = threading.Thread(
        target=start_browser,
        args=(server_ready, url),
    )
    browser_thread.start()

    server = HTTPServer((ip, port), RequestHandler)
    print(f"started {name} at {url}", file=sys.stderr)
    print(f"\033[1m{instruction}\033[0m\n", file=sys.stderr)
    server_ready.set()

    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.server_close()
        print(f"\rstopped {name}", file=sys.stderr)

    browser_thread.join()
