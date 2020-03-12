import os
import gc

def dir_path(name):
    return name[:-1]
    # i_name = i.name[:-1] #upy
    # i_name = i.name  # pc

def byte_compare(a,b):


    if (len(a) != len(b)):
        return False

    for i in range(0, len(a)):
        if (a[i] != b[i]):
            return False
    return True


def copy_file_obj(src, dest, length=512):
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


def copy_file(src, dest, length=512):
    with open(src, "rb") as fsrc:
        with open(dest, "wb") as fdest:
            while True:
                buf = fsrc.read(length)
                if not buf:
                    return
                fdest.write(buf)

def deep_copy_folder(src, dest):
    for f in os.ilistdir(src):
        psrc = "{}/{}".format(src, f[0])
        pdest = "{}/{}".format(dest, f[0])
        if f[1] == 0x4000:
            try:
                os.mkdir(pdest)
            except:
                pass
            deep_copy_folder(psrc, pdest)
        else:
            copy_file(psrc, pdest)


def deep_delete_folder(path):
    try:
        os.ilistdir(path)
    except:
        return

    for f in os.ilistdir(path):
        ppath = "{}/{}".format(path, f[0])
        if f[1] == 0x4000:
            deep_delete_folder(ppath)
            try:
                os.rmdir(ppath)
            except:
                pass
        else:
            try:
                os.remove(ppath)
            except:
                pass

    try:
        os.rmdir(path)
    except:
        pass


def uname():
    return list(os.uname())

def mem_info():
    gc.collect()
    return [gc.mem_free(), gc.mem_alloc()]