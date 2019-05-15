# Copyright (c) 2017-2018 The University of Manchester
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
import spinn_utilities.package_loader as package_loader


def test_import_all():
    if os.environ.get('CONTINUOUS_INTEGRATION', 'false').lower() == 'true':
        package_loader.load_module("spinn_utilities", remove_pyc_files=False)
    else:
        package_loader.load_module("spinn_utilities", remove_pyc_files=True)


if __name__ == '__main__':
    test_import_all()
