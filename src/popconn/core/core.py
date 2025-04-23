import pandas as pd

from popconn.core.matrix import compute_population_covariance


class CovConn:
    """
    CovConn handles population-level covariance connectomes from long- or wide-format data.

    Attributes
    ----------
    data : pd.DataFrame
        Input data in either wide or long format.
    long_format : bool
        Whether the input data is in long format.
    subject_col : str
        Column for subject identifiers (used in long format).
    region_col : str
        Column for brain regions/features (used in long format).
    value_col : str
        Column for measurement values (used in long format).
    """

    def __init__(
        self,
        data: pd.DataFrame,
        *,
        long_format: bool = False,
        subject_col: str = "subject_id",
        region_col: str = "region",
        value_col: str = "value",
    ):
        self.data = data
        self.long_format = long_format
        self.subject_col = subject_col
        self.region_col = region_col
        self.value_col = value_col
        self._wide_data = self._to_wide_format(data) if long_format else data.copy()
        self._covariance = None

    def _to_wide_format(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.pivot(
            index=self.subject_col, columns=self.region_col, values=self.value_col
        )

    def compute_covariance(self, method: str = "pearson") -> pd.DataFrame:
        """
        Compute a region × region correlation matrix.

        Parameters
        ----------
        method : str
            Correlation method: 'pearson', 'spearman', or 'kendall'.

        Returns
        -------
        pd.DataFrame
            Correlation matrix of shape (n_regions, n_regions).
        """
        self._covariance = compute_population_covariance(self._wide_data, method)
        return self._covariance

    @property
    def wide_data(self) -> pd.DataFrame:
        """
        Access the wide-format representation of the data.
        """
        return self._wide_data

    @property
    def covariance(self) -> pd.DataFrame:
        """
        Access the most recently computed covariance matrix.
        """
        if self._covariance is None:
            raise ValueError(
                "Covariance matrix has not been computed yet. Call `compute_covariance()` first."
            )
        return self._covariance
