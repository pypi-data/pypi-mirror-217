from .space_packet import SpacePacket


class SpacePacketProtocolEntity:
    def __init__(self, apid=None, transport=None):
        self.apid = apid
        self.transport = transport
        self.transport.indication = self._pdu_received

    def request(self, space_packet):
        if self.transport:
            self.transport.request(space_packet.encode())

    def indication(self, space_packet):
        # to be overwritten by higher layer user
        pass

    def _pdu_received(self, pdu):
        space_packet = SpacePacket.decode(pdu)
        self.indication(space_packet)
