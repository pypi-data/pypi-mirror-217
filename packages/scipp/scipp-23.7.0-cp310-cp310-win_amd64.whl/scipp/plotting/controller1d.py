# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)
# @author Neil Vaytet

import numpy as np

from ..units import one
from .controller import PlotController


class PlotController1d(PlotController):
    """
    Controller class for 1d plots.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_line_color(self, line_id=None, color=None):
        """
        Get a message from the panel to change the color of a given line.
        Forward the message to the view.
        """
        self.view.update_line_color(line_id=line_id, color=color)

    def refresh(self):
        """
        Do nothing for refresh in case of 1d plot.
        """
        return

    def rescale_to_data(self, button=None):
        """
        A small delta is used to add padding around the plotted points.
        """
        with_min_padding = self.vmin is None
        with_max_padding = self.vmax is None
        vmin, vmax = self.find_vmin_vmax(button=button)
        if vmin.unit is None:
            vmin.unit = one
            vmax.unit = one
        if self.norm == "log":
            delta = 10 ** (0.05 * np.log10(vmax.value / vmin.value))
            if with_min_padding or (button is not None):
                vmin /= delta
            if with_max_padding or (button is not None):
                vmax *= delta
        else:
            delta = 0.05 * (vmax - vmin)
            if with_min_padding or (button is not None):
                vmin -= delta
            if with_max_padding or (button is not None):
                vmax += delta
        self.view.rescale_to_data(vmin, vmax)

    def toggle_norm(self, owner):
        """
        Toggle data normalization from toolbar button signal.
        """
        self.norm = "log" if owner.value else "linear"
        vmin, vmax = self.find_vmin_vmax()
        if self.norm == "log":
            self.rescale_to_data()
            self.view.toggle_norm(self.norm, vmin, vmax)
        else:
            self.view.toggle_norm(self.norm, vmin, vmax)
            self.rescale_to_data()
