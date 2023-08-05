"""\
Copyright (c) 2023, Flagstaff Solutions, LLC
All rights reserved.

"""
import sys

import plotly.graph_objects as go
from gofigr.backends import GoFigrBackend


class PlotlyBackend(GoFigrBackend):
    """Plotly backend for GoFigr"""
    def is_compatible(self, fig):
        return isinstance(fig, go.Figure)

    def is_interactive(self, fig):
        return True

    def find_figures(self, shell):
        for _, obj in shell.user_ns.items():
            if self.is_compatible(obj):
                yield obj

    # pylint: disable=useless-return
    def get_default_figure(self, silent=False):
        if not silent:
            print("Plotly does not have a default figure. Please specify a figure to publish.", file=sys.stderr)

        return None

    def get_title(self, fig):
        title_text = None
        try:
            title = fig.layout.title
            if isinstance(title, go.layout.Title):
                title_text = title.text
            elif isinstance(title, str):
                title_text = title
        except Exception:  # pylint: disable=broad-exception-caught
            title_text = None

        return title_text

    def figure_to_bytes(self, fig, fmt, params):
        return fig.to_image(format=fmt, **params)

    def figure_to_html(self, fig):
        return fig.to_html(include_plotlyjs='cdn')

    def close(self, fig):
        pass
