# EPU Forecasting — MSc Thesis

**Forecasting Economic Policy Uncertainty using Hybrid ML-Econometric Models**

> MSc Business Statistics | VIT | 2023-2025

---

## What this project does

Forecasts three US policy uncertainty indices using 141 monthly macro variables (1987-2023):

| Index | Full Name | What it measures |
|-------|-----------|-----------------|
| EPU | Economic Policy Uncertainty | Newspaper coverage + tax expiry + forecaster disagreement |
| CPU | Climate Policy Uncertainty | Uncertainty about climate/environmental policy |
| GPR | Geopolitical Risk | Wars, terrorism, international tensions |

Models compared:
- ARIMAX: ARIMA with Granger-selected exogenous variables
- SARIMA: Seasonal ARIMA via grid search
- LightGBM: Gradient boosted trees with SHAP explainability

---
## 📁 Repository Structure

```
epu-thesis/
├── data/
│   ├── raw/                         # Original source files
│   │   ├── POLICYUS.xlsx            # Master panel: 141 variables, 435 months
│   │   ├── CPU_index.csv            # Climate Policy Uncertainty
│   │   ├── US_Policy_Uncertainty_Data.xlsx
│   │   └── Categorical_EPU_Data.xlsx
│   │
│   └── processed/                   # Processed outputs & statistical results
│       ├── filtered_data.xlsx
│       ├── granger_causality_results.xlsx
│       ├── hurst_exponent_results.xlsx
│       ├── seasonality_test_results.xlsx
│       ├── stationarity_test_results.xlsx
│       ├── tsays_test_results.xlsx
│       └── df_transformed.csv       # Generated in preprocessing stage
│
├── notebooks/
│   ├── 01_data_loading_preprocessing.ipynb   # Data cleaning & transformation
│   ├── 02_statistical_tests.ipynb            # Stationarity, Hurst, TSay tests
│   ├── 03_exploratory_data_analysis.ipynb    # Visualization & insights
│   ├── 04_arimax_sarima_modeling.ipynb       # Classical time-series models
│   └── 05_lightgbm_hybrid.ipynb              # ML-based hybrid forecasting
│
├── outputs/                         # Saved plots, model outputs, figures
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```


---

## Notebooks Guide

| Notebook | What it does |
|----------|-------------|
| 01 | Load POLICYUS, transform non-stationary variables, save df_transformed.csv |
| 02 | ADF+KPSS, Hurst Exponent, Seasonality, Tsay's Test, Granger Causality |
| 03 | Time series plots, distributions, correlation heatmap, ACF/PACF, STL |
| 04 | ARIMAX + SARIMA modeling and comparison |
| 05 | LightGBM + SHAP + final 3-model comparison |

**Run in order: 01 -> 02 -> 03 -> 04 -> 05**
Always run 01 first — it creates df_transformed.csv needed by all other notebooks.

---

## Key Findings

### Stationarity
| Variable | ADF | KPSS | Conclusion |
|----------|-----|------|-----------|
| EPU | Stationary | Non-Stationary | Conflicting |
| CPU | Non-Stationary | Non-Stationary | Needs transformation |
| GPR | Stationary | Stationary | Stationary |

### Hurst Exponent
| Variable | H | Interpretation |
|----------|---|---------------|
| EPU | 0.778 | Strong persistence |
| CPU | 0.804 | Strong persistence |
| GPR | 0.687 | Moderate persistence |

### Tsay Linearity Test
| Variable | Result | Implication |
|----------|--------|------------|
| EPU | Linear | ARIMA sufficient |
| CPU | Nonlinear | ML model needed |
| GPR | Linear | ARIMA sufficient |

### Forecast Results (12-month test set)
| Model | Target | RMSE | MAE | MAPE | R2 |
|-------|--------|------|-----|------|----|
| ARIMAX | EPU | 24.15 | 21.66 | 11.68% | -0.05 |
| SARIMA | EPU | 23.17 | 17.63 | 10.10% | 0.04 |
| ARIMAX | GPR | 11.30 | 8.38 | 6.67% | 0.11 |
| SARIMA | GPR | 9.40 | 7.32 | 6.19% | 0.39 |
| ARIMAX | CPU | 58.71 | 45.14 | 135.60% | 0.03 |

---

## Setup

```bash
git clone https://github.com/aarushiksharmads/PolicyUncertainty-Thesis.git
cd epu-thesis
pip install -r requirements.txt
jupyter notebook
```
---

## Data Sources

- Baker, Bloom and Davis (2016). Measuring economic policy uncertainty. QJE 131(4).
- Gavriilidis (2021). Measuring climate policy uncertainty. SSRN 3847388.
- Federal Reserve Bank of St. Louis FRED Database.

---

## Tech Stack

Python 3.11 | pandas | numpy | statsmodels | pmdarima | lightgbm | shap | scikit-learn | matplotlib | seaborn
