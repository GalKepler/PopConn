import networkx as nx
import pandas as pd
from networkx.algorithms.efficiency_measures import global_efficiency


def correlation_matrix_difference(
    mat1: pd.DataFrame, mat2: pd.DataFrame
) -> pd.DataFrame:
    """
    Compute the difference between two correlation (covariance) matrices.

    Parameters
    ----------
    mat1, mat2 : pd.DataFrame
        Covariance matrices for each group.

    Returns
    -------
    pd.DataFrame
        Difference matrix (region x region).
    """
    return mat1 - mat2


def frobenius_norm_difference(mat1: pd.DataFrame, mat2: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Frobenius norm of the difference between two covariance matrices.

    Parameters
    ----------
    mat1, mat2 : pd.DataFrame
        Covariance matrices for each group.

    Returns
    -------
    pd.DataFrame
        1x1 DataFrame with Frobenius norm.
    """
    diff = mat1 - mat2
    frob = (diff.values**2).sum() ** 0.5
    return pd.DataFrame([[frob]], index=["frobenius"], columns=["norm"])


def degree_difference(mat1: pd.DataFrame, mat2: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the difference in weighted node degree between two graphs derived from covariance matrices.

    Parameters
    ----------
    mat1, mat2 : pd.DataFrame
        Covariance matrices for each group.

    Returns
    -------
    pd.DataFrame
        A one-column DataFrame indexed by region name, with the difference in degree.
    """
    G1 = nx.from_numpy_array(mat1.values)
    G2 = nx.from_numpy_array(mat2.values)

    deg1 = dict(G1.degree(weight="weight"))
    deg2 = dict(G2.degree(weight="weight"))

    regions = mat1.index
    deg_diff = {regions[i]: deg1[i] - deg2[i] for i in range(len(regions))}

    return pd.DataFrame.from_dict(deg_diff, orient="index", columns=["degree_diff"])


def strength_difference(mat1: pd.DataFrame, mat2: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the difference in node strength between two covariance matrices.

    Strength is defined as the sum of absolute weights connected to each node.

    Parameters
    ----------
    mat1, mat2 : pd.DataFrame
        Covariance matrices for each group.

    Returns
    -------
    pd.DataFrame
        A one-column DataFrame indexed by region name, with the difference in strength.
    """
    strength1 = mat1.abs().sum(axis=1)
    strength2 = mat2.abs().sum(axis=1)
    return pd.DataFrame(strength1 - strength2, columns=["strength_diff"])


def global_efficiency_difference(
    mat1: pd.DataFrame, mat2: pd.DataFrame
) -> pd.DataFrame:
    """
    Compute the difference in global efficiency between two covariance matrices.

    Global efficiency measures how efficiently information is exchanged in a network,
    calculated as the average inverse shortest path length.

    Parameters
    ----------
    mat1, mat2 : pd.DataFrame
        Covariance matrices for each group.

    Returns
    -------
    pd.DataFrame
        A 1x1 DataFrame with the difference in global efficiency.
    """
    G1 = nx.from_numpy_array(mat1.values)
    G2 = nx.from_numpy_array(mat2.values)

    eff1 = global_efficiency(G1)
    eff2 = global_efficiency(G2)

    return pd.DataFrame([[eff1 - eff2]], columns=["global_efficiency_diff"])
