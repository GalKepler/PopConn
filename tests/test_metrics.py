import pandas as pd
import pytest

from popconn.stats.metrics import (
    correlation_matrix_difference,
    frobenius_norm_difference,
)


@pytest.fixture
def long_format_data():
    return pd.DataFrame(
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


def test_correlation_matrix_difference(long_format_data):
    group1 = long_format_data[long_format_data["group"] == "young"]
    group2 = long_format_data[long_format_data["group"] == "old"]

    result = correlation_matrix_difference(group1, group2)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 3)  # Expecting a region x region matrix


def test_frobenius_norm_difference(long_format_data):
    group1 = long_format_data[long_format_data["group"] == "young"]
    group2 = long_format_data[long_format_data["group"] == "old"]

    result = frobenius_norm_difference(group1, group2)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 1)  # Frobenius norm is a scalar value
