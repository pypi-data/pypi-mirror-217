# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from pytermor import format_auto_float

from ._base import RadioMenuItemConfig, _BaseIndicator, _BoolState, CheckMenuItemConfig
from es7s.shared import SocketMessage, get_merged_uconfig
from es7s.shared.dto import MemoryInfo
import pytermor as pt


class IndicatorMemory(_BaseIndicator[MemoryInfo]):
    def __init__(self):
        self.config_section = "indicator.memory"

        self._show_virt_bytes_none = _BoolState(
            config_var=(self.config_section, "label-virtual-bytes"),
            config_var_value="off",
        )
        self._show_virt_bytes_dynamic = _BoolState(
            config_var=(self.config_section, "label-virtual-bytes"),
            config_var_value="dynamic",
        )
        self._show_virt_bytes_short = _BoolState(
            config_var=(self.config_section, "label-virtual-bytes"),
            config_var_value="short",
        )

        self._show_virt_perc = _BoolState(
            config_var=(self.config_section, "label-virtual-percents")
        )
        self._show_swap_perc = _BoolState(config_var=(self.config_section, "label-swap-percents"))
        self._show_swap_bytes = _BoolState(config_var=(self.config_section, "label-swap-bytes"))
        self._virt_warn_threshold: float = get_merged_uconfig().getfloat(
            self.config_section, "virtual-warn-threshold"
        )
        self._swap_warn_threshold: float = get_merged_uconfig().getfloat(
            self.config_section, "swap-warn-threshold"
        )

        super().__init__(
            "memory",
            icon_subpath="memory",
            icon_name_default="0.svg",
            icon_path_dynamic_tpl="%d.svg",
            icon_thresholds=[
                95,
                *range(90, 0, -10),
            ],
            title="RAM usage",
        )

    def _init_state(self):
        super()._init_state()
        self._state_map.update(
            {
                CheckMenuItemConfig(
                    "Show virtual (%)", separator_before=True
                ): self._show_virt_perc,
                RadioMenuItemConfig(
                    "No virtual abs. value", separator_before=True, group=self.name
                ): self._show_virt_bytes_none,
                RadioMenuItemConfig(
                    "Show virtual (kB/MB/GB)", group=self.name
                ): self._show_virt_bytes_dynamic,
                RadioMenuItemConfig(
                    "Show virtual (GB)", group=self.name
                ): self._show_virt_bytes_short,
                CheckMenuItemConfig("Show swap (%)", separator_before=True): self._show_swap_perc,
                CheckMenuItemConfig("Show swap (kB/MB/GB)"): self._show_swap_bytes,
            }
        )

    def _render(self, msg: SocketMessage[MemoryInfo]):
        virtual_ratio = msg.data.virtual_used / msg.data.virtual_total

        warning_virt = virtual_ratio > self._virt_warn_threshold
        warning_swap = msg.data.swap_used / msg.data.swap_total > self._swap_warn_threshold

        if warning_virt:
            self._enqueue_notification(f"High memory usage ({virtual_ratio*100:.0f}%)")

        self._render_result(
            self._format_result(
                msg.data.virtual_used,
                msg.data.virtual_total,
                msg.data.swap_used,
                msg.data.swap_total,
            ),
            self._format_result(1e10, 1e10, 1e10, 1e10),
            warning_virt or warning_swap,
            self._select_icon(100 * virtual_ratio),
        )

    def _format_result(
        self, virt_used: float, virt_total: float, swap_used: float, swap_total: float
    ) -> str:
        parts = []
        if self._show_virt_perc:
            parts += [self._format_used_perc(virt_used, virt_total)]
        if self._show_virt_bytes_dynamic or self._show_virt_bytes_short:
            parts += [
                "".join(
                    self._format_used_bytes(
                        round(virt_used), short=self._show_virt_bytes_short.value
                    )
                )
            ]
        if self._show_swap_perc:
            parts += [self._format_used_perc(swap_used, swap_total)]
        if self._show_swap_bytes:
            parts += ["".join(self._format_used_bytes(round(swap_used)))]
        return " ".join(parts).rstrip()

    def _format_used_perc(self, used: float, total: float) -> str:
        return f"{100 * used / total:3.0f}% "

    def _format_used_bytes(self, used: int, short: bool = False) -> tuple[str, str]:
        used_kb = used / 1024
        used_mb = used / 1024**2
        used_gb = used / 1024**3
        if short:
            return pt.format_auto_float(used_gb, 3), "G"

        if used_kb < 1:
            return "< 1k", ""
        if used_kb < 1000:
            return format_auto_float(used_kb, 4, False), "k"
        if used_mb < 10000:
            return format_auto_float(used_mb, 4, False), "M"
        return format_auto_float(used_gb, 4, False), "G"
