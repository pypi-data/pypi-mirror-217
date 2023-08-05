# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ._external import ExternalCommandFactory
from . import *


autodiscover_extras = ExternalCommandFactory.make_all
