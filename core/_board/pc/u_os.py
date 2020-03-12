import os
import gc
from random import randint

def dir_path(name):
    return name
    # i_name = i.name[:-1] #upy
    # i_name = i.name  # pc

def rmtree(top):
    for path, dirs, files in os.walk(top, False):
        for f in files:
            os.unlink(path + "/" + f)
        os.rmdir(path)


def copyfileobj(src, dest, length=512):
    if hasattr(src, "readinto"):
        buf = bytearray(length)
        while True:
            sz = src.readinto(buf)
            if not sz:
                break
            if sz == length:
                dest.write(buf)
            else:
                b = memoryview(buf)[:sz]
                dest.write(b)
    else:
        while True:
            buf = src.read(length)
            if not buf:
                break
            dest.write(buf)


def byte_compare(a,b):

    if (len(a) != len(b)):
        return False

    for i in range(0, len(a)):
        if (a[i] != b[i]):
            return False

    return True


def isfile(file):
    try:
        if os.stat(file)[6]: #size more 0
            return True
        else:
            return False
    except OSError as e:
        # log.debug("LSFILE: {}".format(e))
        return False


def list_dir(path):
    try:
        return os.listdir(path)
    except OSError as e:
        # log.debug("LSDIR: {}".format(e))
        return []



def deep_delete_folder(path):
    try:
        rmtree(path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        pass


def copy_file_obj(src, dest, length=512):

    try:
        copyfileobj(src, dest, length)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        pass

def uname():
    # (sysname ='esp32',
    #  nodename='esp32',
    #  release='1.12.0',
    #  version='v1.12-188-gd3b2c6e44-dirty on 2020-02-29',
    #  machine='ANY with ESP32')
    return ('pcdev', 'pcdev', 'x.xx.x', 'vx.xx-xxx-xxxxx-dirty on YYYY-MM-DD', 'ANY with PCDEV')


def mem_info():
    gc.collect()
    return [randint(20000, 112000), randint(20000, 112000)]
