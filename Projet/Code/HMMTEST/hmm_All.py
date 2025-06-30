import os
import warnings
import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib
import argparse
import logging
import matplotlib.pyplot as plt

# Suppress runtime warnings for numerical stability
warnings.filterwarnings("ignore", category=RuntimeWarning)

# -------------------------------------------
# Argument parsing
# -------------------------------------------
parser = argparse.ArgumentParser(
    description="Fit a Gaussian HMM per commune on log-transformed counts with improved convergence"
)
parser.add_argument(
    "--data",
    type=str,
    required=True,
    help="CSV with date index, commune column, raw count column",
)
parser.add_argument(
    "--group_column",
    type=str,
    default="TX_DESCR_FR",
    help="Column for grouping (commune)",
)
parser.add_argument(
    "--count_column",
    type=str,
    default="CASES_PER_10K",
    help="Column with raw counts per 10K",
)
parser.add_argument("--states", type=int, default=5, help="Number of hidden states")
parser.add_argument(
    "--n_init", type=int, default=10, help="Number of random initializations"
)
parser.add_argument(
    "--n_iter", type=int, default=1000, help="Maximum number of EM iterations"
)
parser.add_argument(
    "--tol", type=float, default=1e-3, help="Convergence tolerance for EM"
)
parser.add_argument(
    "--covariance_type",
    type=str,
    default="full",
    choices=["full", "diag", "spherical", "tied"],
    help="Type of covariance for GaussianHMM",
)
parser.add_argument(
    "--output", type=str, default="models/", help="Directory to save outputs"
)
args = parser.parse_args()

# Prepare output directories
os.makedirs(args.output, exist_ok=True)
os.makedirs(os.path.join(args.output, "plots"), exist_ok=True)

# Logging config
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logging.info("Loading dataset into memory")

# -------------------------------------------
# Load and preprocess data
# -------------------------------------------
raw = pd.read_csv(args.data, sep=",", parse_dates=[0], index_col=0)
if args.group_column not in raw.columns or args.count_column not in raw.columns:
    logging.error("Columns not found. Available: %s", list(raw.columns))
    raise KeyError("Invalid group or count column")

# Convert raw counts to float and log-transform
logging.info(
    "Converting '%s' to numeric and applying log1p transform", args.count_column
)
series = pd.to_numeric(
    raw[args.count_column].astype(str).str.replace(",", ""), errors="coerce"
)
raw["log_counts"] = np.log1p(series)

# Group communes
communes = raw[args.group_column].unique()
logging.info("Processing %d communes: %s", len(communes), communes)

# -------------------------------------------
# HMM training per commune with improved initialization and convergence checks
# -------------------------------------------
for commune, df in raw.groupby(args.group_column):
    df = df.sort_index()
    logging.info("---\nCommune: %s (%d records)", commune, len(df))
    data = df["log_counts"].dropna().values.reshape(-1, 1)
    n = len(data)
    if n < args.states * 2:
        logging.warning(
            "Skipping %s: insufficient data (%d) for %d states", commune, n, args.states
        )
        continue

    # Split 70/30
    split = int(n * 0.7)
    X_train, X_test = data[:split], data[split:]
    logging.info("Train: %d obs, Test: %d obs", len(X_train), len(X_test))

    # Scale data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    best_score, best_model = -np.inf, None
    # Initialization and EM
    for seed in range(args.n_init):
        # KMeans for means initialization
        kmeans = KMeans(n_clusters=args.states, random_state=seed).fit(X_train_scaled)
        model = GaussianHMM(
            n_components=args.states,
            covariance_type=args.covariance_type,
            n_iter=args.n_iter,
            tol=args.tol,
            init_params="mc",
            params="stmc",
            random_state=seed,
            verbose=False,
        )
        model.means_init = kmeans.cluster_centers_
        # Initialize covars to sample covariances
        model.covars_init = np.array(
            [
                np.cov(X_train_scaled[kmeans.labels_ == i].T) + 1e-2 * np.eye(1)
                for i in range(args.states)
            ]
        )
        try:
            model.fit(X_train_scaled)
        except Exception as e:
            logging.warning("EM fit failed init %d for %s: %s", seed, commune, e)
            continue
        # Check convergence
        if not getattr(model.monitor_, "converged", True):
            logging.warning("Init %d did not converge for %s", seed, commune)
            continue
        # Score on test
        try:
            score = model.score(X_test_scaled)
        except Exception as e:
            logging.warning("Scoring failed init %d for %s: %s", seed, commune, e)
            continue
        logging.info("Init %d converged; Test LL=%.3f", seed, score)
        if score > best_score:
            best_score, best_model = score, model

    if best_model is None:
        logging.error("No converged model for %s", commune)
        continue

    # Save best model
    model_file = os.path.join(args.output, f"hmm_{commune}.pkl")
    joblib.dump((best_model, scaler), model_file)
    logging.info("Saved model+scaler for %s: %s", commune, model_file)

    # Save transition matrix
    trans_file = os.path.join(args.output, f"transmat_{commune}.csv")
    header = ",".join([f"S{i}" for i in range(args.states)])
    np.savetxt(
        trans_file, best_model.transmat_, delimiter=",", header=header, comments=""
    )
    logging.info("Saved transition matrix for %s: %s", commune, trans_file)

    # Predict on test
    states = best_model.predict(X_test_scaled)
    # Plot on original counts
    plt.figure(figsize=(10, 4))
    dates_test = df.index[split:]
    plt.plot(dates_test, X_test.flatten(), label="Log counts (test)")
    plt.step(dates_test, states, where="post", label="States", color="orange")
    plt.title(f"{commune} - GaussianHMM states")
    plt.legend()
    plot_file = os.path.join(args.output, "plots", f"{commune}_hmm.png")
    plt.savefig(plot_file)
    plt.close()
    logging.info("Saved plot for %s: %s", commune, plot_file)

logging.info("All communes processed")
