#! /usr/local/bin/python
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
from socketserver import TCPServer
from os import getpid
from pathlib import Path
from sys import argv
from signal import SIGTERM
from os import kill
import logging
from traceback import format_exception
from os import fork
from os import devnull
import sys
from urllib.request import urlretrieve
from pathlib import Path
from tempfile import TemporaryDirectory
import tarfile


LOGFILE = Path("~/.mypyref.log").expanduser()
PIDFILE = Path("~/.mypyref.pid").expanduser()
LOGFILE.unlink(missing_ok=True)

logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PORT = 9000
ROOT = Path("~/Documents/mypyref").expanduser()
PYTHON_VERSION = '3.11.4'
DIRNAME = f"python-{PYTHON_VERSION}-docs-html"


def main():

    command = argv[1]

    if command == 'start':
        if PIDFILE.is_file():
            raise Exception('MyPyDoc is already running')
        if fork() == 0:
            sys.stderr = open(devnull, 'w')
            sys.stdout = open(devnull, 'w')
            try:
                class MyHandler(SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        return super().__init__(*args, directory=ROOT/DIRNAME, **kwargs)
                with HTTPServer(("", PORT), MyHandler) as httpd:
                    pid = str(getpid())
                    PIDFILE.write_text(pid)
                    logging.info(f'Serving to port {PORT} as pid {pid}')
                    httpd.serve_forever()
            except Exception as e:
                logging.error(str(e) + "\n" + "".join(format_exception(e)))

    if command == 'stop':
        if not PIDFILE.is_file():
            raise Exception('MyPyDoc is not running')
        pid = PIDFILE.read_text()
        logging.info(f'Terminating process at pid {pid}')
        try:
            kill(int(pid), SIGTERM)
        except ProcessLookupError as e:
            logging.info(e)
        PIDFILE.unlink()
    
    if command == 'install':
        filename = f"{DIRNAME}.tar.bz2"
        url = f"https://docs.python.org/3/archives/{filename}"
        with TemporaryDirectory() as tempdir:
            tempfile = Path(tempdir) / filename
            urlretrieve(url, str(tempfile))
            with tarfile.open(tempfile, "r:bz2") as tar:
                tar.extractall(ROOT)
