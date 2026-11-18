"""
Additional analyses for the revision (BMC Geriatrics, ADRD dysphagia clustering).

Reproduces Supplementary Tables 1, 4, 5 and 6, the permutation test of the
feature selection, the collinearity check of the selected features and the
robustness check with age and Barthel Index in the candidate pool.

Usage:
    python revision_analyses.py data.xlsx [n_permutations]

n_permutations defaults to 999. All analyses use the corrected dataset
(LfdNr 326 and 363).
"""
import sys
import itertools
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.impute import SimpleImputer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, recall_score

warnings.filterwarnings("ignore")

DATA = sys.argv[1]
N_PERM = int(sys.argv[2]) if len(sys.argv) > 2 else 999
SEED = 42

# 11 expert-defined candidate features (Table 2)
POOL = [
    "Spontanschluck",             # spontaneous swallow (30 s rest)
    "Oral_Phase_Mehrere_dich",    # prolonged pre-pharyngeal transit
    "Leaking_any_liquids",        # premature spillage
    "Swallow_Reflex",             # delayed pharyngeal swallow initiation >= 3 s
    "Trigger_spaet",              # swallow onset piriform sinus, coding A
    "Trigger_kaudal_any_neu",     # swallow onset piriform sinus, coding B
    "Whiteout_dich",              # reduced white-out intensity
    "Nachschluck_any2_ohneBrot",  # repetitive swallowing
    "Residue_Sinus_Y2",           # piriform sinus residue
    "Komplex_dich_A",             # complex pattern
    "SehrKomplex_dich_A",         # super-complex pattern
]
# selected subset (highest ARI)
BEST = [
    "Nachschluck_any2_ohneBrot",
    "Residue_Sinus_Y2",
    "Oral_Phase_Mehrere_dich",
    "Swallow_Reflex",
    "Whiteout_dich",
]
COVARIATES = ["Alter_in_Jahren", "BarthelIndexbeiAufnahme", "Sex", "PD", "stroke"]


def header(title):
    print("\n" + "=" * 78 + "\n" + title + "\n" + "=" * 78)


def two_clusters(X):
    """Ward linkage, Euclidean distance, two clusters."""
    return AgglomerativeClustering(n_clusters=2, linkage="ward").fit(X).labels_


def ari_binary(P, yv):
    """Adjusted Rand index of each row of the 0/1 partition matrix P with binary yv
    (identical to sklearn's adjusted_rand_score, vectorized for speed)."""
    n = len(yv)
    comb2 = lambda x: x * (x - 1) / 2
    n11 = P @ yv
    a1 = P.sum(1)
    b1 = yv.sum()
    cells = np.stack([n11, a1 - n11, b1 - n11, n - a1 - b1 + n11])
    s_ij = comb2(cells).sum(0)
    s_a = comb2(a1) + comb2(n - a1)
    s_b = comb2(b1) + comb2(n - b1)
    exp = s_a * s_b / comb2(n)
    return (s_ij - exp) / ((s_a + s_b) / 2 - exp)


def nagelkerke(m):
    n, l1, l0 = m.nobs, m.llf, m.llnull
    cs = 1 - np.exp(2 * (l0 - l1) / n)
    return cs / (1 - np.exp(2 * l0 / n))


raw = pd.read_excel(DATA)
# mode imputation of the few missing feature values (<= 2 per feature)
imp = pd.DataFrame(
    SimpleImputer(strategy="most_frequent").fit_transform(raw), columns=raw.columns
).astype(float)
y = (imp["Group"] - 1).astype(int)  # 0 = no dementia, 1 = dementia
# Nebendiagnose: 1 = history of stroke, 2 = mild Parkinson's disease
imp["stroke"] = (raw["Nebendiagnose"] == 1).astype(float)
imp["PD"] = (raw["Nebendiagnose"] == 2).astype(float)

# ---------------------------------------------------------------------------
header("Supplementary Table 1: univariable logistic regression, 11 candidates")
# observed (non-imputed) values
rows = []
for f in POOL:
    dd = raw[[f, "Group"]].dropna()
    m = sm.Logit(dd["Group"] - 1, sm.add_constant(dd[[f]])).fit(disp=0)
    ci = np.exp(m.conf_int().loc[f])
    rows.append([f, len(dd), m.params[f], m.pvalues[f], np.exp(m.params[f]), ci[0], ci[1]])
print(pd.DataFrame(rows, columns=["feature", "n", "B", "p", "OR", "CI_lo", "CI_hi"])
      .round(3).to_string(index=False))

# ---------------------------------------------------------------------------
header("Supplementary Table 4: multivariable model of the five selected features")
Xb = sm.add_constant(imp[BEST])
m4 = sm.Logit(y, Xb).fit(disp=0)
ci = np.exp(m4.conf_int())
print(pd.DataFrame({"B": m4.params, "SE": m4.bse, "OR": np.exp(m4.params),
                    "CI_lo": ci[0], "CI_hi": ci[1], "p": m4.pvalues}).round(3).to_string())
pred = (m4.predict(Xb) >= 0.5).astype(int)
print(f"Nagelkerke R2 = {nagelkerke(m4):.3f}")
print(f"In-sample sensitivity {recall_score(y, pred):.2f}, "
      f"specificity {recall_score(y, pred, pos_label=0):.2f} (threshold 0.5)")

header("Collinearity of the selected features (variance inflation factors)")
for i, c in enumerate(Xb.columns):
    if c != "const":
        print(f"{c:28s} VIF {variance_inflation_factor(Xb.values, i):.2f}")

# ---------------------------------------------------------------------------
header("Supplementary Table 5: each feature adjusted for age, Barthel, sex, PD, stroke")
cc = imp.copy()
cc["BarthelIndexbeiAufnahme"] = raw["BarthelIndexbeiAufnahme"]  # no imputation
cc = cc[raw["BarthelIndexbeiAufnahme"].notna().values]
print(f"complete cases n = {len(cc)}")
rows = []
for f in BEST:
    yc = cc["Group"] - 1
    mc = sm.Logit(yc, sm.add_constant(cc[[f]])).fit(disp=0)
    ma = sm.Logit(yc, sm.add_constant(cc[[f] + COVARIATES])).fit(disp=0)
    cic, cia = np.exp(mc.conf_int().loc[f]), np.exp(ma.conf_int().loc[f])
    rows.append([f, f"{np.exp(mc.params[f]):.2f} ({cic[0]:.2f}-{cic[1]:.2f})",
                 f"{np.exp(ma.params[f]):.2f} ({cia[0]:.2f}-{cia[1]:.2f})",
                 round(ma.pvalues[f], 4)])
print(pd.DataFrame(rows, columns=["feature", "crude OR (95% CI)",
                                  "adjusted OR (95% CI)", "p adjusted"]).to_string(index=False))

# ---------------------------------------------------------------------------
header("Supplementary Table 6: sensitivity analyses (PD, stroke, both excluded)")
lab_full = two_clusters(imp[BEST].values)
subsets = {
    "excluding mild PD": imp["PD"] == 0,
    "excluding history of stroke": imp["stroke"] == 0,
    "excluding both": (imp["PD"] == 0) & (imp["stroke"] == 0),
}
for name, mask in subsets.items():
    mask = mask.values
    ys = y.values[mask]
    ari_orig = adjusted_rand_score(ys, lab_full[mask])
    ari_new = adjusted_rand_score(ys, two_clusters(imp.loc[mask, BEST].values))
    print(f"{name:30s} n = {mask.sum():3d} (dementia {ys.sum():3d})  "
          f"original assignment ARI {ari_orig:.3f}  re-clustering ARI {ari_new:.3f}")

# ---------------------------------------------------------------------------
header("Feature selection over all non-empty subsets and permutation test")
combos = [c for r in range(1, len(POOL) + 1) for c in itertools.combinations(POOL, r)]
parts = np.array([two_clusters(imp[list(c)].values) for c in combos])  # subsets x patients
aris = ari_binary(parts, y.values)
assert np.allclose(aris, [adjusted_rand_score(y, p) for p in parts])  # check vs sklearn
obs = aris.max()
print(f"{len(combos)} subsets, best ARI {obs:.4f}: {combos[int(aris.argmax())]}")

# dementia status is permuted, the full selection is repeated in each permutation.
# The cluster partitions do not depend on dementia status and are computed once.
rng = np.random.default_rng(SEED)
null = np.empty(N_PERM)
for i in range(N_PERM):
    null[i] = ari_binary(parts, rng.permutation(y.values)).max()
p_perm = (1 + (null >= obs).sum()) / (1 + N_PERM)
print(f"{N_PERM} permutations: mean max ARI {null.mean():.3f}, "
      f"95th percentile {np.quantile(null, 0.95):.3f}, p = {p_perm:.4f}")

# ---------------------------------------------------------------------------
header("Robustness check: age (>= 85) and Barthel (< 60) added to the pool")
pool13 = POOL + ["Alter_dich", "Barthel_dich"]
combos13 = [c for r in range(1, len(pool13) + 1) for c in itertools.combinations(pool13, r)]
aris13 = ari_binary(np.array([two_clusters(imp[list(c)].values) for c in combos13]), y.values)
res = sorted(zip(aris13, combos13), key=lambda t: -t[0])
print(f"best overall ARI {res[0][0]:.4f}: {res[0][1]}")
for cov in ("Alter_dich", "Barthel_dich"):
    best_cov = next(t for t in res if cov in t[1])
    print(f"best subset containing {cov}: ARI {best_cov[0]:.4f} {best_cov[1]}")
