# Copyright (c) 2020 Viktor Vorobjov

import os
from pathlib import Path
import shutil


print("Gent Tool")


class Gen:

    def __init__(self, symlink=True):
        self.symlink = symlink



    def create_lib(self, path, libs, path_ulib):

        for key, value in libs.items():

            _path = Path(path)

            target = Path("{}/{}/{}".format(path_ulib, key, value))
            link = Path("{}/{}".format(_path, value))

            # print(" ")
            # print(_path)
            # print(is_file)

            if not target.is_dir():
                dir_dst = os.path.abspath("{}".format(path))
                if not os.path.exists(dir_dst):
                    os.makedirs(dir_dst)

            if target.is_dir():
                link_dst = link.parent.exists()
                if not link_dst:
                    link.parent.mkdir()

            error = False
            try:
                if self.symlink:
                    link.symlink_to(target.resolve(), target_is_directory=target.is_dir())
                else:
                    if target.resolve().is_file():
                        shutil.copy(target.resolve(), link)
                    else:
                        shutil.copytree(target.resolve(), link)
                already = "New"
            except Exception as e:
                error = e
                already = "Error"
                pass
            finally:
                if error and link.exists():
                    already = "Exist"

            _type = "File"
            if target.is_dir():
                _type = "Dir "

            # print("{}: {} - {} :{} ".format(_type, already, link, error))
            print("{}: {} - {} ".format(_type, already, link))



    def gen_libs(self, src_lib, src_path, src, dst_lib, dst_path):

        _path = "{}/{}".format(dst_lib, dst_path)
        _lib = {src_path: src}
        _path_ulib = src_lib

        self.create_lib(path=_path, libs=_lib, path_ulib=_path_ulib)
