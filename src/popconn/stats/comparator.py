from typing import Callable, Optional, Tuple

import numpy as np
import pandas as pd


class GroupComparator:
    """
    GroupComparator handles permutation-based statistical comparison between
    two groups in a long- or wide-format dataset. It uses a user-defined
    statistic function to compute a difference matrix or scalar metric
    and tests its significance via permutation testing.

    Parameters
    ----------
    data : pd.DataFrame
        The full dataset containing all subjects and group labels.
    group_col : str
        Column name in `data` identifying group membership.
    long_format : bool, optional
        Whether the data is in long format (default: False).
    subject_col : str, optional
        Column name for subject identifiers (used only if long_format=True).
    region_col : str, optional
        Column name for regions/features (used only if long_format=True).
    value_col : str, optional
        Column name for the measured value (used only if long_format=True).

    Attributes
    ----------
    data : pd.DataFrame
        The original input data.
    group_labels : Tuple[str, str]
        Unique labels identifying the two comparison groups.
    group1_data : pd.DataFrame
        Subset of `data` belonging to group 1.
    group2_data : pd.DataFrame
        Subset of `data` belonging to group 2.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        group_col: str,
        *,
        long_format: bool = False,
        subject_col: str = "subject_id",
        region_col: str = "region",
        value_col: str = "value",
    ):
        self.group_col = group_col
        self.long_format = long_format
        self.subject_col = subject_col
        self.region_col = region_col
        self.value_col = value_col

        groups = data[group_col].unique()
        if len(groups) != 2:
            raise ValueError("Only two-group comparisons are supported.")

        self.group_labels: Tuple[str, str] = tuple(groups)
        self.data = data
        self.group1_data = data[data[group_col] == self.group_labels[0]]
        self.group2_data = data[data[group_col] == self.group_labels[1]]

    def run_permutation_test(
        self,
        stat_func: Callable[[pd.DataFrame, pd.DataFrame], pd.DataFrame],
        n_permutations: int = 1000,
        return_distribution: bool = False,
        random_state: Optional[int] = None,
    ) -> dict:
        """
        Perform a permutation test to compare two groups using a custom statistic.

        Parameters
        ----------
        stat_func : Callable
            Function that accepts (group1_data, group2_data) and returns a statistic
            as a pd.DataFrame (e.g., difference matrix, scalar wrapped as df).
        n_permutations : int
            Number of permutations to run (default: 1000).
        return_distribution : bool
            Whether to return the full null distribution (default: False).
        random_state : int or None
            Optional seed for reproducibility.

        Returns
        -------
        dict
            {
                'observed': pd.DataFrame,
                'p_values': pd.DataFrame,
                'null_distributions': Optional[np.ndarray]
            }
        """
        rng = np.random.default_rng(random_state)
        observed = stat_func(self.group1_data, self.group2_data)
        null_diffs = []

        for _ in range(n_permutations):
            shuffled = self.data.copy()
            shuffled[self.group_col] = rng.permutation(shuffled[self.group_col].values)
            g1 = shuffled[shuffled[self.group_col] == self.group_labels[0]]
            g2 = shuffled[shuffled[self.group_col] == self.group_labels[1]]
            null = stat_func(g1, g2)
            null_diffs.append(null.values)

        null_diffs = np.stack(null_diffs)
        p_values = np.mean(np.abs(null_diffs) >= np.abs(observed.values), axis=0)

        return {
            "observed": observed,
            "p_values": pd.DataFrame(
                p_values, index=observed.index, columns=observed.columns
            ),
            "null_distributions": null_diffs if return_distribution else None,
        }
