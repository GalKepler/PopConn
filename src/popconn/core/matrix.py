import pandas as pd


def compute_population_covariance(
    df: pd.DataFrame, method: str = "pearson"
) -> pd.DataFrame:
    """
    Compute correlation matrix across brain regions, over subjects.

    Parameters
    ----------
    df : pd.DataFrame
        Rows = subjects, Columns = regions or metrics.
    method : str
        Correlation method: 'pearson', 'spearman', 'kendall'.

    Returns
    -------
    pd.DataFrame
        Region × region correlation matrix.
    """
    return df.corr(method=method)
