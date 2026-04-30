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
    SPBGU_YELLOW,
    apply_spbgu_style,
)

apply_spbgu_style()

# ── benchmark-real, sorted by accuracy ──
models_data = [
    ("pro_baseline", 0.828, 0.780, 0.876),
    ("train_synth_250", 0.892, 0.852, 0.928),
    ("lite_latest_v1", 0.904, 0.868, 0.940),
    ("train_synth_50", 0.904, 0.868, 0.940),
    ("train_synth_1000", 0.912, 0.872, 0.944),
    ("lite_latest_v3", 0.932, 0.900, 0.960),
    ("lite_rc_v2", 0.944, 0.916, 0.972),
    ("lite_rc_v1", 0.948, 0.920, 0.976),
    ("train_synth_500", 0.956, 0.928, 0.980),
    ("lite_latest_v2", 0.968, 0.944, 0.988),
    ("train_real_250", 0.980, 0.960, 0.996),
    ("train_mixed_500", 0.988, 0.972, 1.000),
]

names = [d[0] for d in models_data]
acc = [d[1] for d in models_data]
ci_lo = [d[2] for d in models_data]
ci_hi = [d[3] for d in models_data]
err_lo = [a - lo for a, lo in zip(acc, ci_lo)]
err_hi = [hi - a for a, hi in zip(acc, ci_hi)]


def _color(name: str) -> str:
    if name == "train_mixed_500":
        return SPBGU_BLUE
    if name == "pro_baseline":
        return SPBGU_RED
    if name.startswith("train_synth"):
        return SPBGU_YELLOW
    return SPBGU_GRAY


fig, axes = plt.subplots(2, 6, figsize=(18, 8), sharey=True)
fig.suptitle(
    "Accuracy моделей с 95% bootstrap-CI — benchmark-real (250 запросов)",
    fontsize=15,
    fontweight="bold",
    color=DARK,
    y=0.98,
)

for idx, ax in enumerate(axes.flat):
    name = names[idx]
    a = acc[idx]
    lo = err_lo[idx]
    hi = err_hi[idx]

    color = _color(name)
    ax.bar(0, a, width=0.6, color=color, edgecolor=BG, linewidth=1.5)
    ax.errorbar(
        0,
        a,
        yerr=[[lo], [hi]],
        fmt="none",
        ecolor=DARK,
        elinewidth=1.8,
        capsize=8,
        capthick=1.8,
    )

    label_color = SPBGU_BLUE if name == "train_mixed_500" else DARK
    ax.text(
        0,
        a + hi + 0.008,
        f"{a * 100:.1f}%",
        ha="center",
        va="bottom",
        fontsize=13,
        fontweight="bold",
        color=label_color,
    )
    ax.text(
        0,
        0.72,
        f"[{ci_lo[idx] * 100:.1f}–{ci_hi[idx] * 100:.1f}]",
        ha="center",
        va="top",
        fontsize=10,
        color=DARK,
        fontweight="bold",
    )

    label = name.replace("_", "\n")
    ax.set_xlabel(label, fontsize=10, color=DARK, labelpad=8, fontweight="bold")
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(0.70, 1.06)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color(SPBGU_GRAY)
    ax.grid(axis="y", color=SPBGU_GRAY, alpha=0.2)

axes[0, 0].set_ylabel("Accuracy", fontsize=12)
axes[1, 0].set_ylabel("Accuracy", fontsize=12)

plt.tight_layout(rect=[0, 0, 1, 0.92])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accuracy_ci.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
