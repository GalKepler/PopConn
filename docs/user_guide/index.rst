User Guide
===========

This guide explains how to use the core features of **PopConn**, including how to compute covariance connectomes, perform group comparisons, and visualize results.

Getting Started
---------------

To get started, see the quick start guide:

1. [Installation Guide](../installation)
2. [Tutorial: Computing Covariance Connectomes](../tutorials/popconn_tutorial_covconn.ipynb)
3. [Tutorial: Group Comparison](../tutorials/popconn_group_comparison_tutorial.ipynb)

Usage Examples
--------------

Here are some usage examples to help you get started with **PopConn**.

### Example 1: Compute Population Covariance Matrix
.. code-block:: python
    :linenos:

    import pandas as pd
    from popconn.core.core import CovConn

    # long-format dataframe with: subject_id, region, value
    df = pd.read_csv("data/long_format_metrics.csv")

    conn = CovConn(df, long_format=True)
    covariance_matrix = conn.compute_covariance()

### Example 2: Perform Group Comparison
.. code-block:: python
   :linenos:

    from popconn.stats.comparator import GroupComparator
    from popconn.stats.metrics import correlation_matrix_difference

    comparator = GroupComparator(
        data=df,
        group_col="group",
        long_format=True,
        subject_col="subject_id",
        region_col="region",
        value_col="value"
    )

    results = comparator.run_permutation_test(
        stat_func=correlation_matrix_difference,
        n_permutations=1000,
        return_distribution=True
    )

    results["p_values"]
