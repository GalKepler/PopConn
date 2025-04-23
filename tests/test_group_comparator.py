import pandas as pd
import pytest

from popconn.stats.comparator import GroupComparator
from popconn.stats.metrics import correlation_matrix_difference


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


def test_group_comparator_instantiates(long_format_data):
    comparator = GroupComparator(
        data=long_format_data,
        group_col="group",
        long_format=True,
        subject_col="subject_id",
        region_col="region",
        value_col="value",
    )
    assert comparator.group_labels == ("young", "old")
    assert comparator.group1_data.shape[0] > 0
    assert comparator.group2_data.shape[0] > 0


def test_run_permutation_test_output_structure(long_format_data):
    comparator = GroupComparator(
        data=long_format_data,
        group_col="group",
        long_format=True,
        subject_col="subject_id",
        region_col="region",
        value_col="value",
    )
    results = comparator.run_permutation_test(
        stat_func=correlation_matrix_difference,
        n_permutations=10,
        return_distribution=True,
        random_state=42,
    )
    assert "observed" in results
    assert "p_values" in results
    assert "null_distributions" in results
    assert results["observed"].shape == results["p_values"].shape
    assert results["null_distributions"].shape == (10, 3, 3)
    assert not pd.isnull(results["p_values"]).any().any(), "p-values contain NaNs"
    assert (
        not pd.isnull(results["observed"]).any().any()
    ), "observed difference contains NaNs"
    assert not pd.isnull(
        results["null_distributions"]
    ).any(), "null_distributions contain NaNs"
    assert "permutation_labels" in results
    assert len(results["permutation_labels"]) == 10
    assert isinstance(results["permutation_labels"][0], pd.DataFrame)
