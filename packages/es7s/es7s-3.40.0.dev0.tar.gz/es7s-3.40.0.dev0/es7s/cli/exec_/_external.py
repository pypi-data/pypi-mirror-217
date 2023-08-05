# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t

from .._base import CliBaseCommand
from .._base_opts_params import CMDTYPE_EXTERNAL
from .._foreign import ForeignInvoker
from ...shared.path import get_config_yaml


class ExternalCommandFactory:
    @staticmethod
    def make_all() -> t.Iterable[CliBaseCommand]:
        for name, cfg in get_config_yaml('cmd-external').get('commands').items():
            finv = ForeignInvoker(cfg.pop('target'), cfg, CMDTYPE_EXTERNAL)
            yield finv.cmd
