# Expected Goals (xG) Model — ENEL 525 Course Project

**Ali Bayoumi (30144286) · Abdelrahman Salem (30210519)**
ENEL 525 – Machine Learning for Engineers, University of Calgary, Fall 2026

We predict the probability that a soccer shot becomes a goal (expected goals, xG) from information available at the moment of the shot. We compare a constant baseline, a distance-and-angle logistic regression, a single sigmoid neuron implemented from scratch in NumPy (Model A), and a multilayer neural network (Model B), benchmarked against StatsBomb's professional xG model.

## Results (held-out test set, 9,798 shots)

| Model | ROC-AUC [95% CI] | Log loss | Brier |
|---|---|---|---|
| Constant baseline | 0.500 | 0.348 | 0.098 |
| Logistic (distance + angle) | 0.744 [0.729, 0.759] | 0.309 | 0.090 |
| Model A: neuron from scratch | 0.781 [0.766, 0.795] | 0.292 | 0.085 |
| Model B: neural network (32 hidden) | 0.783 [0.768, 0.797] | 0.291 | 0.085 |
| StatsBomb xG (benchmark) | 0.817 [0.802, 0.831] | 0.275 | 0.080 |

Confidence intervals are from 1,000 bootstrap resamples of the test set.

## Data

[StatsBomb Open Data](https://github.com/statsbomb/open-data), loaded with the `statsbombpy` package. We use all free **men's** competitions: 66,854 shots from 2,651 matches (65,822 after removing penalties and shootouts). The data is not stored in this repository; the download script below recreates it.

Data provided by StatsBomb.

## Setup

Requires Python 3.9 or newer.

```
git clone <this-repo-url>
cd <repo-folder>
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
```

## How to run

Run from the repository root, in this order:

1. **Download the data** (about 30–60 minutes; safe to re-run if interrupted):
   ```
   python src/download_shots.py
   ```
   Creates `data/raw/` (one CSV per competition) and `data/shots.csv`.
2. **`notebooks/02_eda.ipynb`**: cleaning, feature engineering (distance, angle), exploratory plots. Creates `data/shots_clean.csv` and figures in `figures/`.
3. **`notebooks/03_models.ipynb`**: match-level train/validation/test split, baselines, Model A, Model B, hyperparameter tuning, final test evaluation, seeds, calibration, ablation and per-competition analysis.

All randomness uses fixed seeds (`SEED = 42`; seeds 0–4 for the repeated-runs experiment).

## Repository structure

```
src/download_shots.py     downloads all shots from StatsBomb open data
notebooks/02_eda.ipynb    cleaning, features, EDA
notebooks/03_models.ipynb modelling and evaluation
figures/                  saved plots and test results
data/                     created by the download script (git-ignored)
requirements.txt          Python dependencies
```
