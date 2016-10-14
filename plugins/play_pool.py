import logging

logger = logging.getLogger(__name__)


class Plugin(object):
    def __init__(self, bus):
        self.bus = bus
        self.bus.subscribe_map({"new_player": self.new_player},
                               thread=True)

    def new_player(self, data):
        event = {"msg": "New player: " + data.id}
        logger.info(event['msg'])
        self.bus.notify("message", event)
