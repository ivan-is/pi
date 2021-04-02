import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import logging

import requests

RPI_MONITOR_ROUTE = os.environ['RPI_MONITOR_ROUTE']
KERNEL_RELEASE = os.environ['KERNEL_RELEASE']

logging.basicConfig(level='DEBUG',
                    format='%(asctime)s: [%(name)s] %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger('urllib3').setLevel(logging.ERROR)

logger = logging.getLogger('pistats')


class MonitorServer(BaseHTTPRequestHandler):

    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    @staticmethod
    def get_current_status() -> dict:
        return requests.get(RPI_MONITOR_ROUTE).json()

    def get_from_rpi_monitor(self):
        state = self.get_current_status()
        return json.dumps({
            "soc_temperature": float(state['soc_temp']),
            "uptime": float(state['uptime']),
            "load_average": [float(state['load1']), float(state['load5']), float(state['load15'])],
            "kernel_release": KERNEL_RELEASE,  # TODO: get automatically
            "memory": {
                "total_memory": int(state['memory_free']) + int(state['memory_available']),
                "free_memory": int(state['memory_free']),
                "available_memory": int(state['memory_available'])
            }
        })

    def do_GET(self):
        self.set_response()
        logger.info(self.path)
        if self.path == "/monitor.json" or self.path == "/monitor":
            response = self.get_from_rpi_monitor()
            self.wfile.write(response.encode())


if __name__ == '__main__':
    port = int(sys.argv[-1])
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, MonitorServer)
    httpd.serve_forever()
