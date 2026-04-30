import os
import sys

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

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

fig = plt.figure(figsize=(12, 7))
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.35)

ax_bars = fig.add_subplot(gs[0])
ax_bottom = fig.add_subplot(gs[1])

fig.suptitle(
    "Валидация на реальных данных: рост error rate",
    fontsize=15,
    fontweight="bold",
    color=DARK,
    y=0.97,
)

# Error rate в %.
models = ["pro_baseline", "train_synth_250", "lite_latest_v2", "train_mixed_500"]
combined = [18.2, 5.4, 1.6, 0.6]
real = [17.2, 10.8, 3.2, 1.2]
gaps = [r - c for r, c in zip(real, combined)]

x = np.arange(len(models))
w = 0.32

b1 = ax_bars.bar(
    x - w / 2,
    combined,
    w,
    label="benchmark-combined",
    color=SPBGU_SLATE,
    edgecolor=BG,
    linewidth=1.5,
)
b2 = ax_bars.bar(
    x + w / 2,
    real,
    w,
    label="benchmark-real",
    color=SPBGU_BLUE,
    edgecolor=BG,
    linewidth=1.5,
)

for bar in b1:
    h = bar.get_height()
    ax_bars.text(
        bar.get_x() + bar.get_width() / 2,
        h + 0.25,
        f"{h:.1f}",
        ha="center",
        va="bottom",
        fontsize=11,
        color=DARK,
        fontweight="bold",
    )
for bar in b2:
    h = bar.get_height()
    ax_bars.text(
        bar.get_x() + bar.get_width() / 2,
        h + 0.25,
        f"{h:.1f}",
        ha="center",
        va="bottom",
        fontsize=11,
        color=SPBGU_BLUE,
        fontweight="bold",
    )

for i in range(len(models)):
    gap = gaps[i]
    sign = "+" if gap >= 0 else ""
    top = max(combined[i], real[i]) + 1.7
    color = SPBGU_RED if gap > 1.6 else SPBGU_BLUE
    ax_bars.text(
        x[i],
        top,
        f"{sign}{gap:.1f} п.п.",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color=color,
    )

ax_bars.set_xticks(x)
ax_bars.set_xticklabels(models, fontsize=11)
ax_bars.set_ylabel("Error rate, %", fontsize=12)
ax_bars.set_ylim(0, max(real) + 5)
ax_bars.legend(frameon=True, facecolor=BG, edgecolor=SPBGU_GRAY, fontsize=10, loc="upper right")
ax_bars.grid(axis="y", color=SPBGU_GRAY, alpha=0.25)

ax_bottom.axis("off")

ax_bottom.text(
    0.25,
    0.65,
    "+0.6 п.п.",
    ha="center",
    va="center",
    fontsize=34,
    fontweight="bold",
    color=SPBGU_BLUE,
    transform=ax_bottom.transAxes,
)
ax_bottom.text(
    0.25,
    0.25,
    "train_mixed_500 — минимальный gap",
    ha="center",
    va="center",
    fontsize=11,
    color=SPBGU_BLUE,
    transform=ax_bottom.transAxes,
)

ax_bottom.plot(
    [0.5, 0.5],
    [0.1, 0.9],
    transform=ax_bottom.transAxes,
    color=SPBGU_GRAY,
    linewidth=1,
    alpha=0.5,
)

ax_bottom.text(
    0.75,
    0.65,
    "+5.4 п.п.",
    ha="center",
    va="center",
    fontsize=34,
    fontweight="bold",
    color=SPBGU_RED,
    transform=ax_bottom.transAxes,
)
ax_bottom.text(
    0.75,
    0.25,
    "train_synth_250 — максимальный рост error rate",
    ha="center",
    va="center",
    fontsize=11,
    color=SPBGU_RED,
    transform=ax_bottom.transAxes,
)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generalization_gap.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
