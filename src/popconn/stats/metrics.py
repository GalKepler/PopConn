import pandas as pd

from popconn.core.core import CovConn


def correlation_matrix_difference(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the difference between correlation matrices of two datasets.

    Parameters
    ----------
    df1, df2 : pd.DataFrame
        Data for each group (in long format).

    Returns
    -------
    pd.DataFrame
        Difference matrix (region x region).
    """
    conn1 = CovConn(df1, long_format=True).compute_covariance()
    conn2 = CovConn(df2, long_format=True).compute_covariance()
    return conn1 - conn2


def frobenius_norm_difference(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Frobenius norm of the difference between two correlation matrices.

    Parameters
    ----------
    df1, df2 : pd.DataFrame
        Data for each group (in long format).

    Returns
    -------
    pd.DataFrame
        1x1 DataFrame with Frobenius norm.
    """
    conn1 = CovConn(df1, long_format=True).compute_covariance()
    conn2 = CovConn(df2, long_format=True).compute_covariance()
    diff = conn1 - conn2
    frob = (diff.values**2).sum() ** 0.5
    return pd.DataFrame([[frob]], index=["frobenius"], columns=["norm"])
