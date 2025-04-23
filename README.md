# 🧠 PopConn

**PopConn** is a Python toolkit for constructing and analyzing **population-level covariance connectomes**—brain networks derived from **inter-subject correlation** of brain region metrics like gray matter volume or diffusion measures.

## 📊 Overview

| Category | Badges |
|----------| -------|
| 📚 Docs  | _Coming soon_
| 🧪 Tests & Coverage  | [![CI](https://github.com/GalKepler/popconn/actions/workflows/ci.yml/badge.svg)](https://github.com/GalKepler/popconn/actions)<br> [![Codecov](https://codecov.io/gh/GalKepler/popconn/branch/main/graph/badge.svg)](https://codecov.io/gh/GalKepler/popconn) <br> [![Codacy](https://app.codacy.com/project/badge/Grade/362bbdaea27548bb9f347eabae612ddb)](https://app.codacy.com/gh/GalKepler/popconn/dashboard) |
| 🐍 Version           | _Coming soon on PyPI_                                                                                                                                       |
| 🎨 Styling           | [![Black](https://img.shields.io/badge/formatter-black-000000.svg)](https://github.com/psf/black) <br> [![isort](https://img.shields.io/badge/imports-isort-%231674b1.svg)](https://pycqa.github.io/isort/) <br> [![Ruff](https://img.shields.io/badge/linter-ruff-blue)](https://github.com/astral-sh/ruff) <br> [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) |
| 📄 License           | [![License](https://img.shields.io/github/license/GalKepler/popconn.svg)](https://opensource.org/license/mit)                                              |

---

## ✨ Features

- 📈 Compute **covariance connectomes** from either **wide** or **long-format** data
- 🔁 Perform **permutation-based group comparisons** with the `GroupComparator`
- 🧱 Build reusable pipelines using the `CovConn` class
- 🔬 Plug in custom **statistical metrics** (e.g., matrix difference, Frobenius norm)
- 📊 Designed for **neuroimaging research**, aging, and population-level modeling

---

## 📦 Installation

```bash
git clone https://github.com/GalKepler/popconn.git
cd popconn
poetry install
```

---

## 🚀 Quick Start

```python
import pandas as pd
from popconn.core.core import CovConn

# long-format dataframe with: subject_id, region, value
df = pd.read_csv("data/long_format_metrics.csv")

conn = CovConn(df, long_format=True)
covariance_matrix = conn.compute_covariance()

```

🎯 Compare Groups with Permutation Testing
```python
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

```
---

## 📘 Tutorials
* 🧠 [CovConn Tutorial Notebook](https://github.com/GalKepler/PopConn/blob/main/notebooks/popconn_tutorial_covconn.ipynb)
* 📊 [Group Comparison Notebook](https://github.com/GalKepler/PopConn/blob/main/notebooks/popconn_group_comparison_tutorial.ipynb)


---

## 🧪 Testing

```bash
poetry run pytest
```
To run all linters:
```bash
poetry run ruff check .
poetry run black --check .
poetry run isort --check-only .
```

---

## 🧬 Use Cases


* Comparing covariance networks between groups (e.g., young vs. old adults)

* Identifying stable communities via bootstrapped clustering

* Visualizing subnetwork structures in population brain data

* Tracking network change across time or skill acquisition


## 🙌 Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
