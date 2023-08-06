SPP_VERSION = 0b000


class SpacePacket:
    def __init__(
        self,
        # packet primary header
        packet_type,
        packet_sec_hdr_flag,
        apid,
        sequence_flags,
        packet_sequence_count,
        packet_version=SPP_VERSION,
        # packet data field
        packet_data_field=None,
    ):
        self.packet_type = packet_type
        self.packet_sec_hdr_flag = packet_sec_hdr_flag
        self.apid = apid
        self.sequence_flags = sequence_flags
        self.packet_sequence_count = packet_sequence_count
        self.packet_version = packet_version
        self.packet_data_field = packet_data_field

    def encode(self):
        self.packet_data_length = len(self.packet_data_field) - 1

        databytes = bytes(
            [
                (self.packet_version << 5) +
                # packet identification
                (self.packet_type << 4)
                + (self.packet_sec_hdr_flag << 3)
                + (self.apid >> 8),
                (self.apid & 0xFF),
                # packet sequence control
                (self.sequence_flags << 6) + (self.packet_sequence_count >> 8),
                (self.packet_sequence_count & 0xFF),
                # packet data length
                (self.packet_data_length >> 8),
                (self.packet_data_length & 0xFF),
            ]
        )

        databytes += self.packet_data_field
        return databytes

    @classmethod
    def decode(cls, pdu):
        packet_type = (pdu[0] >> 4) & 0x01
        packet_sec_hdr_flag = (pdu[0] >> 3) & 0x01
        apid = ((pdu[0] & 0x07) << 8) + pdu[1]
        sequence_flags = pdu[2] >> 6
        packet_sequence_count = ((pdu[2] & 0x3F) << 8) + pdu[3]
        packet_version = pdu[0] >> 5
        packet_data_length = (pdu[4] << 8) + pdu[5] + 1
        packet_data_field = pdu[6:]

        if packet_data_length != len(packet_data_field):
            raise ValueError("Packet data length mismatch")

        return cls(
            packet_type,
            packet_sec_hdr_flag,
            apid,
            sequence_flags,
            packet_sequence_count,
            packet_version,
            packet_data_field,
        )
