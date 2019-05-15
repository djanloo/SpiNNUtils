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

from .file_converter import FileConverter
import os
import sys

if 'SPINN_DIRS' in os.environ:
    RANGE_DIR = os.path.join(os.environ['SPINN_DIRS'], "lib")
else:
    RANGE_DIR = "lib"

DICTIONARY_HEADER = "Id,Preface,Original\n" \
                    ",DO NOT EDIT,THIS FILE WAS AUTOGENERATED BY MAKE\n"
RANGE_PER_DIR = 1000
SKIPABLE_FILES = ["common.mk", "Makefile.common",
                  "paths.mk", "Makefile.paths",
                  "neural_build.mk", "Makefile.neural_build"]
LOG_RANGE_FILENAME = "log.ranges"
LOG_FILE_HEADER = "AUTOGENERATED DO NOT EDIT\n"


class Converter(object):
    __slots__ = [
        # Full destination directory
        "_dest",
        # Part of destination directory to replace in when converting paths
        "_dest_basename",
        # File to hold dictionary mappings
        "_dict",
        # Full source directory
        "_src",
        # Part of source directory to take out when converting paths
        "_src_basename"]

    def __init__(self, src, dest, dict_file):
        """ Converts a whole directory including sub directories

        :param src: Full source directory
        :type src: str
        :param dest: Full destination directory
        :type dest: str
        :param dict_file: Full path to dictionary file
        :type dict_file: str
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
        self._dict = os.path.abspath(dict_file)

    def run(self):
        """ Runs the file converter on a whole directory including sub \
            directories

        WARNING. This code is absolutely not thread safe.
        Interwoven calls even on different FileConverter objects is dangerous!
        It is highly likely that dict files become corrupted and the same
        message_id is used multiple times.

        :return:
        """
        self._mkdir(self._dest)
        with open(self._dict, 'w') as dict_f:
            dict_f.write(DICTIONARY_HEADER)
        message_id = self._get_id()
        for dir_name, _subdir_list, file_list in os.walk(self._src):
            self._mkdir(dir_name)
            for file_name in file_list:
                _, extension = os.path.splitext(file_name)
                source = os.path.join(dir_name, file_name)
                if extension in [".c", ".cpp", ".h"]:
                    destination = self._any_destination(source)
                    message_id = FileConverter.convert(
                        source, destination, self._dict, message_id)
                elif file_name in SKIPABLE_FILES:
                    pass
                else:
                    print("Unexpected file {}".format(source))

    def _get_id(self):

        rangefile = os.path.join(RANGE_DIR, LOG_RANGE_FILENAME)
        range_start = 0
        filename = self._dest
        common_dir = self._find_common_based_on_environ()
        if filename.startswith(common_dir):
            filename = filename[len(common_dir)+1:]

        # If the range_file does not exist create it and use range_start
        if not os.path.exists(rangefile):
            with open(rangefile, 'w') as log_ranges_file:
                log_ranges_file.write(LOG_FILE_HEADER)
                log_ranges_file.write("{} {}\n".format(
                    range_start, filename))
            return range_start

        # Check if the file is ranged or find highest range so far
        highest_found = range_start
        with open(rangefile, 'r') as log_ranges_file:
            data_lines = iter(log_ranges_file)
            next(data_lines)  # Ignore do not edit
            for line in data_lines:
                parts = line.split(" ", 1)
                if filename.strip() == parts[1].strip():
                    return int(parts[0])
                else:
                    highest_found = max(highest_found, int(parts[0]))

        # Go one step above best found
        new_start = highest_found + RANGE_PER_DIR

        # Append to range file in case rebuilt without clean
        with open(rangefile, 'a') as log_ranges_file:
            log_ranges_file.write("{} {}\n".format(new_start, filename))
        return new_start

    def _any_destination(self, path):
        # Here we need the local separator
        src_bit = os.path.sep + self._src_basename + os.path.sep
        dest_bit = os.path.sep + self._dest_basename + os.path.sep
        li = path.rsplit(src_bit, 1)
        return dest_bit.join(li)

    def _mkdir(self, path):
        destination = self._any_destination(path)
        if not os.path.exists(destination):
            os.mkdir(destination)
        if not os.path.exists(destination):
            raise Exception("mkdir failed {}".format(destination))

    def _find_common_based_on_environ(self):
        if 'SPINN_DIRS' not in os.environ:
            return ""
        if 'NEURAL_MODELLING_DIRS' not in os.environ:
            return ""
        return os.path.dirname(os.path.commonprefix(
            [os.environ['SPINN_DIRS'], os.environ['NEURAL_MODELLING_DIRS']]))

    @staticmethod
    def convert(src, dest, dict_file):
        converter = Converter(src, dest, dict_file)
        converter.run()


if __name__ == '__main__':
    src = sys.argv[1]
    dest = sys.argv[2]
    dict_file = sys.argv[3]
    Converter.convert(src, dest, dict_file)
