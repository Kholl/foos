import threading
import logging
import socket
import json

logger = logging.getLogger(__name__)

class Plugin(object):
    def __init__(self, bus):
        self.bus = bus
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        hostname = socket.gethostname()
        logger.info("Listening " + hostname + ":13337")

        self.server.bind((hostname, 13337))
        self.server.listen(1)
        threading.Thread(daemon=True, target=self.loop).start()

    def loop(self):
        while True:
            (clientsocket, address) = self.server.accept()

            recvdata = ""
            while True:
                data = clientsocket.recv()
                if data is None:
                    break

                recvdata += data

            clientsocket.close()
            self.notify(recvdata)

    def notify(self, recvdata):
        (command, params) = recvdata.split("~")
        self.bus.notify(command, json.loads(params))
