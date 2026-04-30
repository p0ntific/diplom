import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spbgu_palette import (  # noqa: E402
    BG,
    DARK,
    SPBGU_BLUE,
    SPBGU_GRAY,
    SPBGU_RED,
    SPBGU_SLATE,
    apply_spbgu_style,
)

apply_spbgu_style()

# benchmark-combined: (model, ER, CI lo, CI hi) в долях. Отсортировано по ER возрастанию.
models_data = [
    ("train_mixed_500", 0.006, 0.000, 0.014),
    ("lite_latest_v2", 0.016, 0.006, 0.028),
    ("lite_rc_v1", 0.020, 0.008, 0.034),
    ("train_synth_500", 0.022, 0.010, 0.036),
    ("lite_rc_v2", 0.026, 0.012, 0.042),
    ("lite_latest_v3", 0.034, 0.018, 0.050),
    ("train_synth_1000", 0.044, 0.026, 0.062),
    ("train_real_250", 0.048, 0.030, 0.068),
    ("train_synth_50", 0.054, 0.036, 0.074),
    ("train_synth_250", 0.054, 0.036, 0.074),
    ("lite_latest_v1", 0.072, 0.052, 0.096),
    ("pro_baseline", 0.182, 0.148, 0.216),
]

names = [d[0] for d in models_data]
err = [d[1] for d in models_data]
ci_lo = [d[2] for d in models_data]
ci_hi = [d[3] for d in models_data]
err_lo = [a - lo for a, lo in zip(err, ci_lo)]
err_hi = [hi - a for a, hi in zip(err, ci_hi)]


def _color(name: str) -> str:
    if name == "train_mixed_500":
        return SPBGU_BLUE
    if name == "pro_baseline":
        return SPBGU_RED
    if name.startswith("train_synth"):
        return SPBGU_SLATE
    return SPBGU_GRAY


fig, axes = plt.subplots(2, 6, figsize=(18, 8), sharey=True)
fig.suptitle(
    "Error rate моделей с 95% bootstrap-CI — benchmark-combined (500 запросов)",
    fontsize=15,
    fontweight="bold",
    color=DARK,
    y=0.98,
)

for idx, ax in enumerate(axes.flat):
    name = names[idx]
    a = err[idx]
    color = _color(name)
    ax.bar(0, a, width=0.6, color=color, edgecolor=BG, linewidth=1.5)
    ax.errorbar(
        0,
        a,
        yerr=[[err_lo[idx]], [err_hi[idx]]],
        fmt="none",
        ecolor=DARK,
        elinewidth=1.8,
        capsize=8,
        capthick=1.8,
    )

    label_color = SPBGU_BLUE if name == "train_mixed_500" else DARK
    ax.text(
        0,
        a + err_hi[idx] + 0.008,
        f"{a * 100:.1f}%",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color=label_color,
    )
    ax.text(
        0,
        0.288,
        f"[{ci_lo[idx] * 100:.1f}–{ci_hi[idx] * 100:.1f}]",
        ha="center",
        va="top",
        fontsize=9,
        color=DARK,
        fontweight="bold",
    )

    label = name.replace("_", "\n")
    ax.set_xlabel(label, fontsize=10, color=DARK, labelpad=8, fontweight="bold")
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(0.0, 0.30)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color(SPBGU_GRAY)
    ax.grid(axis="y", color=SPBGU_GRAY, alpha=0.2)
    ax.axhline(y=0.10, color=SPBGU_RED, linestyle="--", alpha=0.4, linewidth=1)

axes[0, 0].set_ylabel("Error rate", fontsize=12)
axes[1, 0].set_ylabel("Error rate", fontsize=12)

plt.tight_layout(rect=[0, 0, 1, 0.92])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accuracy_ci.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
