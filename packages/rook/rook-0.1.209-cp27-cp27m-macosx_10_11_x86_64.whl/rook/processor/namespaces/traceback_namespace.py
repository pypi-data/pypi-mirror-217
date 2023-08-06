import inspect
import os

from .namespace import Namespace
from .python_object_namespace import PythonObjectNamespace


class TracebackNamespace(Namespace):
    def __init__(self, frame, depth):
        super(TracebackNamespace, self).__init__()
        self._frame = frame
        self._depth = depth

    def __getitem__(self, key):
        return self.read_key(key)

    def call_method(self, name, args):
        if name == "size":
            return PythonObjectNamespace(self._depth)
        else:
            return super(TracebackNamespace, self).call_method(name, args)

    def read_key(self, key):
        pos = int(key)

        current_frame = self._frame

        for i in range(pos):
            current_frame = current_frame.f_back()

        return current_frame

    def dump(self, traceback_frames_holder, get_string_index_in_cache=None, increase_pending_size=lambda _size: None):
        """
        Dump traceback frames to given 'traceback_frames_holder'.
        It's the caller responsibility to set the variant type.
        """
        current_frame = self._frame.frame
        lineno = self._frame._lineno

        if get_string_index_in_cache is not None:
            unavailable = get_string_index_in_cache("unavailable")

        for i in range(self._depth):
            frame = traceback_frames_holder.add()

            code = current_frame.f_code
            filename = code.co_filename
            if filename.endswith('.pyc'):
                filename = os.path.splitext(filename)[0] + 'py'
            function = code.co_name

            frame.lineno = lineno if lineno is not None else 0
            if get_string_index_in_cache is None:
                frame.filename = filename if filename is not None else "unavailable"
                frame.name = function if function is not None else "unavailable"
                module = inspect.getmodule(current_frame)
                frame.module = module.__name__ if module is not None else "unavailable"
            else:
                frame.filename_index_in_cache = get_string_index_in_cache(filename) if filename is not None else unavailable
                frame.name_index_in_cache = get_string_index_in_cache(function) if function is not None else unavailable
                frame.module_index_in_cache = unavailable
                increase_pending_size(11)

            current_frame = current_frame.f_back
            if not current_frame:
                break

            lineno = inspect.getlineno(current_frame)
