"""
Methods related to plotting, regarding matplotlib.
"""
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np


def cumulative_bins(*arrs: Sequence[float], num_bins: int) -> Sequence[float]:
    """
    Will return an array to be used in a matplotlib histogram for the keyword `bins`.
    If you are plotting multiple histograms on the same plot, their bin width won't
    necessarily be the same size. Pass them to this method along with the total number
    of bins to rectify that.

    Parameters:
    arrs - The data that will be plotted in the histogram
    num_bins - The total number of bins
    """
    return np.histogram(np.hstack(arrs), bins=num_bins)[2]


def log_bins(*arrs: Sequence[float], num_bins: int) -> Sequence[float]:
    """
    Will return an array to be used in a matplotlib histogram for the keyword `bins`.
    These bins will have equal width in log space and, like `tot_bins`, can be passed
    multiple sets of data or just one.

    Parameters:
    arrs - The data that will be plotted in the histogram
    num_bins - The total number of bins
    """
    all_data = np.hstack(arrs)
    return np.geomspace(np.min(all_data), np.max(all_data), num_bins)


def bar_count(
    ax: plt.Axes,
    counts: Union[dict[str, float], Sequence[float]],
    labels: Optional[str] = None,
    label_bars: bool = False,
    sort_type: Optional[str] = None,
    *,
    bar_params: Optional[dict[str, ...]] = None,
    **kwargs: ...,
) -> plt.Axes.bar:
    """
    Creates a bar plot given values and labels. The parameter `counts` can be either a
    dictionary or a list (of values).

    Parameters:
    ax - Matplotlib axis to plot on
    counts - Dictionary of form {label: value} or a list of values
    labels (default None) - Optional list of labels. If specified, `counts` should then
        also be a list. If not specified, then `counts` should be a dictionary.
    label_bars (default False) - If True, each bar will be labeled with its value shown
        on top of the bar.
    sort_type (default None) - How to sort the bars. By default, it won't sort. Can be
        'asc' for sort ascending (smallest to largest value left to right) or 'desc' for
        descending.
    bar_params (default {}) - A dictionary of keywords to be specifically passed to
        `ax.bar`.
    kwargs - Other keywords used in the plot. They (with their defaults) are:
        label_fmt (default "{:.2f}") - The string format for the bar label
        ylabel (default "") - The label of the y axis
        xlabel (default "") - The label of the x axis
        ylabel_fs (default 13) - Fontsize of the y axis label
        xlabel_fs (default 13) - Fontsize of the x axis label
        title (default "") - The title of the plot
        title_fs (default 18) - The fontsize of the plot
        x_rot (default 45) - Degree angle to rotate the x axis bar labels
            counterclockwise from horizontal
    """
    # Make sure `counts` and `labels` play nicely together
    if labels is not None:
        if not isinstance(counts, (list, tuple, np.ndarray)):
            raise TypeError(
                "If `labels` is defined, then `counts` should be a list-type object, "
                f"not a {type(counts)} object."
            ) from None
        if not isinstance(labels, (list, tuple, np.ndarray)):
            raise TypeError(
                "If `labels` is defined, then it should be a list-type object, "
                f"not a {type(labels)} object."
            ) from None
        if len(counts) != len(labels):
            raise IndexError(
                "If `labels` is defined, then it should be an equal length to `counts`."
                f" Current lengths are {len(counts)=} and {len(labels)=}."
            ) from None
        values = counts
    else:
        values = list(counts.values())
        labels = list(counts.keys())

    # Sort data if needed
    if sort_type is not None:
        if sort_type not in {"asc", "desc"}:
            raise ValueError(
                f"`sort_type` should be either 'desc' or 'asc', not {sort_type}."
            )
        values, labels = zip(
            *sorted(
                zip(values, labels), key=lambda x: x[0], reverse=sort_type == "desc"
            )
        )

    bar_params = bar_params if bar_params is not None else {}
    bar = ax.bar(labels, values, **bar_params)
    # Label the top of each bar with its value?
    if label_bars:
        ax.bar_label(bar, fmt=kwargs.get("label_fmt", "{:.2f}"))
    ax.set_ylabel(kwargs.get("ylabel", ""), fontsize=kwargs.get("ylabel_fs", 13))
    ax.set_xlabel(kwargs.get("xlabel", ""), fontsize=kwargs.get("xlabel_fs", 13))
    ax.set_title(kwargs.get("title", ""), fontsize=kwargs.get("title_fs", 18))
    ax.tick_params(axis="x", rotation=kwargs.get("x_rot", 45))

    return bar
