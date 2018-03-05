# pylint: disable=redefined-builtin
import platform
import sys

if platform.python_version().startswith("2."):
    _ACCEPTABLE_TYPES = [int, long]  # noqa: F821
else:
    _ACCEPTABLE_TYPES = [int]


class AbstractSized(object):
    """ Base class for slice and ID checking against size.
    """

    __slots__ = [
        "_size"]

    def __init__(self, size):
        """ Constructor for a ranged list.

        :param size: Fixed length of the list
        """
        self._size = max((int(round(size)), 0))

    def __len__(self):
        """ Size of the list, irrespective of actual values

        :return: the initial and Fixed size of the list
        """
        return self._size

    @staticmethod
    def _is_id_type(id):  # @ReservedAssignment
        """ Check if the given ID has a type acceptable for IDs. """
        return isinstance(id, _ACCEPTABLE_TYPES)

    def _check_id_in_range(self, id):  # @ReservedAssignment
        if id < 0:
            if self._is_id_type(id):
                raise IndexError(
                    "The index {} is out of range.".format(id))
            raise TypeError("Invalid argument type {}.".format(type(id)))
        if id >= self._size:
            if self._is_id_type(id):
                raise IndexError(
                    "The index {0!d} is out of range.".format(id))
            raise TypeError("Invalid argument type {}.".format(type(id)))

    def _check_slice_in_range(self, slice_start, slice_stop):
        if slice_start is None:
            slice_start = 0
        elif slice_start < 0:
            slice_start = self._size + slice_start
            if slice_start < 0:
                if self._is_id_type(slice_start):
                    raise IndexError(
                        "The range_start {} is out of range.".format(
                            slice_start))
                raise TypeError("Invalid argument type {}.".format(
                    type(slice_start)))
        if slice_stop is None or slice_stop == sys.maxsize:
            slice_stop = self._size
        elif slice_stop < 0:
            slice_stop = self._size + slice_stop
        if slice_start > slice_stop:
            if not self._is_id_type(slice_start):
                raise TypeError("Invalid argument type {}.".format(
                    type(slice_start)))
            if not self._is_id_type(slice_stop):
                raise TypeError("Invalid argument type {}.".format(
                    type(slice_start)))
            raise IndexError(
                "The range_start {} is after the range stop {}.".format(
                    slice_start, slice_stop))
        if slice_stop > len(self):
            if self._is_id_type(slice_stop):
                raise IndexError("The range_stop {} is out of range.".format(
                    slice_stop))
            raise TypeError("Invalid argument type {}.".format(
                type(slice_stop)))
        return slice_start, slice_stop
