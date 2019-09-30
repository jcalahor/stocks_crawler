import socket
import urllib.request
import urllib.parse
from urllib import *
import re
import ast


def web_request(logger, ul):
    try:
        timeout = 10  # PROB 6 SECONDS SHOULD GO HERE
        socket.setdefaulttimeout(timeout)
        headers = {}
        headers[
            'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; Win 64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        req = urllib.request.Request(ul, headers=headers)
        resp = urllib.request.urlopen(req)
        t = resp.read().decode('utf-8')
        resp.close()
        return t
    except Exception as e:
        logger.exception(e)
        logger.info(ul)

