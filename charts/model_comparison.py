import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

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

# ── Данные (benchmark-combined, sorted by accuracy) ──
models = [
    ("pro_baseline", 0.818, 0.526, 57),
    ("lite_latest_v1", 0.928, 0.9247, 34),
    ("train_synthetic_50", 0.946, 0.6309, 25),
    ("train_synthetic_250", 0.946, 0.9447, 25),
    ("train_real_250", 0.952, 0.9486, 22),
    ("train_synthetic_1000", 0.956, 0.9553, 20),
    ("lite_latest_v3", 0.966, 0.9657, 15),
    ("lite_rc_v2", 0.974, 0.9741, 11),
    ("train_synthetic_500", 0.978, 0.9788, 9),
    ("lite_rc_v1", 0.980, 0.9807, 8),
    ("lite_latest_v2", 0.984, 0.9853, 6),
    ("train_mixed_500", 0.994, 0.9962, 1),
]

names = [m[0] for m in models]
acc = [m[1] * 100 for m in models]
f1 = [m[2] for m in models]
errors = [m[3] for m in models]

y = np.arange(len(names))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={"width_ratios": [3, 1]})
fig.suptitle(
    "Сравнение моделей — benchmark-combined (500 примеров)",
    fontsize=16,
    fontweight="bold",
    color=DARK,
    y=0.97,
)


def _color(name: str) -> str:
    if name == "train_mixed_500":
        return SPBGU_BLUE
    if name == "pro_baseline":
        return SPBGU_RED
    if name.startswith("train_synthetic"):
        return SPBGU_YELLOW
    return SPBGU_GRAY


bar_colors = [_color(n) for n in names]

bars = ax1.barh(y, acc, color=bar_colors, edgecolor=BG, height=0.66)
for bar, a, e in zip(bars, acc, errors):
    ax1.text(
        bar.get_width() + 0.3,
        bar.get_y() + bar.get_height() / 2,
        f"{a:.1f}%  ({e} ош.)",
        va="center",
        fontsize=11,
        fontweight="bold",
        color=DARK,
    )

ax1.set_yticks(y)
ax1.set_yticklabels(names, fontsize=11)
ax1.set_xlim(75, 105)
ax1.set_xlabel("Accuracy, %", fontsize=12)
ax1.invert_yaxis()
ax1.axvline(x=90, color=DARK, linestyle="--", alpha=0.3, linewidth=1)
ax1.text(90.3, -0.6, "цель: 90%", fontsize=9, color=DARK, alpha=0.6)

legend_items = [
    Patch(facecolor=SPBGU_RED, label="baseline (Pro)"),
    Patch(facecolor=SPBGU_YELLOW, label="чистая синтетика"),
    Patch(facecolor=SPBGU_GRAY, label="прочие конфигурации"),
    Patch(facecolor=SPBGU_BLUE, label="best: mixed_500"),
]
ax1.legend(
    handles=legend_items,
    loc="lower right",
    frameon=True,
    facecolor=BG,
    edgecolor=SPBGU_GRAY,
    fontsize=10,
)

ax2.scatter(f1, y, color=bar_colors, s=120, edgecolors=DARK, linewidths=1.2, zorder=5)
for i, val in enumerate(f1):
    ax2.text(val + 0.012, y[i], f"{val:.3f}", va="center", fontsize=10, color=DARK)

ax2.set_yticks(y)
ax2.set_yticklabels([""] * len(y))
ax2.set_xlim(0.45, 1.08)
ax2.set_xlabel("Macro F1", fontsize=12)
ax2.invert_yaxis()
ax2.axvline(x=0.85, color=DARK, linestyle="--", alpha=0.3, linewidth=1)
ax2.text(0.855, -0.6, "цель: 0.85", fontsize=9, color=DARK, alpha=0.6)

plt.tight_layout(rect=[0, 0, 1, 0.94])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_comparison.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
