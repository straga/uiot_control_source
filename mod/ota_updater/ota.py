from esp32 import Partition
import esp

from machine import reset


try:
    import uasyncio as asyncio
    import uos as os
    import ubinascii as binascii
    import upip_utarfile as utar
    from core.u_os import *
    from core.platform import upy_buffer as _abuffer

except Exception:
    import asyncio as asyncio
    import os
    import binascii
    import tarfile as utar
    from core.u_os import *
    from core.platform import pc_buffer as _abuffer





import hashlib

import logging
log = logging.getLogger("OTA")
log.setLevel(logging.DEBUG)

from core.thread.thread import run_in_executer



class OtaUpdater:

    def __init__(self):

        self.CHUNK_SIZE = 512
        self.SEC_SIZE = 4096
        self.upd_type = None
        self.upd_size = 0
        self.upd_hash = None
        self.next_part = ""
        self.cur_part = ""
        self.set_part()
        self.status = 0.0

    def get_status(self):
        return self.status

    def set_part(self):
        runningpart = Partition(Partition.RUNNING)
        part_info = runningpart.info()
        part_name = part_info[4]

        if part_name == "ota_0":
            self.next_part = "factory"
        elif part_name == "factory":
            self.next_part = "ota_0"

        self.cur_part = part_name

    def set_metadata(self, request):

        if "content-length" in request._headers:
            self.upd_size = int(request._headers["content-length"])
        if "content-type" in request._headers:
            if request._headers["content-type"] == "application/octet-stream":
                self.upd_type = "partition"
            elif request._headers["content-type"] == "application/x-tar":
                self.upd_type = "vfs"
        if "sha256" in request._headers:
            self.upd_hash = request._headers["sha256"]


    async def update(self, request):

        self.set_metadata(request)

        if self.upd_type == "vfs":

            update_vfs = UpdateVFS(next_part=self.next_part, cur_part=self.cur_part)
            #make file
            update_vfs.file = update_vfs.write_file(update_vfs.TAR_PATH)
            #download file
            await self.download_chunk(request, update_vfs)
            #close file
            log.info("Vfs Close")
            update_vfs.file_close()
            log.info("Start Calc hash")
            hash_result = await run_in_executer(update_vfs.check_file_hash, update_vfs.TAR_PATH, self.upd_hash)

            if not hash_result:
                update_vfs.remove_file(update_vfs.TAR_PATH)
                log.info("Vfs update corrupt")
                return False

            else:
                log.info("Vfs update OK")

                await run_in_executer(update_vfs.delete_old_vfs)

                unpack = await run_in_executer(update_vfs.unpack_tar)
                await run_in_executer(update_vfs.remove_file, update_vfs.TAR_PATH)

                if not unpack:
                    return False

        if self.upd_type == "partition":

            update_part = UpdatePart(next_part=self.next_part, cur_part=self.cur_part)
            parts = Partition.find(label=self.next_part)

            if parts:
                part_upd = parts[0]
                update_part.set_part(part_upd)

                await self.download_chunk(request, update_part)

                check_hash = await run_in_executer(update_part.check_partition, self.upd_hash, self.upd_size)

                if not check_hash:
                    update_part.delete_partition()
                    log.debug('Partion Delete')
                    return False

                Partition.set_boot(part_upd)
                reset()

            else:
                return False

        return True



    async def download_chunk(self, request, updater):

        log.debug("= : POST DATA (content size): {}".format(self.upd_size))
        log.debug("= : POST DATA (update type): {}".format(self.upd_type))

        pieces = int(self.upd_size / self.CHUNK_SIZE) + (self.upd_size % self.CHUNK_SIZE > 0)
        log.debug("= : POST DATA (pieces): {}".format(pieces))

        last_piece = (pieces - 1)
        written_size = 0

        for i in range(0, pieces):

            try:
                if i < last_piece:
                    buf = await request.reader.readexactly(self.CHUNK_SIZE)
                else:
                    buf = await request.reader.read(self.CHUNK_SIZE)
            except Exception as e:
                log.error("Download: {}".format(e))
                break

            if buf:
                if self.upd_type == "vfs":
                    written_size += updater.write_file_chunk(buf, updater.file)

                if self.upd_type == "partition":
                    written_size += updater.write_partition_chunk(buf, i)

                self.status = i / last_piece
                log.info("<- {:.2%}".format(self.status))
                if len(buf) < self.CHUNK_SIZE and i < last_piece:
                    log.info("{} <- c_sz: {}, w_sz: {}".format(i, len(buf), written_size))
                    log.debug(buf)

        log.info("Pieces: {}".format(pieces))
        log.info("Update size: {}".format(self.upd_size))
        log.info("Written size = {}".format(written_size))



class UpdateVFS:
    def __init__(self, next_part, cur_part, chunk_size=512):
        self.CHUNK_SIZE = chunk_size
        self.next_boot_part = next_part
        self.cur_boot_part = cur_part
        self.TAR_PATH = "/update.tar"
        self.file = False

    def remove_file(self, path):
        try:
            os.remove(path)
        except Exception as e:
            log.error("File not exist: {}".format(e))
            pass

    def write_file(self, path):
        self.remove_file(path)
        f = open(path, "ab")
        return f



    def file_close(self):
        try:
            self.file.close()
        except Exception as e:
            log.error("File not exist: {}".format(e))
            pass


    def write_file_chunk(self, buf, file):
        file.write(buf)
        file.flush()
        return len(buf)

    def check_file_hash(self, path, hash):
        h256 = hashlib.sha256()
        with open(path, 'rb') as f:
            while True:
                buf = f.read(self.CHUNK_SIZE)
                if not buf:
                    break
                h256.update(buf)
        filehash = (binascii.hexlify(h256.digest()).decode())
        log.info('{} hash is "{}", should be "{}"'.format(path, filehash, hash))
        return filehash == hash


    def delete_old_vfs(self):
        deep_delete_folder("/{}".format(self.next_boot_part))
        os.mkdir("/{}".format(self.next_boot_part))

    def unpack_tar(self):

        t = utar.TarFile(self.TAR_PATH)
        updatebasepath = "/{}/".format(self.next_boot_part)
        log.info("Update Base Path: {}".format(updatebasepath))
        for i in t:
            # log.info("info {}".format(i))
            # gc.collect()

            if i.type == utar.DIRTYPE:
                i_name = dir_path(i.name)
                #i_name = i.name[:-1] #upy
                #i_name = i.name # pc
                log.debug("{} -> {}".format(i.name, i_name))
                try:
                    os.mkdir(updatebasepath + i_name)
                except Exception as e:
                    log.debug("mkdir: er:{}, path:{}".format(e, updatebasepath + i_name))
                    return False
            else:
                # log.info("file: {}".format(updatebasepath+i.name))
                with open(updatebasepath+i.name, 'wb') as ef:
                    pf = t.extractfile(i)
                    copy_file_obj(pf, ef)

        return True


class UpdatePart:
    def __init__(self, next_part, cur_part, chunk_size=512, sec_size=4096):
        self.CHUNK_SIZE = chunk_size
        self.SEC_SIZE = sec_size
        self.next_boot_part = next_part
        self.cur_boot_part = cur_part
        self.part = None
        self.chunkspersec = self.SEC_SIZE // self.CHUNK_SIZE


    def set_part(self, part):
        self.part = part
        self.part_start = part.info()[2]
        self.part_size = part.info()[3]
        self.part_base_sec = self.part_start // 4096

    # def copy_partition(self):
    #     buf = bytearray(self.CHUNK_SIZE)
    #     for i in range(0, self.partitions[self.cur_boot_partition][3]/self.CHUNK_SIZE):
    #         esp.flash_read(self.partitions[self.cur_boot_partition][2]+self.CHUNK_SIZE*i, buf)
    #         self.write_partition_chunk(buf, i)


    def delete_partition(self):
        buf = bytearray(self.CHUNK_SIZE)
        for i in range(0, int(self.part_size/self.CHUNK_SIZE)):
            self.write_partition_chunk(buf, i)


    def write_partition_chunk(self, buffer, next_id):
        if next_id % self.chunkspersec == 0:
            esp.flash_erase(self.part_base_sec + next_id // self.chunkspersec)
        esp.flash_write(self.part_start + self.CHUNK_SIZE * next_id, buffer)

        return len(buffer)

    def check_partition(self, updatehash, updatesize):
        h = hashlib.sha256()

        buf_sz = int((updatesize / self.CHUNK_SIZE - updatesize // self.CHUNK_SIZE) * self.CHUNK_SIZE)
        log.debug('First buf_sz {}'.format(buf_sz))
        if buf_sz == 0:
            buf = bytearray(self.CHUNK_SIZE)
        else:
            buf = bytearray(buf_sz)

        position = self.part_start
        pieces = int(updatesize / self.CHUNK_SIZE) + (updatesize % self.CHUNK_SIZE > 0)
        for i in range(0, pieces):

            # log.debug('id {}, P:  {}'.format(i, position))
            esp.flash_read(position, buf)
            # log.debug('{}'.format(buf))

            h.update(buf)
            position += len(buf)

            buf = _abuffer(512)

            if not buf:
                break

        parthash = (binascii.hexlify(h.digest()).decode())

        log.info('partition hash is "{}", should be "{}"'.format(parthash, updatehash))
        return parthash == updatehash
