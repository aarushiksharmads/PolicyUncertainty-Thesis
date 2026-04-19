import json

def make_nb(cells):
    return {
        'cells': cells,
        'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': '3.11.0'}},
        'nbformat': 4,
        'nbformat_minor': 4
    }

def md(text):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': [text]}

def code(text):
    return {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [text]}

nb1 = make_nb([
    md('# Notebook 1: Data Loading and Preprocessing'),
    code('import pandas as pd\nimport numpy as np\nfrom scipy.stats import boxcox, yeojohnson\nfrom statsmodels.tsa.stattools import adfuller\nimport warnings\nwarnings.filterwarnings("ignore")\nprint("Libraries loaded.")'),
    code('df = pd.read_excel("../data/raw/POLICYUS.xlsx", parse_dates=["Date"], index_col="Date")\nprint(f"Shape: {df.shape}")\nprint(f"Date range: {df.index[0].date()} to {df.index[-1].date()}")'),
    code('print(f"Total missing values: {df.isnull().sum().sum()}")\ndf[["EPU", "CPU", "GPR"]].describe().round(2)'),
    code('non_stationary_cols = [\n    "CPU", "CES0600000007", "HOUST", "HOUSTNE", "HOUSTMW", "HOUSTS", "HOUSTW",\n    "PERMIT", "PERMITNE", "PERMITMW", "PERMITS", "PERMITW", "CAPE", "cred",\n    "credgdp", "capr", "mortg_inc", "mortg", "prfi_gdp", "pip_inc"\n]\n\ndef best_transform(df, columns):\n    df_t = df.copy()\n    log = {}\n    for col in columns:\n        s = df[col].dropna()\n        results = {}\n        if (s > 0).all():\n            results["log"] = adfuller(np.log(s))[1]\n            bc, _ = boxcox(s)\n            results["boxcox"] = adfuller(bc)[1]\n        yj, _ = yeojohnson(s)\n        results["yeojohnson"] = adfuller(yj)[1]\n        best = min(results, key=results.get)\n        if results[best] < 0.05:\n            if best == "log":\n                df_t[col] = np.log(df[col])\n            elif best == "boxcox":\n                transformed, _ = boxcox(s)\n                df_t.loc[s.index, col] = transformed\n            elif best == "yeojohnson":\n                transformed, _ = yeojohnson(s)\n                df_t.loc[s.index, col] = transformed\n            log[col] = f"{best} (p={results[best]:.4f})"\n        else:\n            df_t[col] = df[col].diff()\n            log[col] = "differencing"\n    return df_t, log\n\ndf_transformed, transform_log = best_transform(df, non_stationary_cols)\ndf_transformed = df_transformed.dropna()\nprint("Transformations applied:")\nfor col, method in transform_log.items():\n    print(f"  {col}: {method}")'),
    code('df_transformed.to_csv("../data/processed/df_transformed.csv")\nprint(f"Saved. Shape: {df_transformed.shape}")')
])

with open('notebooks/01_data_loading_preprocessing.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb1, f, indent=1)
print('Done.')
