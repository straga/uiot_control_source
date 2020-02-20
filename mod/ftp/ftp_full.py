
# FTP active
# async def _port(self, argument):
#     argument = argument.split(',')
#
#     self.request.active_ip = '.'.join(argument[:4])
#     self.request.active_port = (int(argument[4]) << 8) + int(argument[5])
#
#     log.info("got the port {}, {}".format(self.request.active_ip, self.request.active_port))
#
#     await self.c_awrite("200 OK.\r\n")
#     self.request.con_type = "active"
#
#
#
# async def wait_transfer(self, con_type):
#
#
#
#     if con_type is "active":
#         log.info("Active: connecting to -> %s %d" % (self.active_ip, self.active_port))
#         reader, writer = await asyncio.open_connection(self.active_ip, self.active_port)
#
#         if not self.transfer:
#             self.transfer = "Start"
#         log.debug("as0. Data Transfer {}".format(self.transfer))
#
#         while True:
#
#             if self.transfer:
#                 await self.data_transfer(reader, writer)
#             else:
#                 self.data_start = False
#                 break
#
#         log.debug("- Data Server <- client from {}".format(self.active_ip))
#         log.debug("as2. Data Server = Close")
#         await _aclose(writer)
#
#     log.debug("s3. Send Data Done")
#     return True
