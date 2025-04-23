Welcome to PopConn's Documentation!
====================================

**PopConn** is a Python toolkit for constructing and analyzing population-level covariance connectomes. It provides tools for performing statistical comparisons on brain networks derived from inter-subject correlations of regional brain metrics.

Features
--------

- Compute **population covariance connectomes** from group-level regional data.
- Support for **group comparisons** and **permutation testing**.
- Integrated **clustering** methods (e.g., **Louvain**, **consensus clustering**).
- Tools for **visualization** and **interpretation** of brain networks.
- ⚙️ **Extensible design** for multi-modal and age-related analyses.

Getting Started
---------------

To get started with **PopConn**, follow these instructions to install and use the toolkit:

1. **Installation**: Install `PopConn` and its dependencies.
2. **Usage**: Check out the provided examples and tutorials.

Installation
------------

To install **PopConn**, you can clone the repository and install using `Poetry`:

```bash
git clone https://github.com/GalKepler/popconn.git
cd popconn
poetry install
```
Alternatively, you can install it directly from PyPI:
```bash
pip install popconn
```

Tutorials
----------

1. **Covariance Connectome Tutorial**

   Learn how to compute a **population-level covariance connectome** from your regional brain metrics, and visualize brain network connectivity.

   [Covariance Connectome Tutorial](tutorials/popconn_tutorial_covconn.ipynb)

2. **Group Comparison Tutorial**

   This tutorial walks through performing a **group comparison** (e.g., young vs. old adults) using **permutation testing** to compare covariance matrices.

   [Group Comparison Tutorial](tutorials/popconn_group_comparison_tutorial.ipynb)

3. **Clustering and Visualization Tutorial**

   Learn how to use the **Louvain clustering method** on the population covariance matrices to identify and visualize brain sub-networks.

   [Clustering and Visualization Tutorial](tutorials/popconn_clustering_tutorial.ipynb)

4. **Statistical Metrics Tutorial**

   This tutorial explains how to compute various **statistical metrics** on brain networks, such as **Frobenius norm**, **correlation matrix differences**, and more.

   [Statistical Metrics Tutorial](tutorials/popconn_statistical_metrics_tutorial.ipynb)

API Reference
-------------

The **PopConn** API provides detailed tools for computing covariance connectomes, performing statistical analysis, and clustering brain networks.

For the full API documentation, see:

- `API Reference` (coming soon)

Contributing
------------

We welcome contributions to **PopConn**! If you have suggestions, bug fixes, or new features, feel free to create a pull request.

To contribute:

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch
4. Submit a pull request with your changes

License
-------

**PopConn** is licensed under the MIT License. See the `LICENSE` file for more details.

Support
-------

If you encounter issues or have questions, feel free to open an issue on the GitHub repository:

[PopConn GitHub Issues](https://github.com/GalKepler/popconn/issues)

Links
-----

- [GitHub Repository](https://github.com/GalKepler/popconn)
- [ReadTheDocs Documentation](https://popconn.readthedocs.io/)
