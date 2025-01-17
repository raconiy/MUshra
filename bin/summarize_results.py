#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Sumamrize MOS evaluation results."""

import numpy as np
import pandas as pd

from scipy.stats import t


result_csv = "~/results/subjective_evalaution/lss.csv"
methods = [
    "ground_truth_1f1m",
    "ground_truth_2females",
    "ground_truth_2males",
    "baseline_tf_1f1m",
    "our_method_1f1m",
    "baseline_tf_2females",
    "our_method_2females",
    "baseline_tf_2males",
    "our_method_2males",
]
gt_method = "ground_truth"
thres = 3
num_acceptable_utts = 3
result = pd.read_csv(result_csv)

# check evaluator
spks = result["name"][
    (result["stimuli_rating"] <= thres) & (result["trial_id"].str.contains(gt_method))
]
unique_spks = list(set(spks.values.tolist()))
remove_indexes = pd.Index([])
for spk in unique_spks:
    if sum(spks == spk) > num_acceptable_utts:
        print(f"{spk} is removed.")
        remove_indexes = remove_indexes.append(result[result["name"] == spk].index)

result_clean = result.drop(remove_indexes)

print(f"Number of scores = {len(result_clean)}")
print("---------- raw results ----------")
for method in methods:
    scores = result[result["trial_id"].str.contains(method)]["stimuli_rating"].values
    mu = np.mean(scores)
    var = np.var(scores, ddof=1)
    conf_bottom, conf_up = t.interval(
        alpha=0.95,
        loc=mu,
        scale=np.sqrt(var / len(scores)),
        df=len(scores) - 1,
    )
    confidence = (conf_up - conf_bottom) / 2
    print(f"{method}: {mu:.2f} ± {confidence:.2f} (#samples={len(scores)})")

print("-------- cleaned results --------")
for method in methods:
    scores = result_clean[result_clean["trial_id"].str.contains(method)][
        "stimuli_rating"
    ].values
    mu = np.mean(scores)
    var = np.var(scores, ddof=1)
    conf_bottom, conf_up = t.interval(
        alpha=0.95,
        loc=mu,
        scale=np.sqrt(var / len(scores)),
        df=len(scores) - 1,
    )
    confidence = (conf_up - conf_bottom) / 2
    print(f"{method}: {mu:.2f} ± {confidence:.2f} (#samples={len(scores)})")
