# Copyright (c) 2018-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from .file_converter import FileConverter
from .log_sqllite_database import LogSqlLiteDatabase

SKIPPABLE_FILES = ["common.mk", "Makefile.common",
                   "paths.mk", "Makefile.paths",
                   "neural_build.mk", "Makefile.neural_build"]


class Converter(object):
    __slots__ = [
        # Full destination directory
        "_dest",
        # Part of destination directory to replace in when converting paths
        "_dest_basename",
        # Full source directory
        "_src",
        # Part of source directory to take out when converting paths
        "_src_basename"]

    def __init__(self, src, dest, new_dict):
        """ Converts a whole directory including sub directories

        :param str src: Full source directory
        :param str dest: Full destination directory
        :param bool new_dict: says if we should generate a new dict
        """
        self._src = os.path.abspath(src)
        if not os.path.exists(self._src):
            raise Exception(
                "Unable to locate source directory {}".format(self._src))
        self._dest = os.path.abspath(dest)
        src_root, src_basename = os.path.split(
            os.path.normpath(self._src))
        dest_root, dest_basename = os.path.split(
            os.path.normpath(self._dest))
        if src_root != dest_root:
            # They must be siblings due to text manipulation in makefiles
            raise Exception("src and destination must be siblings")
        self._src_basename = src_basename
        self._dest_basename = dest_basename
        if new_dict:
            LogSqlLiteDatabase(new_dict)

    def run(self):
        """ Runs the file converter on a whole directory including \
            sub-directories.

        .. warning::
            This code is absolutely not thread safe.
            Interwoven calls even on different FileConverter objects is
            dangerous!
        """
        self._mkdir(self._dest)
        for dir_name, _subdir_list, file_list in os.walk(self._src):
            self._mkdir(dir_name)
            for file_name in file_list:
                _, extension = os.path.splitext(file_name)
                source = os.path.join(dir_name, file_name)
                if extension in [".c", ".cpp", ".h"]:
                    destination = self._any_destination(source)
                    FileConverter.convert(source, destination)
                elif file_name in SKIPPABLE_FILES:
                    pass
                else:
                    print("Unexpected file {}".format(source))

    def _any_destination(self, path):
        # Here we need the local separator
        src_bit = os.path.sep + self._src_basename + os.path.sep
        dest_bit = os.path.sep + self._dest_basename + os.path.sep
        li = path.rsplit(src_bit, 1)
        return dest_bit.join(li)

    @staticmethod
    def _mkdir(destination):
        if not os.path.exists(destination):
            os.mkdir(destination)
        if not os.path.exists(destination):
            raise Exception("mkdir failed {}".format(destination))

    @staticmethod
    def convert(src, dest, new_dict):
        """ Wrapper function around this class.
        """
        converter = Converter(src, dest, new_dict)
        converter.run()


if __name__ == '__main__':
    _src = sys.argv[1]
    _dest = sys.argv[2]
    if len(sys.argv) > 3:
        _new_dict = bool(sys.argv[3])
    else:
        _new_dict = False
    Converter.convert(_src, _dest, _new_dict)
