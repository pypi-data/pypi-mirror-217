from importlib.metadata import version

from .ddicts import format_ddict, nested_ddict
from .plot import bar_count, cumulative_bins, log_bins
from .save import save

__all__ = [
    "save",
    "nested_ddict",
    "format_ddict",
    "cumulative_bins",
    "log_bins",
    "bar_count",
]
__version__ = version("my-favorite-things")
