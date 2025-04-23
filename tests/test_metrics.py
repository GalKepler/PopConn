import pandas as pd
import pytest

from popconn.core import CovConn
from popconn.stats import METRICS


@pytest.fixture
def covariance_matrices():
    """Return group1 and group2 covariance matrices computed from long-format test data."""
    data = pd.DataFrame(
        {
            "subject_id": ["s1"] * 3
            + ["s2"] * 3
            + ["s3"] * 3
            + ["s4"] * 3
            + ["s5"] * 3
            + ["s6"] * 3,
            "region": ["A", "B", "C"] * 6,
            "value": [
                1,
                2,
                3,
                1.2,
                2.1,
                2.9,
                0.8,
                1.9,
                2.7,
                1.1,
                1.8,
                3.1,
                1.3,
                2.3,
                2.8,
                1.0,
                2.0,
                3.0,
            ],
            "group": ["young"] * 9 + ["old"] * 9,
        }
    )

    group1 = data[data["group"] == "young"]
    group2 = data[data["group"] == "old"]

    conn1 = CovConn(group1, long_format=True).compute_covariance()
    conn2 = CovConn(group2, long_format=True).compute_covariance()

    return conn1, conn2


def test_all_registered_metrics_run_without_error(covariance_matrices):
    mat1, mat2 = covariance_matrices

    for name, func in METRICS.items():
        result = func(mat1, mat2)
        assert isinstance(result, pd.DataFrame), f"{name} did not return a DataFrame"
        assert not result.isnull().values.any(), f"{name} returned NaNs"


def test_output_shapes(covariance_matrices):
    mat1, mat2 = covariance_matrices

    expected_shapes = {
        "correlation_matrix_difference": (3, 3),
        "frobenius_norm_difference": (1, 1),
        "degree_difference": (3, 1),
        "strength_difference": (3, 1),
        "global_efficiency_difference": (1, 1),
    }

    for name, func in METRICS.items():
        result = func(mat1, mat2)
        assert (
            result.shape == expected_shapes[name]
        ), f"{name} returned shape {result.shape}, expected {expected_shapes[name]}"
