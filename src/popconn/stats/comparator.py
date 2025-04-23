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

        This method shuffles the group labels for the subjects and computes the
        difference in the statistic (e.g., covariance matrices) for each permutation.
        The p-values are computed based on the proportion of permutations that show
        a difference as extreme as the observed difference.

        Parameters
        ----------
        stat_func : Callable
            A function that accepts two DataFrames (representing two groups) and
            returns a statistic (e.g., a difference matrix, scalar value).
        n_permutations : int
            The number of permutations to perform. Default is 1000.
        return_distribution : bool
            Whether to return the full null distribution (default is False).
        random_state : int or None, optional
            Optional seed for the random number generator, for reproducibility.

        Returns
        -------
        dict
            A dictionary containing:
            - 'observed' (the observed statistic)
            - 'p_values' (calculated p-values from the null distribution)
            - 'null_distributions' (the null distributions from the permutations,
              returned only if `return_distribution=True`)
            - 'permutation_labels' (subject-group assignments for each permutation)
        """
        rng = np.random.default_rng(random_state)

        # Step 1: Compute the observed statistic
        observed = stat_func(self.group1_data, self.group2_data)

        # Step 2: Initialize lists to store the results
        null_diffs, label_history = [], []

        # Step 3: Perform the permutation testing
        for _ in range(n_permutations):
            # Step 3a: Permute subject labels to shuffle group assignments
            permuted = self._permutation_subject_labels(rng)

            # Step 3b: Get shuffled data based on permuted group labels
            shuffled_data = self._get_shuffled_data(permuted)

            # Step 3c: Compute the difference in statistic for the permutation
            null_diff = self._compute_permutation_diff(stat_func, shuffled_data)
            null_diffs.append(null_diff)

            # Store the shuffled labels for later inspection
            label_history.append(permuted)

        # Step 4: Calculate p-values based on the null distribution
        null_diffs = np.stack(null_diffs)
        p_values = self._compute_p_values(observed, null_diffs)

        # Step 5: Return the results as a dictionary
        return {
            "observed": observed,
            "p_values": pd.DataFrame(
                p_values, index=observed.index, columns=observed.columns
            ),
            "null_distributions": null_diffs if return_distribution else None,
            "permutation_labels": label_history,
        }

    def _permutation_subject_labels(self, rng: np.random.Generator) -> pd.DataFrame:
        """
        Permute the group labels (subject assignments) while keeping the subjects intact.

        This function randomly shuffles the group labels for each subject but ensures
        that each subject remains associated with a full set of regions.

        Parameters
        ----------
        rng : np.random.Generator
            A random number generator instance to use for permutation.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the permuted subject group labels.
        """
        subject_labels = self.data[[self.subject_col, self.group_col]].drop_duplicates()
        permuted = subject_labels.copy()
        permuted[self.group_col] = rng.permutation(
            subject_labels[self.group_col].values
        )
        return permuted

    def _get_shuffled_data(self, permuted: pd.DataFrame) -> pd.DataFrame:
        """
        Merge the permuted subject labels back into the original data, ensuring the
        full data structure is maintained with the new group assignments.

        Parameters
        ----------
        permuted : pd.DataFrame
            The DataFrame with permuted subject group labels.

        Returns
        -------
        pd.DataFrame
            The shuffled data with the updated group labels.
        """
        return self.data.drop(columns=[self.group_col]).merge(
            permuted, on=self.subject_col
        )

    def _compute_permutation_diff(
        self, stat_func: Callable, shuffled_data: pd.DataFrame
    ) -> np.ndarray:
        """
        Compute the difference in statistics between two groups for a single permutation.

        This method calculates the statistic (e.g., covariance difference) after permuting
        the group labels and using the shuffled data.

        Parameters
        ----------
        stat_func : Callable
            The function to calculate the statistic (e.g., covariance difference).
        shuffled_data : pd.DataFrame
            The shuffled dataset with permuted group assignments.

        Returns
        -------
        np.ndarray
            The computed difference matrix or scalar from the permutation.
        """
        g1 = shuffled_data[shuffled_data[self.group_col] == self.group_labels[0]]
        g2 = shuffled_data[shuffled_data[self.group_col] == self.group_labels[1]]
        return stat_func(g1, g2).values

    def _compute_p_values(
        self, observed: pd.DataFrame, null_diffs: np.ndarray
    ) -> np.ndarray:
        """
        Compute p-values from the observed statistic and the null distribution.

        This method calculates the p-value for each element of the observed matrix by
        comparing it with the corresponding values from the null distribution. The p-value
        is the fraction of permutations where the null difference was as extreme as the
        observed difference.

        Parameters
        ----------
        observed : pd.DataFrame
            The observed statistic (e.g., covariance difference).
        null_diffs : np.ndarray
            The null distribution containing statistics from the permutations.

        Returns
        -------
        np.ndarray
            The p-values for each element in the observed statistic matrix.
        """
        return np.mean(np.abs(null_diffs) >= np.abs(observed.values), axis=0)
