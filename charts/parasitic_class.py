"""Confusion matrix для train_synth_50 на benchmark-combined.

Иллюстрирует «паразитный» класс GetSearchQuerySummary, объясняющий разрыв
accuracy = 0.946 vs Macro F1 = 0.631.
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

# Из artifacts/evaluations/train_synthetic_50--benchmark-combined.json
labels = ["GetSearchQuery\nSummary", "ResolveEntities\n(GEO)", "SearchTags\n(TAG)"]
matrix = np.array(
    [
        [0, 0, 0],
        [1, 304, 19],
        [1, 4, 169],
    ]
)

fig, ax = plt.subplots(figsize=(8.5, 6))

# Базовая тёплая заливка
ax.imshow(matrix, cmap="Blues", aspect="auto", vmin=0, vmax=320)

# Подсветка паразитного класса (первая строка / первый столбец)
ax.add_patch(
    plt.Rectangle((-0.5, -0.5), 3, 1, fill=False, edgecolor=SPBGU_RED, linewidth=2.6)
)
ax.add_patch(
    plt.Rectangle((-0.5, -0.5), 1, 3, fill=False, edgecolor=SPBGU_RED, linewidth=2.6)
)

for i in range(3):
    for j in range(3):
        v = matrix[i, j]
        text_color = "white" if v > 100 else DARK
        ax.text(
            j,
            i,
            str(v),
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
            color=text_color,
        )

ax.set_xticks(range(3))
ax.set_xticklabels(labels, fontsize=11)
ax.set_yticks(range(3))
ax.set_yticklabels(labels, fontsize=11)
ax.set_xlabel("Предсказанный класс", fontsize=13, fontweight="bold")
ax.set_ylabel("Истинный класс", fontsize=13, fontweight="bold")
ax.set_title(
    "train_synth_50 на benchmark-combined: «паразитный» класс",
    fontsize=14,
    fontweight="bold",
    pad=14,
)
ax.grid(False)

# Аннотация справа
ax.text(
    1.06,
    0.95,
    "accuracy = 0.946\nMacro F1 = 0.631",
    transform=ax.transAxes,
    fontsize=12,
    fontweight="bold",
    va="top",
    color=DARK,
    bbox=dict(boxstyle="round,pad=0.4", facecolor=BG, edgecolor=SPBGU_GRAY),
)
ax.text(
    1.06,
    0.65,
    "F1 третьего класса = 0\n(support = 0)\nmacro-усреднение\nпо 3 лейблам",
    transform=ax.transAxes,
    fontsize=11,
    va="top",
    color=SPBGU_RED,
    bbox=dict(boxstyle="round,pad=0.4", facecolor=BG, edgecolor=SPBGU_RED),
)

plt.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parasitic_class.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
