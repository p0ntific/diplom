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

fig, ax = plt.subplots(figsize=(10, 6))

# ── Данные (error rate, %) ──
synth_sizes = [50, 250, 500, 908]
synth_err = [5.4, 5.4, 2.2, 4.4]

mixed_size = 500
mixed_err = 0.6

# ── Кривая synthetic ──
ax.plot(
    synth_sizes,
    synth_err,
    color=SPBGU_SLATE,
    linewidth=2.8,
    marker="o",
    markersize=11,
    markerfacecolor=SPBGU_SLATE,
    markeredgecolor=DARK,
    markeredgewidth=1.2,
    label="synthetic",
    zorder=3,
)

for x, y in zip(synth_sizes, synth_err):
    ax.annotate(
        f"{y:.1f}%",
        (x, y),
        textcoords="offset points",
        xytext=(0, 14),
        ha="center",
        fontsize=11,
        fontweight="bold",
        color=DARK,
    )

# ── Точка mixed ──
ax.scatter(
    [mixed_size],
    [mixed_err],
    color=SPBGU_BLUE,
    s=240,
    edgecolors=DARK,
    linewidths=1.5,
    zorder=5,
    label="mixed",
)
ax.annotate(
    "0.6%",
    (mixed_size, mixed_err),
    textcoords="offset points",
    xytext=(15, -3),
    ha="left",
    fontsize=14,
    fontweight="bold",
    color=SPBGU_BLUE,
)
ax.annotate(
    "mixed_500",
    (mixed_size, mixed_err),
    textcoords="offset points",
    xytext=(15, -20),
    ha="left",
    fontsize=10,
    color=SPBGU_BLUE,
)

ax.plot([500, 500], [2.2, 0.6], color=SPBGU_BLUE, linestyle=":", linewidth=1.5, alpha=0.6)

ax.set_xlabel("Число обучающих примеров", fontsize=13)
ax.set_ylabel("Error rate, %", fontsize=13)
ax.set_title(
    "Кривая обучения: error rate (synthetic vs mixed)",
    fontsize=15,
    fontweight="bold",
    pad=14,
)
ax.set_xlim(-30, 1000)
ax.set_ylim(-0.6, 7.5)
ax.set_xticks([50, 250, 500, 750, 908])
ax.set_xticklabels(["50", "250", "500", "750", "908"])

ax.text(
    0.5,
    0.94,
    "500 mixed  <  908 synthetic    |    500 mixed  <  best ~1500 synthetic run",
    transform=ax.transAxes,
    ha="center",
    fontsize=11,
    color=SPBGU_RED,
    fontweight="bold",
    style="italic",
    bbox=dict(boxstyle="round,pad=0.4", facecolor=BG, edgecolor=SPBGU_RED, alpha=0.9),
)

ax.legend(loc="upper left", frameon=True, facecolor=BG, edgecolor=SPBGU_GRAY, fontsize=11)

plt.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saturation_curve.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
