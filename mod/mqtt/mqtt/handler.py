
try:
    import ustruct as struct
except Exception:
    import struct
    pass

import logging
log = logging.getLogger("MQTT")
log.setLevel(logging.INFO)

class MQTTHandler:

    def __init__(self, connect, client):
        self.connect = connect
        self.client = client

    async def handler(self, m_type, m_raw):

        log.debug('[m_type] : {}'.format(m_type))

        #CONNACK 0x20:  # dec 32
        if m_type == 0x20:
            code = 1
            self.connect.broker_status = 0

            try:
                (flags, code) = struct.unpack("!BB", m_raw)
                log.debug('[CONNACK] flags: %s, code: %s', hex(flags), hex(code))
            except Exception as e:
                log.debug('[CONNACK] : {}'.format(e))
                pass

            # if return code not 0, something wrong, else #subscipe to topic
            if not code:
                log.info('Connected')
                self.connect.open_status = 1
                self.connect.broker_status = 1
                self.client.fail = 0
                await self.client.sbt_subscribe()
            else:
                log.info('Disconnected')
                await self.client.close()


        #SUBACK 0x90 # dec 144
        elif m_type == 0x90:

            pack_format = "!H" + str(len(m_raw) - 2) + 's'
            (mid, packet) = struct.unpack(pack_format, m_raw)
            pack_format = "!" + "B" * len(packet)
            get_qos = struct.unpack(pack_format, packet)

            log.debug('[SUBACK] mid: {} q: {}'.format(mid, get_qos))
            if get_qos[0] == 0:  # 0x00 - Success - Maximum QoS 0 , 0x80 - Failure
                log.info('[SUBACK] mid: {}'.format(mid))
                self.connect._ping = 0

        #PUBLISH 0x30, 0x31 # _handle_publish_packet , retain and not retain
        elif m_type in [0x30, 0x31]:

            retain = m_type & 0x01

            #format
            try:
                pack_format = "!H" + str(len(m_raw) - 2) + 's'
                (slen, packet) = struct.unpack(pack_format, m_raw)
                pack_format = '!' + str(slen) + 's' + str(len(packet) - slen) + 's'
            except Exception as exc:
                log.warning('[ERR pack format] {}'.format(exc))
                return
            #message
            try:
                (topic, packet) = struct.unpack(pack_format, packet)
            except Exception as exc:
                log.warning('[ERR unpack] {}'.format(exc))
                return

            #topic
            if not topic:
                log.warning('[ERR PROTO] topic name is empty')
                return

            try:
                print_topic = topic.decode('utf-8')
            except UnicodeDecodeError as exc:
                log.warning('[INVALID CHARACTER IN TOPIC] {} - {}'.format(topic, exc))
                print_topic = topic

            if self.client.cb:
                self.client.cb(print_topic, packet, retain)

        #PINGRESP 0xD0 # dec 208
        elif m_type == 0xD0:
            log.debug('[PING PINGRESP]')
            self.client.fail = 0
