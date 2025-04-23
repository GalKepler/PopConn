import pandas as pd

from popconn.stats.comparator import GroupComparator
from popconn.stats.metrics import correlation_matrix_difference


def compare_groups(
    data: pd.DataFrame,
    group_col: str,
    *,
    method: str = "pearson",
    n_permutations: int = 1000,
    return_distribution: bool = False,
    long_format: bool = False,
    subject_col: str = "subject_id",
    region_col: str = "region",
    value_col: str = "value",
) -> dict:
    """
    Compare two groups' covariance matrices using permutation testing.

    This function is a wrapper around GroupComparator that uses
    the correlation matrix difference as the default statistic.

    Parameters
    ----------
    data : pd.DataFrame
        Full dataset containing both groups.
    group_col : str
        Column indicating group membership.
    method : str
        Correlation method for covariance matrices.
    n_permutations : int
        Number of permutations for testing.
    return_distribution : bool
        Whether to return the full null distribution.
    long_format : bool
        Whether the input data is in long format.
    subject_col : str
        Subject ID column.
    region_col : str
        Region/feature column.
    value_col : str
        Measurement column.

    Returns
    -------
    dict
        Dictionary with keys:
        - 'observed': the observed matrix difference
        - 'p_values': permutation-based p-values
        - 'null_distributions': optional permutation matrix stack
    """
    comparator = GroupComparator(
        data=data,
        group_col=group_col,
        long_format=long_format,
        subject_col=subject_col,
        region_col=region_col,
        value_col=value_col,
    )

    return comparator.run_permutation_test(
        stat_func=correlation_matrix_difference,
        n_permutations=n_permutations,
        return_distribution=return_distribution,
    )
