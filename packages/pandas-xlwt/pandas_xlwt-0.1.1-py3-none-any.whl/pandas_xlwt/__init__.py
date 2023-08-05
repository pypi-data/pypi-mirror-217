from typing import Literal
from pandas.io.excel._util import register_writer
from pandas_xlwt._xlwt import XlwtWriter as _XlwtWriter

register_writer(_XlwtWriter)