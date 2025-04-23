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

- 🧠 Compute **population covariance connectomes** from group-level regional data
- 🧪 Support for **group comparisons** and bootstrapping
- 🔍 Integrated clustering (e.g., **Louvain**, consensus clustering)
- 📈 Tools for **visualization** and interpretation of brain networks
- ⚙️ Extensible design for multi-modal and age-related analyses

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
from popconn.matrix import compute_population_covariance
from popconn.clustering import louvain_cluster

# Example: rows = subjects, columns = brain regions
df = pd.read_csv("data/regional_metrics.csv")

# Compute a region-by-region correlation matrix across subjects
conn_matrix = compute_population_covariance(df)

# Cluster using Louvain method
labels = louvain_cluster(conn_matrix)
```

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
