# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)
# @author Neil Vaytet

import io
from copy import copy

import numpy as np

from .. import config, units
from ..core import DataArray, DType
from ..core import abs as abs_
from ..core import concat, full_like, geomspace, scalar, values
from ..utils import running_in_jupyter


def get_line_param(name, index):
    """
    Get the default line parameter from the config.
    If an index is supplied, return the i-th item in the list.
    """
    param = config['plot'][name]
    return param[index % len(param)]


def to_bin_centers(x, dim):
    """
    Convert array edges to centers
    """
    return 0.5 * (x[dim, 1:] + x[dim, :-1])


def to_bin_edges(x, dim):
    """
    Convert array centers to edges
    """
    idim = x.dims.index(dim)
    if x.shape[idim] < 2:
        one = scalar(1.0, unit=x.unit)
        return concat([x[dim, 0:1] - one, x[dim, 0:1] + one], dim)
    else:
        center = to_bin_centers(x, dim)
        # Note: use range of 0:1 to keep dimension dim in the slice to avoid
        # switching round dimension order in concatenate step.
        left = center[dim, 0:1] - (x[dim, 1] - x[dim, 0])
        right = center[dim, -1] + (x[dim, -1] - x[dim, -2])
        return concat([left, center, right], dim)


def get_colormap(name):
    """
    Return a matplotlib colormap.
    """
    import matplotlib

    if hasattr(matplotlib, 'colormaps'):
        # This exists since matplotlib v3.5
        return matplotlib.colormaps[name]
    # This raises a PendingDeprecationWarning since matplotlib 3.6
    return matplotlib.cm.get_cmap(name)


def parse_params(params=None, defaults=None, globs=None, array=None):
    """
    Construct the colorbar settings using default and input values
    """
    from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize

    parsed = dict(config['plot']['params'])
    if defaults is not None:
        for key, val in defaults.items():
            parsed[key] = val
    if globs is not None:
        for key, val in globs.items():
            # Global parameters need special treatment because by default they
            # are set to None, and we don't want to overwrite the defaults.
            if val is not None:
                parsed[key] = val
    if params is not None:
        if isinstance(params, bool):
            params = {"show": params}
        for key, val in params.items():
            parsed[key] = val

    if parsed["norm"] == "log":
        norm = LogNorm
    elif parsed["norm"] == "linear":
        norm = Normalize
    else:
        raise RuntimeError(
            "Unknown norm. Expected 'linear' or 'log', "
            "got {}.".format(parsed["norm"])
        )
    vmin = parsed["vmin"]
    vmax = parsed["vmax"]
    parsed["norm"] = norm(
        vmin=vmin.value if vmin is not None else None,
        vmax=vmax.value if vmax is not None else None,
    )

    # Convert color into custom colormap
    if parsed["color"] is not None:
        parsed["cmap"] = LinearSegmentedColormap.from_list(
            "tmp", [parsed["color"], parsed["color"]]
        )
    else:
        parsed["cmap"] = copy(get_colormap(parsed["cmap"]))

    if parsed["under_color"] is None:
        parsed["cmap"].set_under(parsed["cmap"](0.0))
    else:
        parsed["cmap"].set_under(parsed["under_color"])
    if parsed["over_color"] is None:
        parsed["cmap"].set_over(parsed["cmap"](1.0))
    else:
        parsed["cmap"].set_over(parsed["over_color"])

    return parsed


def vars_to_err(v):
    """
    Convert variances to errors.
    """
    with np.errstate(invalid="ignore"):
        v = np.sqrt(v)
    np.nan_to_num(v, copy=False)
    return v


def find_log_limits(x):
    """
    To find log scale limits, we histogram the data between 1.0-30
    and 1.0e+30 and include only bins that are non-zero.
    """
    from .. import flatten, ones

    volume = np.product(x.shape)
    pixel = flatten(values(x.astype(DType.float64)), to='pixel')
    weights = ones(dims=['pixel'], shape=[volume], unit='counts')
    hist = DataArray(data=weights, coords={'order': pixel}).hist(
        order=geomspace('order', 1e-30, 1e30, num=61, unit=x.unit)
    )
    # Find the first and the last non-zero bins
    inds = np.nonzero((hist.data > scalar(0.0, unit=units.counts)).values)
    ar = np.arange(hist.data.shape[0])[inds]
    # Safety check in case there are no values in range 1.0e-30:1.0e+30:
    # fall back to the linear method and replace with arbitrary values if the
    # limits are negative.
    if len(ar) == 0:
        [vmin, vmax] = find_linear_limits(x)
        if vmin.value <= 0.0:
            if vmax.value <= 0.0:
                vmin = full_like(vmin, 0.1)
                vmax = full_like(vmax, 1.0)
            else:
                vmin = 1.0e-3 * vmax
    else:
        vmin = hist.coords['order']['order', ar.min()]
        vmax = hist.coords['order']['order', ar.max() + 1]
    return [vmin, vmax]


def find_linear_limits(x):
    """
    Find variable finite min and max.
    TODO: If we implement finitemin and finitemax for Variable, we would no longer need
    to go via Numpy's isfinite.
    """
    v = x.values
    finite_vals = v[np.isfinite(v)]
    finite_min = np.amin(finite_vals)
    finite_max = np.amax(finite_vals)
    return [
        scalar(finite_min, unit=x.unit, dtype='float64'),
        scalar(finite_max, unit=x.unit, dtype='float64'),
    ]


def find_limits(x, scale=None, flip=False):
    """
    Find sensible limits, depending on linear or log scale.
    """
    if scale is not None:
        if scale == "log":
            lims = {"log": find_log_limits(x)}
        else:
            lims = {"linear": find_linear_limits(x)}
    else:
        lims = {"log": find_log_limits(x), "linear": find_linear_limits(x)}
    if flip:
        for key in lims:
            lims[key] = np.flip(lims[key]).copy()
    return lims


def fix_empty_range(lims, replacement=None):
    """
    Range correction in case xmin == xmax
    """
    dx = scalar(0.0, unit=lims[0].unit)
    if lims[0].value == lims[1].value:
        if replacement is not None:
            dx = 0.5 * replacement
        elif lims[0].value == 0.0:
            dx = scalar(0.5, unit=lims[0].unit)
        else:
            dx = 0.5 * abs_(lims[0])
    return [lims[0] - dx, lims[1] + dx]


def fig_to_pngbytes(fig):
    """
    Convert figure to png image bytes.
    We also close the figure to prevent it from showing up again in
    cells further down the notebook.
    """
    import matplotlib.pyplot as plt

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def to_dict(meta):
    """
    Convert a coords, meta, attrs or masks object to a python dict.
    """
    return {name: var for name, var in meta.items()}


def is_static():
    """
    Returns `True` if the `inline` matplotlib backend is currently in use.
    """
    from matplotlib.pyplot import get_backend

    return get_backend().lower().endswith('inline')


def is_sphinx_build():
    """
    Returns `True` if we are running inside a sphinx documentation build.
    """
    if not running_in_jupyter():
        return False
    from IPython import get_ipython

    ipy = get_ipython()
    cfg = ipy.config
    meta = cfg["Session"]["metadata"]
    if hasattr(meta, "to_dict"):
        meta = meta.to_dict()
    return meta.get("scipp_sphinx_build", False)
