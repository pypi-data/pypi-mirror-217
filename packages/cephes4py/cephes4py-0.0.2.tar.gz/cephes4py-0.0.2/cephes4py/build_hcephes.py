import os
import platform
from os.path import join
from cffi import FFI
import struct
from os.path import exists, join
from sysconfig import get_config_var

def bits_arch():
    """Determines the number of bits of the Python process.

        Return ``32`` or ``64``.
    """
    return struct.calcsize("P") * 8


class System(object):
    def __init__(self):
        self._library_dirs = []
        self._include_dirs = []

    def add_library_dir(self, d):
        self._library_dirs.append(d)

    def add_include_dir(self, d):
        self._include_dirs.append(d)


class Windows(System):
    def get_programfiles(self):
        if bits_arch() == 32:
            return self.get_32bits_programfiles()
        return self.get_64bits_programfiles()

    def get_64bits_programfiles(self):
        n = "PROGRAMW6432"
        if n not in os.environ:
            raise RuntimeError("{} variable is not defined.".format(n))

        f = os.environ[n]
        if not exists(f):
            raise RuntimeError("Could not find {}.".format(f))

        return f

    def get_32bits_programfiles(self):
        n = "PROGRAMFILES"
        if n not in os.environ:
            raise RuntimeError("{} variable is not defined.".format(n))

        f = os.environ[n]
        if not exists(f):
            raise RuntimeError("Could not find {}.".format(f))

        return f

    def get_include_dirs(self):
        dirs = [join(get_config_var("prefix"), "include")]

        names = ["INCLUDE", "LIBRARY_INC"]
        vals = [os.environ[n] for n in names if n in os.environ]
        dirs += [d for v in vals for d in v.split(";")]

        dirs = [d for d in dirs if len(d) > 0 and exists(d)]
        return self._include_dirs + dirs

    def get_library_dirs(self):
        dirs = [join(get_config_var("prefix"), "lib")]

        names = ["LIBRARY_LIB"]
        vals = [os.environ[n] for n in names if n in os.environ]
        dirs += [d for v in vals for d in v.split(";")]

        dirs = [d for d in dirs if len(d) > 0 and exists(d)]
        return self._library_dirs + dirs

    def find_libname(self, name):
        """Try to infer the correct library name."""
        names = ["{}.lib", "lib{}.lib", "{}lib.lib"]
        names = [n.format(name) for n in names]
        dirs = self.get_library_dirs()
        for d in dirs:
            for n in names:
                if exists(join(d, n)):
                    return n[:-4]
        msg = "Could not find the {} library.".format(name)
        raise ValueError(msg)

    def __str__(self):
        msg = "Arch: {}bits\n".format(bits_arch())
        if bits_arch() == 32:
            msg += "ProgramFiles: {}\n".format(self.get_32bits_programfiles())
        if bits_arch() == 64:
            msg += "ProgramFiles32: {}\n".format(self.get_32bits_programfiles())
            msg += "ProgramFiles64: {}\n".format(self.get_64bits_programfiles())
        msg += "Include dirs: {}\n".format(self.get_include_dirs())
        msg += "Library dirs: {}\n".format(self.get_library_dirs())
        return msg


class Unix(System):
    def get_include_dirs(self):
        dirs = [join(get_config_var("prefix"), "include")]
        dirs += ["/usr/include", "/usr/local/include"]
        dirs = [d for d in dirs if len(d) > 0 and exists(d)]
        return self._include_dirs + dirs

    def get_library_dirs(self):
        dirs = [join(get_config_var("prefix"), "lib")]
        dirs += ["/usr/lib", "/usr/local/lib"]
        dirs = [d for d in dirs if len(d) > 0 and exists(d)]
        return self._library_dirs + dirs

    def __str__(self):
        msg = "Arch: {}bits\n".format(bits_arch())
        msg += "Include dirs: {}\n".format(self.get_include_dirs())
        msg += "Library dirs: {}\n".format(self.get_library_dirs())
        return msg
    

ffibuilder = FFI()
libs = ["hcephes"]

folder = os.path.dirname(os.path.abspath(__file__))
with open(join(folder, "interface.h"), "r") as f:
    ffibuilder.cdef(f.read())

if platform.system() == "Windows":
    s = Windows()
    f = s.get_programfiles()
    for lib in libs:
        s.add_library_dir(join(f, lib, "lib"))
        s.add_include_dir(join(f, lib, "include"))

    libs = [s.find_libname(lib) for lib in libs]
else:
    s = Unix()

library_dirs = s.get_library_dirs()
extra_link_args = []
if platform.system() == "Darwin":
    if len(library_dirs) > 0:
        extra_link_args += ["-Wl,-rpath," + ",-rpath,".join(library_dirs)]


ffibuilder.set_source(
    "_cephes4py",
    '#include "hcephes.h"',
    libraries=libs,
    library_dirs=library_dirs,
    include_dirs=s.get_include_dirs(),
    extra_link_args=extra_link_args,
    language="c",
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)