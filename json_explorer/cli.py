import argparse
import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

from .explore import TripleCounter


def start_browser(server_ready_event, url):
    server_ready_event.wait()
    webbrowser.open(url)


def jsonl_iterator(filename):
    with open(filename) as infile:
        for line in infile:
            yield json.loads(line)


def main():
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument(
        "filename",
        help="filename of a file in JSON Lines format",
    )
    parser.add_argument("-p", "--port", default=8001, type=int, help="port for server (default 8001)")
    parser.add_argument("-n", "--no-serve", help="write HTML to stdout instead of serving", action="store_true")
    args = parser.parse_args()

    counter = TripleCounter.from_objects(jsonl_iterator(args.filename))
    response_text = counter.html()

    if args.no_serve:
        print(response_text)
        return

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(response_text, "utf-8"))

    name = "JSON Explorer"
    instruction = "press Control+C to stop"
    url = f"http://localhost:{args.port}"

    server_ready = threading.Event()
    browser_thread = threading.Thread(
        target=start_browser,
        args=(server_ready, url),
    )
    browser_thread.start()

    server = HTTPServer(("localhost", args.port), RequestHandler)
    print(f"started {name} at {url}", file=sys.stderr)
    print(f"\033[1m{instruction}\033[0m\n", file=sys.stderr)
    server_ready.set()

    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.server_close()
        print(f"\rstopped {name}", file=sys.stderr)

    browser_thread.join()
