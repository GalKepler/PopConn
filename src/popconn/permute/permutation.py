import numpy as np
import pandas as pd


def permute_labels(df: pd.DataFrame, group_col: str) -> pd.Series:
    """
    Shuffle group labels for permutation testing.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe with a group column.
    group_col : str
        The name of the column to permute.

    Returns
    -------
    pd.Series
        A new shuffled version of the group column.
    """
    return pd.Series(np.random.permutation(df[group_col].values), index=df.index)
