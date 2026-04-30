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
    SPBGU_SLATE,
    apply_spbgu_style,
)

apply_spbgu_style()

# ── Данные benchmark-combined: (имя, error rate, Macro F1, число ошибок) ──
# Error rate отсортирован по возрастанию (лучшие сверху).
models = [
    ("train_mixed_500", 0.006, 0.9962, 3),
    ("lite_latest_v2", 0.016, 0.9853, 8),
    ("lite_rc_v1", 0.020, 0.9807, 10),
    ("train_synthetic_500", 0.022, 0.9788, 11),
    ("lite_rc_v2", 0.026, 0.9741, 13),
    ("lite_latest_v3", 0.034, 0.9657, 17),
    ("train_synthetic_1000", 0.044, 0.9553, 22),
    ("train_real_250", 0.048, 0.9486, 24),
    ("train_synthetic_50", 0.054, 0.6309, 27),
    ("train_synthetic_250", 0.054, 0.9447, 27),
    ("lite_latest_v1", 0.072, 0.9247, 36),
    ("pro_baseline", 0.182, 0.526, 91),
]

names = [m[0] for m in models]
err_pct = [m[1] * 100 for m in models]
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
        return SPBGU_SLATE
    return SPBGU_GRAY


bar_colors = [_color(n) for n in names]

bars = ax1.barh(y, err_pct, color=bar_colors, edgecolor=BG, height=0.66)
for bar, e_pct, e_n in zip(bars, err_pct, errors):
    ax1.text(
        bar.get_width() + 0.25,
        bar.get_y() + bar.get_height() / 2,
        f"{e_pct:.1f}%  ({e_n} ош.)",
        va="center",
        fontsize=11,
        fontweight="bold",
        color=DARK,
    )

ax1.set_yticks(y)
ax1.set_yticklabels(names, fontsize=11)
ax1.set_xlim(0, 22)
ax1.set_xlabel("Error rate, %", fontsize=12)
ax1.invert_yaxis()
ax1.axvline(x=10, color=DARK, linestyle="--", alpha=0.3, linewidth=1)
ax1.text(10.2, -0.5, "цель: $<$10%", fontsize=9, color=DARK, alpha=0.7)

legend_items = [
    Patch(facecolor=SPBGU_RED, label="baseline (Pro)"),
    Patch(facecolor=SPBGU_SLATE, label="чистая синтетика"),
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
    ax2.text(val - 0.012, y[i], f"{val:.3f}", va="center", ha="right", fontsize=10, color=DARK)

ax2.set_yticks(y)
ax2.set_yticklabels([""] * len(y))
ax2.set_xlim(0.45, 1.08)
ax2.set_xlabel("Macro F1", fontsize=12)
ax2.invert_yaxis()
ax2.axvline(x=0.85, color=DARK, linestyle="--", alpha=0.3, linewidth=1)
ax2.text(0.855, -0.5, "цель: 0.85", fontsize=9, color=DARK, alpha=0.7)

plt.tight_layout(rect=[0, 0, 1, 0.94])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_comparison.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
