# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from .._scipp.core import DataArray, Dataset, Variable
from ..typing import VariableLike

if TYPE_CHECKING:
    import pandas as pd


def from_pandas_series(se: pd.Series) -> DataArray:
    row_index = se.axes[0]
    row_index_name = "row" if row_index.name is None else str(row_index.name)
    name = "" if se.name is None else str(se.name)

    return DataArray(
        data=Variable(values=se.values, dims=[row_index_name]),
        coords={row_index_name: Variable(dims=[row_index_name], values=row_index)},
        name=name,
    )


def from_pandas_dataframe(df: pd.DataFrame) -> Dataset:
    import pandas as pd

    row_index = df.axes[0]
    row_index_name = row_index.name or "row"

    if df.ndim == 1:
        # Special case for 1d dataframes, treat them as a series, but still
        # wrap them in a dataset object for consistency of return types.
        return Dataset(data={row_index_name: from_pandas_series(pd.Series(df))})

    sc_data = {}
    for column_name in df.axes[1]:
        sc_data[f"{column_name}"] = from_pandas_series(pd.Series(df[column_name]))

    return Dataset(data=sc_data)


def from_pandas(pd_obj: Union[pd.DataFrame, pd.Series]) -> VariableLike:
    """Converts a pandas.DataFrame or pandas.Series object into a
    scipp Dataset or DataArray respectively.

    Parameters
    ----------
    pd_obj:
        The Dataframe or Series to convert.

    Returns
    -------
    :
        The converted scipp object.
    """
    import pandas as pd

    if isinstance(pd_obj, pd.DataFrame):
        return from_pandas_dataframe(pd_obj)
    elif isinstance(pd_obj, pd.Series):
        return from_pandas_series(pd_obj)
    else:
        raise ValueError(f"from_pandas: cannot convert type '{type(pd_obj)}'")
