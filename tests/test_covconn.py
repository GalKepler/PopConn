import pandas as pd
import pytest

from popconn.core.core import CovConn


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


def test_covconn_wide_shape(long_format_data):
    conn = CovConn(
        data=long_format_data,
        long_format=True,
        subject_col="subject_id",
        region_col="region",
        value_col="value",
    )
    assert conn.wide_data.shape == (6, 3)  # 6 subjects, 3 regions


def test_covariance_computation(long_format_data):
    conn = CovConn(long_format_data, long_format=True)
    cov = conn.compute_covariance()
    assert cov.shape[0] == cov.shape[1]
    assert (cov.columns == cov.index).all()


def test_covariance_property(long_format_data):
    conn = CovConn(long_format_data, long_format=True)
    conn.compute_covariance()
    cov = conn.covariance
    assert isinstance(cov, pd.DataFrame)
    assert cov.shape == (3, 3)
