#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import scale
import planet_weight

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/json')
        self.end_headers()

        weight = scale.get_latest_weight()
        results = planet_weight.get_planet_weights(weight)

        # Send message back to client
        message = json.dumps(results)
        print(message)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
