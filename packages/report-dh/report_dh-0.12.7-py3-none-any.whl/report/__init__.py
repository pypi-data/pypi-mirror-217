from .item import feature, story, title, step, log, attachment
from ._internal import Launch
from ._data import parse
from . import attachment_type

import atexit

parse()
# Launch.start_launch()

atexit.register(Launch.finish_launch)


__all__ = [
    'attachment_type',
    'parse'
]
