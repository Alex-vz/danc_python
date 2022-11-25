#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
import argparse
from pathlib import Path

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import traceback

from urllib.parse import urlparse, parse_qs

import danc_python as danc


def list_dir(base_dir, dirname):
    """
    """
    ld, descr = danc.list_dir(base_dir, dirname)
    if not descr:
        c_title = "Каталог"
        c_description = ""
    else:
        c_title = descr["title"]
        c_description = descr["description"]

    res = "<ul>"

    for itm in ld:
        if itm["is_dir"]:
            title = "[{}]".format(itm["title"])
            link = itm["link"]+"/"
        else:
            title = itm["title"]
            link = itm["link"]

        if itm["link"]:
            res += '<li><a href="{link}" title="{description}">{title}</a></li>'.format(link=link, title=title, description=itm["description"])
        else:
            res += '<li title={description}>{title}</li>'.format(title=title, description=itm["description"])

    res += "</ul>"

    return res, c_title, c_description


def proc_dir(base_dir, path):
    base_dir, path = _dir_clear(base_dir, path)
    content, title, description = list_dir(base_dir, path)
    return DIR_BODY.format(content=content, title=title, description=description)


def proc_module(base_dir, path):
    #base_dir, path = _dir_clear(base_dir, path)

    #in_file = base_dir + path 
    base_dir = Path(base_dir)
    path = Path("."+path)

    in_file = base_dir / path 

    try:
        module = danc.load_module(in_file)
    except Exception as e:
        traceback.print_exc()
        return '<div style="color:red;fomt-weight:bold;">Ошибка иморта</div>'

    dtype = module.get("DIAGRAM_TYPE")
    if not dtype:
        return '<div style="color:red;fomt-weight:bold;">Неизвестный тип диаграммы</div>'

    draw_func = module.get("draw")
    code_block = module.get("CODE")
    if not (draw_func or code_block):
        return '<div style="color:red;fomt-weight:bold;">Неопределен код диаграммы</div>'


    title = module.get("TITLE", str(path))
    description = module.get("DESCRIPTION", "&nbsp;")
    detail = module.get("DETAIL", "&nbsp;")

    diagram = danc.Diagram()
    try:
        d = diagram.init_draw(dtype)
        if draw_func:
            draw_func(d)
        else:
            d.code(code_block)
        image_url = diagram.perp_url(d)
    except Exception as e:
        traceback.print_exc()
        return '<div style="color:red;fomt-weight:bold;">Ошибка при генерации</div>'

    return MODULE_BODY.format(title=title,description=description,image_url=image_url,detail=detail)


BODY = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>Examples</title>
    <meta name="description" content="">
    <meta name="keywords" content="">
    <link href="" rel="stylesheet">
    </head>
    <body>
        {content}
    </body>
    </html>
"""

DIR_BODY = """
    <h1 title="{description}">{title}</h1>
    <div>{content}</div>
"""

MODULE_BODY = """
    <h1>{title}</h1>
    <div>{description}</div>
    <div>
        <img src="{image_url}">
    </div>
    <div>{detail}</div>
"""

def _dir_clear(base_dir, dir_path):
    base_dir = base_dir.rstrip("/")
    dir_path = dir_path.rstrip("/")
    if not dir_path or dir_path=="/":
        dir_path = ""
    elif not dir_path.startswith("/"):
        dir_path = "/"+dir_path
    return base_dir, dir_path


class S(BaseHTTPRequestHandler):

    BASE_DIR = "."

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        msg = "GET request for {}".format(self.path)
        urp = urlparse(self.path)
        #print(urp)
        #print(parse_qs(urp.query))
        cpath=urp.path
        if cpath=="/favicon.ico":
            return
        elif cpath.endswith(".py"):
            content = proc_module(self.BASE_DIR, cpath)
        else:
            content = proc_dir(self.BASE_DIR, cpath)
        self.wfile.write(BODY.format(request=msg, content=content).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(args):
    server_class = HTTPServer 
    handler_class = S 
    S.BASE_DIR = args.base_dir
    port = args.out_port
    address = args.out_address
    logging.basicConfig(level=logging.INFO)
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


#BASE_DIR = "./data"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process diagram and open in browser.')
    parser.add_argument('-p', type=int, dest="out_port", metavar="port", 
                        help='listen port, default=8080', default=8080)
    parser.add_argument('-a', type=str, dest="out_address", metavar="address", 
                        help='listen address, default="127.0.0.1"', default="127.0.0.1")
    parser.add_argument('-d', type=str, dest="base_dir", metavar="datadir", 
                        help='directory to start from, default="./data"', default="./data")

    run(parser.parse_args())

