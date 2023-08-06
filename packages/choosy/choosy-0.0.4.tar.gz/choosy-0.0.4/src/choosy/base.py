# SPDX-FileCopyrightText: 2023-present Casey Schneider-Mizell <caseysm@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

def _is_array_like(value):
    if isinstance(value, str):
        return False
    else:
        try:
            len(value)
            return True
        except:
            return False

def _make_listlike(value):
    if not _is_array_like(value):
        return [value]
    else:
        return value

def _rng(seed: Optional[int] = None):
    # Build the random number generator
    if seed is None:
        return np.random.default_rng()
    else:
        return np.random.default_rng(seed=seed)

def _unique_values_sorted(df, column):
    return df[column].sort_values().unique()

class StructuredSampler:
    def __init__(
        self,
        data: pd.DataFrame,
        bin_column: Optional[Union[str, List[str]]] = None,
        weight_column: Optional[str] = None,
        count_column: Optional[str] = None,
        seed: Optional[int] = None,
    ):
        """
        Set up a dataframe for sampling.

        Parameters
        ~~~~~~~~~
        data: pd.DataFrame
            Dataframe to sample from.
        bin_column: str or list of str, optional.
            Column or columns to use for binning. If None, no binning is used.
        weight_column: str, optional.
            Column to use for weighting. If None, no weighting is used.
        seed: int, optional.
            Seed for the random number generator. Default is None.
        """
        self._data = data
        self._weight_column = weight_column
        self._bin_column = bin_column
        self._rng = _rng(seed)
        self._count_column = count_column
        self._count_types = {}
        if self._count_column is not None:
            self._count_types[self._count_column] = _unique_values_sorted(self._data, self._count_column)

    def sample_data(
        self,
        n_sample: Union[int, Dict, pd.Series],
        count_column: Optional[str] = None,
        bin_column: Optional[Union[str, List[str]]] = None,
        weight_column: Optional[str] = None,
        replace: Optional[bool] = True,
        column_name: Optional[str] = "sample_count",
    ):
        """
        Sample data from a dataframe, selecting specified numbers of samples based on values in a column or columns.

        Parameters
        ~~~~~~~~~
        n_sample: int, pd.Series, or dict.
            Number of samples to pull from the initial dataframe.
            If an int, bin_column is not used.
            If a dict, maps bins to number of samples per bin. Must have a bin_column.
            If a Series, maps bins to number of samples via n_sample.loc[*index_value] where
            bin_column must be the same length and order as the indices, for example as in a
            groupby+count operation.
        count_column : str or None.
            Column to accumulate values for.
            If None, returns the sampled dataframe rather than accumulated values.
        bin_column : str or list.
            Column to use for binning. Values in this column must match values in the n_sample dict or series.
            Bin column can be a list of strings if n_sample is a series with a multi-level index.
        replace: bool, optional.
            Chooses whether to sample data with replacement or not. Default is True.
        column_name: str, optional.
            Name of the column to use for the aggregated count column. Default is "sample_count".

        Returns
        ~~~~~~~
        pd.DataFrame
            A dataframe sampled from the original. If count_column is not None, the dataframe is aggregated by values
            from that column, otherwise the dataframe rows are returned directly.
        """
        if bin_column is None:
            bin_column = self._bin_column
        if weight_column is None:
            weight_column = self._weight_column
        dfs, ns, weights = self._build_stratification(n_sample, bin_column, weight_column)
        inds = self._stratified_indices(dfs, ns, weights, n_repeats=1, replace=replace).squeeze()
        return self._aggregate_results(
            self._data.loc[inds],
            count_column,
            column_name,
        )

    def sample_repeat(
        self,
        n_repeat: int,
        n_sample: Union[int, Dict, pd.Series],
        count_column: Optional[str] = None,
        bin_column: Optional[Union[str, List[str]]] = None,
        weight_column: Optional[str] = None,
        replace: Optional[bool] = True,
    ):
        """Repeated sampling of counts from a dataframe with the same parameters.

        Parameters
        ----------
        n_repeat : int
            Number of repeated samplings.
        n_sample : int, pd.Series, or dict.
            Number of samples to pull from the initial dataframe.
            Same behavior as in sample_data.
            If an int, bin_column is not used.
            If a dict, maps bins to number of samples per bin. Must have a bin_column.
            If a Series, maps bins to number of samples via n_sample.loc[*index_value] where
            bin_column must be the same length and order as the indices, for example as in a
            groupby+count operation.
        count_column : str
            Column to accumulate values for.
        bin_column : str or list, optional
            Column to use for binning. Values in this column must match values in the n_sample dict or series.
            Bin column can be a list of strings if n_sample is a series with a multi-level index.
            Optional, default is None.
        weight_column : str, optional
            Column to use for sample weighting. Optional, default is None.
        replace : bool, optional
            Chooses whether to sample with replacement, by default True
        seed : int, optional
            Random seed value, by default None

        Returns
        -------
        pd.DataFrame
            A dataframe with columns that are sampled values and rows that are repeated samples.
        """
        if bin_column is None:
            bin_column = self._bin_column
        if weight_column is None:
            weight_column = self._weight_column
        if count_column is None:
            count_column = self._count_column
            if count_column is None:
                raise ValueError("count_column must be specified here or in the constructor.")

        dfs, ns, weights = self._build_stratification(n_sample, bin_column, weight_column)
        inds = self._stratified_indices(dfs, ns, weights, n_repeat, replace)
        dfs_to_concat = []
        trial_column = 'trials'
        while trial_column in self._data.columns:
            trial_column += '_'
        for ii, ind_row in enumerate(inds):
            df_temp = self._data.loc[ind_row]
            df_temp[trial_column] = ii
            dfs_to_concat.append(df_temp)
        df_all = pd.concat(dfs_to_concat, ignore_index=True)

        out = pd.crosstab(
            index=df_all[trial_column],
            columns=df_all[count_column],
        )
        return self._format_counted_output(out, count_column)

    def _build_stratification(
        self,
        n_sample,
        bin_column,
        weight_column,
    ):
        dfs = []
        ns = []
        weights = []
        if isinstance(n_sample, int):
            if bin_column is None:
                dfs.append(self._data)
                ns.append(n_sample)
                weights.append(self._weights(self._data, weight_column))
            else:
                bin_values = np.unique(self._data[bin_column])
                for bin_value in bin_values:
                    df = self._data.query(self._format_filter(bin_column, bin_value))
                    dfs.append(df)
                    ns.append(n_sample)
                    weights.append(self._weights(df, weight_column))
        elif isinstance(n_sample, dict):
            if bin_column is None:
                msg = "No bin column is set!"
                raise ValueError(msg)
            for bin_value, n in n_sample.items():
                df = self._data.query(self._format_filter(bin_column, bin_value))
                dfs.append(df)
                ns.append(n)
                weights.append(self._weights(df, weight_column))
        elif isinstance(n_sample, pd.Series):
            if bin_column is None:
                msg = "No bin column is set!"
                raise ValueError(msg)
            for index_val in n_sample.index:
                df = self._data.query(self._format_filter(bin_column, index_val))
                dfs.append(df)
                ns.append(n_sample.loc[index_val])
                weights.append(self._weights(df, weight_column))
        else:
            msg = f"n_sample must be an int, dict, or pd.Series, not {type(n_sample)}"
            raise ValueError(msg)
        return dfs, ns, weights

    def _aggregate_results(self, df, count_column, name):
        "Format the results into a single dataframe."
        if count_column is None:
            return df
        else:
            return self._format_counted_output(
                df.groupby(count_column).agg(**{name: pd.NamedAgg(column=count_column, aggfunc="count")}).T,
                count_column,
            ).T

    def _format_filter(self, columns, values):
        "Format the filter for the query method."
        filters = []
        for col, val in zip(_make_listlike(columns), _make_listlike(values)):
            if isinstance(val, str):
                filters.append(f'{col}=="{val}"')
            else:
                filters.append(f"{col}=={val}")
        return " and ".join(filters)

    def _stratified_indices(
        self,
        dfs,
        ns,
        weights,
        n_repeats,
        replace,
    ):
        "Sample indices from a list of dataframes."
        indices = []
        for df, nn, w in zip(dfs, ns, weights):
            if len(df)==0:
                indices.append(np.zeros((n_repeats, 0), dtype=int))
            indices.append(
                self._rng.choice(
                    df.index.values,
                    size=(n_repeats, nn),
                    replace=replace,
                    p=w,
                )
            )
        return np.concatenate(indices, axis=1)

    def _weights(
        self,
        df,
        weight_column,
    ):
        if weight_column is None:
            weight_column = self._weight_column
        if weight_column is None:
            return None
        else:
            w = df[weight_column].values
            return w / np.sum(w)

    def _format_counted_output(self, df_out, count_column):
        if count_column is None:
            return df_out
        else:
            if count_column not in self._count_types:
                self._count_types[count_column] = _unique_values_sorted(self._data, count_column)
            count_types = self._count_types[count_column]
            for col in count_types:
                if col not in df_out.columns:
                    df_out[col] = 0
            return df_out[count_types]