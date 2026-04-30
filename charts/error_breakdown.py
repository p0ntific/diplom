"""Инверсия bias: распределение ошибок по типам у разных моделей.

На benchmark-combined (500 примеров):
- baseline: все 57 ошибок = TAG→GEO (модель «всегда GEO»)
- synthetic-обучение: преимущественно GEO→TAG
- mixed_500: симметрия, минимум ошибок
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

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

models = [
    "pro_baseline",
    "train_synth_50",
    "train_synth_500",
    "train_real_250",
    "train_mixed_500",
]
geo_to_tag = [0, 19, 8, 1, 0]
tag_to_geo = [57, 4, 1, 21, 1]
no_pred = [34, 2, 2, 2, 2]

x = np.arange(len(models))
w = 0.26

fig, ax = plt.subplots(figsize=(11, 6))

b1 = ax.bar(x - w, geo_to_tag, w, color=SPBGU_BLUE, label="GEO -> TAG", edgecolor=BG, linewidth=1.2)
b2 = ax.bar(x, tag_to_geo, w, color=SPBGU_RED, label="TAG -> GEO", edgecolor=BG, linewidth=1.2)
b3 = ax.bar(
    x + w,
    no_pred,
    w,
    color=SPBGU_YELLOW,
    label=r"нет tool_call ($\rho_\varnothing$)",
    edgecolor=BG,
    linewidth=1.2,
)

for bars in (b1, b2, b3):
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + 0.6,
                str(int(h)),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=DARK,
            )

ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=11)
ax.set_ylabel("Число ошибок (из 500)", fontsize=12)
ax.set_title(
    "Анализ ошибок: инверсия bias после дообучения",
    fontsize=14,
    fontweight="bold",
    pad=14,
)
ax.legend(frameon=True, facecolor=BG, edgecolor=SPBGU_GRAY, fontsize=11)
ax.set_ylim(0, max(max(geo_to_tag), max(tag_to_geo), max(no_pred)) + 12)
ax.grid(axis="y", color=SPBGU_GRAY, alpha=0.25)

# Подпись о смысле
ax.text(
    0.5,
    -0.18,
    "Базовая модель всегда выбирает GEO (57/57 ошибок) — после дообучения bias переворачивается, "
    "а mixed_500 устраняет асимметрию",
    transform=ax.transAxes,
    ha="center",
    va="top",
    fontsize=10.5,
    color=SPBGU_GRAY,
    style="italic",
)

plt.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "error_breakdown.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
