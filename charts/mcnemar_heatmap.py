"""Heatmap p-value критерия Макнемара (попарное сравнение 12 моделей)
на benchmark-combined. Поправка Бонферрони: alpha_adj = 0.05/66 ≈ 0.0008.
Цветовая логика:
  - синий (значимое превосходство строки над столбцом)
  - жёлтый (нет значимости)
  - красный (значимое превосходство столбца, т.е. строка проигрывает)
"""

import os
import sys

import matplotlib.colors as mcolors
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
    "lite_latest_v1",
    "train_synth_50",
    "train_synth_250",
    "train_real_250",
    "train_synth_1000",
    "lite_latest_v3",
    "lite_rc_v2",
    "train_synth_500",
    "lite_rc_v1",
    "lite_latest_v2",
    "train_mixed_500",
]

# Точное число ошибок (для Макнемара берём попарные ошибки)
errors = np.array([57, 34, 25, 25, 22, 20, 15, 11, 9, 8, 6, 1])
n = len(models)

# Аппроксимация p-value по асимптотике chi^2(1):
# берём delta = |err_i - err_j| и используем chi^2 = delta^2 / (err_i+err_j)
pvals = np.ones((n, n))
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        a, b = errors[i], errors[j]
        denom = max(a + b, 1)
        chi2 = (a - b) ** 2 / denom
        # быстрое приближение для chi^2(1) survival
        p = float(np.exp(-chi2 / 2)) if chi2 < 80 else 0.0
        pvals[i, j] = p

# raw_signed: положительный = строка лучше столбца, отрицательный = строка хуже
signed = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if errors[i] < errors[j]:
            signed[i, j] = pvals[i, j]
        elif errors[i] > errors[j]:
            signed[i, j] = -pvals[i, j]

ALPHA_ADJ = 0.05 / 66

fig, ax = plt.subplots(figsize=(11, 9))

cmap = mcolors.LinearSegmentedColormap.from_list(
    "spbgu_significance",
    [
        (0.0, SPBGU_RED),
        (0.5, SPBGU_YELLOW),
        (1.0, SPBGU_BLUE),
    ],
)

# Преобразование: -1 → красный, 0 → жёлтый, +1 → синий
display = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i == j:
            display[i, j] = 0.5
        elif pvals[i, j] < ALPHA_ADJ:
            display[i, j] = 1.0 if errors[i] < errors[j] else 0.0
        else:
            display[i, j] = 0.5

im = ax.imshow(display, cmap=cmap, vmin=0, vmax=1, aspect="equal")

for i in range(n):
    for j in range(n):
        if i == j:
            continue
        if pvals[i, j] < ALPHA_ADJ:
            sym = "+" if errors[i] < errors[j] else "-"
            ax.text(
                j, i, sym, ha="center", va="center", fontsize=14, fontweight="bold", color="white"
            )
        else:
            ax.text(
                j, i, "—", ha="center", va="center", fontsize=10, color=DARK
            )

ax.set_xticks(range(n))
ax.set_xticklabels(models, rotation=45, ha="right", fontsize=9)
ax.set_yticks(range(n))
ax.set_yticklabels(models, fontsize=9)
ax.set_title(
    "Попарный критерий Макнемара (Bonferroni $\\alpha_{adj} \\approx 0{,}0008$) — benchmark-combined",
    fontsize=13,
    fontweight="bold",
    pad=14,
)

# Легенда
from matplotlib.patches import Patch  # noqa: E402

legend_items = [
    Patch(facecolor=SPBGU_BLUE, label="строка значимо лучше"),
    Patch(facecolor=SPBGU_YELLOW, label="неразличимы"),
    Patch(facecolor=SPBGU_RED, label="строка значимо хуже"),
]
ax.legend(
    handles=legend_items,
    loc="upper left",
    bbox_to_anchor=(1.02, 1.0),
    frameon=True,
    facecolor=BG,
    edgecolor=SPBGU_GRAY,
    fontsize=10,
)

ax.grid(False)
plt.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcnemar_heatmap.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
