"""All numbers, tables and figures of the paper.

    python analyze.py

The script reads the CSV files written by run.py and study2.py and prints every number used in
the paper, in the order of the paper, each labelled with the table or research question it
belongs to. Nothing is fitted or tuned: all results are means of test outcomes (0 or 1) or judge
verdicts, plus standard non-parametric tests from scipy.

Study 1   P_default(r) = share of ABL-r runs (r not in the prompt) that pass the test of r
          P_stated(r)  = share of FULL runs that pass the test of r
          Info(r)      = P_stated(r) - P_default(r)
          Means are taken over requirements, with 95% bootstrap intervals over requirements.
          RQ1: Kruskal-Wallis and pairwise Mann-Whitney (Holm correction) on P_default by category.
          RQ2: Fisher's exact test on failures of stated requirements, P_default <= 0.2 vs the rest.
Erosion   P_survive = share of requirements met by the starting code that are still met after each step.
Study 2   A requirement is met when the majority of judges says so. Answers without code are left out.
          RQ4: Mann-Whitney for D vs T in BARE, Wilcoxon signed-rank for BARE vs FULL.

Reads:   results/main/results.csv          Study 1   (one row per request and requirement)
         results/main/results_erosion.csv  erosion   (one row per chain step and requirement)
         results/main/results_study2.csv Study 2   (one row per answer, requirement and judge)
Writes:  fig_pdefault.pdf, fig_study2.pdf, per_req_study1.csv, per_req_study2.csv
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(0)  # fixed seed: bootstrap intervals are the same on every run


def mean_ci(values):
    """Mean and 95% bootstrap interval: resample the values 5000 times, take the 2.5 and 97.5 percentile."""
    values = np.asarray(values)
    means = [rng.choice(values, len(values)).mean() for _ in range(5000)]
    low, high = np.percentile(means, [2.5, 97.5])
    return f"{values.mean():.2f} [{low:.2f}, {high:.2f}]"


# =============================================================================
# STUDY 1
# =============================================================================
s1 = pd.read_csv("results/main/results.csv")
print("STUDY 1")
print("  models:", sorted(s1.model.unique()), " repetitions:", s1.rep.nunique())

runs = s1.drop_duplicates("json_file")
print("  runs: ABL", (runs.condition != "FULL").sum(), " FULL", (runs.condition == "FULL").sum())
print("  crashed runs per model:", runs.groupby("model").crashed.sum().to_dict())
print("  truncated runs:", runs.truncated.sum(), "  total cost USD:", round(runs.cost_usd.sum(), 2))

# Crashed or truncated runs say nothing about requirements, so they are left out.
ok = s1[(s1.crashed == 0) & (s1.truncated == 0)]

# P_default(r): runs with prompt ABL-r, looking only at requirement r (it was not in the prompt).
ablated = ok[ok.condition.str.startswith("ABL") & (ok.in_prompt == False)]
# P_stated(r): FULL runs (all requirements in the prompt), looking at requirement r.
full = ok[ok.condition == "FULL"]

per_req = pd.DataFrame({
    "category": s1.groupby("req_id").category.first(),
    "P_default": ablated.groupby("req_id").passed.mean(),
    "P_stated": full.groupby("req_id").passed.mean(),
})
per_req["Info"] = per_req.P_stated - per_req.P_default
per_req.round(2).sort_values(["category", "P_default"]).to_csv("per_req_study1.csv")

print("\n  Table 2 (mean over requirements, 95% CI):")
for cat in ["K", "D", "S"]:
    r = per_req[per_req.category == cat]
    print(f"  {cat}  n={len(r):2}  P_default {mean_ci(r.P_default)}  P_stated {mean_ci(r.P_stated)}"
          f"  Info {mean_ci(r.Info)}  never met by default: {(r.P_default == 0).sum()}")

# RQ1: do the categories differ in P_default?
groups = {cat: per_req[per_req.category == cat].P_default for cat in ["K", "D", "S"]}
kw = stats.kruskal(groups["K"], groups["D"], groups["S"])
print(f"\n  RQ1 Kruskal-Wallis: H = {kw.statistic:.1f}, p = {kw.pvalue:.2g}")
pairs = [("K", "D"), ("K", "S"), ("D", "S")]
p_raw = [stats.mannwhitneyu(groups[a], groups[b]).pvalue for a, b in pairs]
# Holm correction: smallest p times 3, next times 2, largest times 1 (and never smaller than the previous one)
order = np.argsort(p_raw)
p_holm, previous = [0.0] * 3, 0.0
for rank, i in enumerate(order):
    previous = max(previous, min(1.0, p_raw[i] * (3 - rank)))
    p_holm[i] = previous
for (a, b), p in zip(pairs, p_holm):
    print(f"  RQ1 Mann-Whitney {a} vs {b}: p (Holm) = {p:.3f}")

# Table 3: per model
print("\n  Table 3, Study 1 part (P_default / P_stated):")
for model in sorted(s1.model.unique()):
    cells = []
    for cat in ["K", "D", "S"]:
        d = ablated[(ablated.model == model) & (ablated.category == cat)].passed.mean()
        s = full[(full.model == model) & (full.category == cat)].passed.mean()
        cells.append(f"{cat} {d:.2f} / {s:.2f}")
    print(f"  {model:9} " + "   ".join(cells))

# RQ2: do failures of stated requirements fall on requirements that are rarely met by default?
print("\n  RQ2 FULL runs that pass every requirement:", round(full.groupby("json_file").passed.min().mean(), 2))
print("  RQ2 requirements not always met when stated:")
print(per_req[per_req.P_stated < 1].round(2).to_string())
full = full.assign(rarely_default=full.req_id.map(per_req.P_default) <= 0.2)
table = pd.crosstab(full.rarely_default, full.passed)  # rows: False/True, columns: 0 (failed) / 1 (passed)
print("  RQ2 2x2 table (rows: P_default <= 0.2, columns: 0 = failed, 1 = passed):")
print(table.to_string())
print(f"  RQ2 Fisher exact test: p = {stats.fisher_exact(table.values).pvalue:.2g}")

# Figure 1
fig, ax = plt.subplots(figsize=(4.7, 2.4))
for x, cat in enumerate(["K", "D", "S"]):
    r = per_req[per_req.category == cat].P_default
    ax.scatter(x + rng.uniform(-0.18, 0.18, len(r)), r, s=14, alpha=0.8)
    low, high = np.percentile([rng.choice(r, len(r)).mean() for _ in range(5000)], [2.5, 97.5])
    ax.errorbar(x + 0.3, r.mean(), yerr=[[r.mean() - low], [high - r.mean()]], fmt="D", color="k", ms=4)
ax.set_xticks(range(3), ["K: convention", "D: domain", "S: stakeholder"])
ax.set_ylabel(r"$P_\mathrm{default}$")
fig.tight_layout()
fig.savefig("fig_pdefault.pdf")

# =============================================================================
# EROSION (RQ3)
# =============================================================================
er = pd.read_csv("results/main/results_erosion.csv")
er["chain"] = er.app + "|" + er.model + "|" + er.variant + "|" + er.rep.astype(str)
# requirements met at step 0 (the starting FULL code) are the ones that can be lost later
met_at_start = er[(er.step == 0) & (er.passed == 1)][["chain", "req_id"]]
later = er[(er.step > 0) & (er.crashed == 0)].merge(met_at_start, on=["chain", "req_id"])
steps = er[er.step > 0].drop_duplicates(["chain", "step"])

print("\nEROSION")
print("  chains per variant:", steps.groupby("variant").chain.nunique().to_dict(),
      " evaluated (code met something at start):", later.groupby("variant").chain.nunique().to_dict())
print("  steps:", len(steps), " crashed steps:", int(steps.crashed.sum()))
print("  P_survive (share of requirements met at start that are still met):")
print(later.pivot_table(index=["variant", "category"], columns="step", values="passed").round(2).to_string())
lost = later[later.passed == 0]
print(f"  lost requirements: {len(lost)}")
if len(lost):
    print(lost.groupby(["variant", "model", "app", "rep", "req_id"]).step.apply(list).to_string())

# =============================================================================
# STUDY 2
# =============================================================================
s2 = pd.read_csv("results/main/results_study2.csv")
print("\nSTUDY 2")
print("  models:", sorted(s2.model.unique()), " judges:", sorted(s2.judge_model.unique()))
answers = s2.drop_duplicates("json_file")
print("  answers:", len(answers))
print("  answers without code (only questions):",
      answers[answers.has_code == 0].groupby(["model", "condition"]).size().to_dict())

# Judges: errors, strictness, agreement
print("  judge returned no verdict (answers):", s2[s2.met.isna()].groupby("judge_model").json_file.nunique().to_dict())
graded = s2[s2.has_code == 1]
print("  share judged met, per judge:", graded.groupby("judge_model").met.mean().round(2).to_dict())
wide = graded.pivot_table(index=["json_file", "req_id"], columns="judge_model", values="met")
judges = list(wide.columns)
for i in range(len(judges)):
    for j in range(i + 1, len(judges)):
        a, b = judges[i], judges[j]
        both = wide[[a, b]].dropna()
        agree = (both[a] == both[b]).mean()
        chance = both[a].mean() * both[b].mean() + (1 - both[a].mean()) * (1 - both[b].mean())
        print(f"  {a} vs {b}: agreement {agree:.2f}, Cohen's kappa {(agree - chance) / (1 - chance):.2f}")
# Self-preference check for a judge that also answers (GPT): how much stricter than the other judges,
# on its own answers and on the other models' answers?
model_of_answer = answers.set_index("json_file").model
for judge in judges:
    if judge in set(answers.model):
        stricter = wide[judge] - wide.drop(columns=judge).mean(axis=1)
        own = model_of_answer.reindex(wide.index.get_level_values("json_file")).values == judge
        print(f"  {judge} as judge minus other judges: own answers {stricter[own].mean():+.2f},"
              f" other answers {stricter[~own].mean():+.2f}")

# A requirement counts as met when the majority of judges says so (2 of 3).
# Missing verdicts are ignored, so with 2 verdicts both must say "met".
votes = graded.groupby(["json_file", "model", "condition", "req_id", "category"]).met.mean().reset_index()
votes["met"] = (votes.met > 0.5).astype(int)

per_req2 = votes.pivot_table(index="req_id", columns="condition", values="met")
per_req2["category"] = votes.groupby("req_id").category.first()
per_req2.round(2).sort_values(["category", "BARE"]).to_csv("per_req_study2.csv")

print("\n  RQ4 (mean over requirements, 95% CI):")
for cat in ["D", "T"]:
    r = per_req2[per_req2.category == cat]
    print(f"  {cat}  n={len(r):2}  BARE {mean_ci(r.BARE)}  FULL {mean_ci(r.FULL)}")
d, t = per_req2[per_req2.category == "D"], per_req2[per_req2.category == "T"]
print(f"  RQ4 Mann-Whitney D vs T in BARE: p = {stats.mannwhitneyu(d.BARE, t.BARE).pvalue:.3f}")
print(f"  RQ4 Wilcoxon BARE vs FULL (same requirements): p = {stats.wilcoxon(per_req2.BARE, per_req2.FULL).pvalue:.2g}")
all_met = votes.groupby(["json_file", "condition"]).met.min().groupby("condition").mean()
print("  RQ4 answers meeting all three requirements:", all_met.round(2).to_dict())
print("  RQ4 never met in BARE:", list(per_req2[per_req2.BARE == 0].index))
print("\n  Table 3, Study 2 part (BARE / FULL):")
for model in sorted(votes.model.unique()):
    v = votes[votes.model == model]
    cells = [f"{cat} {v[(v.condition == 'BARE') & (v.category == cat)].met.mean():.2f} / "
             f"{v[(v.condition == 'FULL') & (v.category == cat)].met.mean():.2f}" for cat in ["D", "T"]]
    print(f"  {model:9} " + "   ".join(cells))

# Figure 2
fig, axes = plt.subplots(1, 2, figsize=(4.8, 3.6), sharex=True)
for ax, cat in zip(axes, ["D", "T"]):
    r = per_req2[per_req2.category == cat].sort_values("BARE")
    y = range(len(r))
    ax.hlines(y, r.BARE, r.FULL, color="#bbb")
    ax.scatter(r.BARE, y, facecolor="white", edgecolor="k", s=18, label="BARE", zorder=3)
    ax.scatter(r.FULL, y, s=18, label="FULL", zorder=3)
    ax.set_yticks(y, r.index, fontsize=6.5)
    ax.set_title(cat)
    ax.set_xlim(-0.05, 1.05)
axes[1].legend(frameon=False)
fig.tight_layout()
fig.savefig("fig_study2.pdf")
print("\nWritten: fig_pdefault.pdf, fig_study2.pdf, per_req_study1.csv, per_req_study2.csv")
