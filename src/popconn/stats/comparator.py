from typing import Callable, List, Optional, Tuple

import numpy as np
import pandas as pd

from popconn.core import CovConn


class GroupComparator:
    """
    A class for performing permutation-based statistical comparisons between two groups
    in long- or wide-format data using user-defined covariance matrix-based metrics.

    This class computes a statistic (e.g., correlation matrix difference, network metric difference)
    based on the covariance matrices of two groups and evaluates its significance using permutation testing.

    Parameters
    ----------
    data : pd.DataFrame
        The full dataset containing all subjects, brain features, and group labels.
    group_col : str
        Name of the column identifying group membership.
    long_format : bool, optional
        Whether the data is in long-format (default is False).
    subject_col : str, optional
        Column name for subject identifiers (used only if long_format=True).
    region_col : str, optional
        Column name for region or feature identifiers (used only if long_format=True).
    value_col : str, optional
        Column name for the values being measured (used only if long_format=True).

    Attributes
    ----------
    group_labels : Tuple[str, str]
        Unique labels for the two groups being compared.
    group1_data : pd.DataFrame
        Subset of data for group 1.
    group2_data : pd.DataFrame
        Subset of data for group 2.
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
        self.data = data
        self.group_col = group_col
        self.long_format = long_format
        self.subject_col = subject_col
        self.region_col = region_col
        self.value_col = value_col

        groups = data[group_col].unique()
        if len(groups) != 2:
            raise ValueError("Exactly two groups are required for comparison.")
        self.group_labels: Tuple[str, str] = tuple(groups)

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
        Run a permutation test comparing two groups using a matrix-based statistic.

        Parameters
        ----------
        stat_func : Callable
            Function that takes two covariance matrices and returns a pd.DataFrame statistic.
        n_permutations : int
            Number of permutations to perform (default: 1000).
        return_distribution : bool
            Whether to return the full null distribution (default: False).
        random_state : int or None
            Seed for reproducibility (default: None).

        Returns
        -------
        dict
            {
                'observed': pd.DataFrame,
                'p_values': pd.DataFrame,
                'null_distributions': np.ndarray or None,
                'permutation_labels': list of pd.DataFrame
            }
        """
        rng = np.random.default_rng(random_state)

        observed = self._compute_observed_statistic(stat_func)
        null_diffs, label_history = self._compute_null_distribution(
            stat_func, n_permutations, rng
        )

        p_values = self._compute_p_values(observed, np.stack(null_diffs))

        return {
            "observed": observed,
            "p_values": pd.DataFrame(
                p_values, index=observed.index, columns=observed.columns
            ),
            "null_distributions": np.stack(null_diffs) if return_distribution else None,
            "permutation_labels": label_history,
        }

    def _compute_observed_statistic(
        self,
        stat_func: Callable[[pd.DataFrame, pd.DataFrame], pd.DataFrame],
    ) -> pd.DataFrame:
        """Compute the observed statistic from group-level covariance matrices."""
        cov1 = self._compute_covariance(self.group1_data)
        cov2 = self._compute_covariance(self.group2_data)
        return stat_func(cov1, cov2)

    def _compute_null_distribution(
        self,
        stat_func: Callable[[pd.DataFrame, pd.DataFrame], pd.DataFrame],
        n_permutations: int,
        rng: np.random.Generator,
    ) -> Tuple[List[np.ndarray], List[pd.DataFrame]]:
        """
        Generate the null distribution via group-label permutations.

        Returns
        -------
        null_diffs : list of np.ndarray
            Statistic computed for each permutation.
        label_history : list of pd.DataFrame
            The group label assignments used in each permutation.
        """
        null_diffs = []
        label_history = []

        for _ in range(n_permutations):
            permuted_labels = self._permutation_subject_labels(rng)
            shuffled = self._get_shuffled_data(permuted_labels)

            g1 = shuffled[shuffled[self.group_col] == self.group_labels[0]]
            g2 = shuffled[shuffled[self.group_col] == self.group_labels[1]]

            cov1 = self._compute_covariance(g1)
            cov2 = self._compute_covariance(g2)

            null_stat = stat_func(cov1, cov2)
            null_diffs.append(null_stat.values)
            label_history.append(permuted_labels)

        return null_diffs, label_history

    def _compute_covariance(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute a covariance matrix from a group's data.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame of a single group.

        Returns
        -------
        pd.DataFrame
            Covariance matrix (regions × regions).
        """
        return CovConn(
            df,
            long_format=self.long_format,
            subject_col=self.subject_col,
            region_col=self.region_col,
            value_col=self.value_col,
        ).compute_covariance()

    def _permutation_subject_labels(self, rng: np.random.Generator) -> pd.DataFrame:
        """
        Permute subject group labels for permutation testing.

        Parameters
        ----------
        rng : np.random.Generator
            Random number generator.

        Returns
        -------
        pd.DataFrame
            A DataFrame mapping subject ID to permuted group label.
        """
        subject_labels = self.data[[self.subject_col, self.group_col]].drop_duplicates()
        permuted = subject_labels.copy()
        permuted[self.group_col] = rng.permutation(
            subject_labels[self.group_col].values
        )
        return permuted

    def _get_shuffled_data(self, permuted: pd.DataFrame) -> pd.DataFrame:
        """
        Merge permuted group labels back into the full dataset.

        Parameters
        ----------
        permuted : pd.DataFrame
            DataFrame with permuted group labels.

        Returns
        -------
        pd.DataFrame
            Dataset with new group assignments.
        """
        return self.data.drop(columns=[self.group_col]).merge(
            permuted, on=self.subject_col
        )

    def _compute_p_values(
        self,
        observed: pd.DataFrame,
        null_diffs: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate p-values from the observed statistic and permutation distribution.

        Parameters
        ----------
        observed : pd.DataFrame
            Observed statistic.
        null_diffs : np.ndarray
            Null distribution (n_permutations × matrix shape).

        Returns
        -------
        np.ndarray
            Matrix of p-values.
        """
        return np.mean(np.abs(null_diffs) >= np.abs(observed.values), axis=0)
