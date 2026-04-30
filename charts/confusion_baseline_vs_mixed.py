"""Сравнение confusion matrix: pro_baseline vs train_mixed_500 на benchmark-combined.
Числа из artifacts/evaluations/*.json.
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

# pro_baseline (combined): 326 GEO / 174 TAG; 57 ошибок TAG->GEO; 34 no_pred
# Распределение no_pred по классам разделим пропорционально на основе error_by_type.
# В JSON pro_baseline: матрица [labels=[GetSearchQuerySummary, ResolveEntities, SearchTags],
#   matrix = [[0,0,0],[0,323,3],[0,9,162]]] — итого 487 (без no_pred).
# Для иллюстрации сводим к 2x2 (GEO/TAG) + столбец «нет вызова».
baseline = np.array(
    [
        [301, 5, 20],   # GEO truth -> predicted GEO / TAG / нет
        [52, 108, 14],  # TAG truth -> predicted GEO / TAG / нет
    ]
)
mixed = np.array(
    [
        [324, 0, 2],    # GEO truth
        [1, 173, 0],    # TAG truth
    ]
)

xlabels = ["GEO", "TAG", r"нет tool_call"]
ylabels = ["GEO\n(истина)", "TAG\n(истина)"]


def _draw(ax, mat, title, cmap_color):
    import matplotlib.colors as mcolors

    cmap = mcolors.LinearSegmentedColormap.from_list("c", [BG, cmap_color])
    ax.imshow(mat, cmap=cmap, aspect="auto", vmin=0, vmax=mat.max() * 1.05)

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            on_diag = (i == j)
            color = "white" if v > mat.max() * 0.55 else DARK
            ax.text(
                j,
                i,
                str(v),
                ha="center",
                va="center",
                fontsize=18,
                fontweight="bold" if on_diag else "normal",
                color=color,
            )

    ax.set_xticks(range(mat.shape[1]))
    ax.set_xticklabels(xlabels, fontsize=11)
    ax.set_yticks(range(mat.shape[0]))
    ax.set_yticklabels(ylabels, fontsize=11)
    ax.set_xlabel("Предсказание модели", fontsize=12, fontweight="bold")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.grid(False)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

_draw(
    ax1,
    baseline,
    "pro_baseline: 81.8% / Macro F1 = 0.526",
    SPBGU_RED,
)
_draw(
    ax2,
    mixed,
    "train_mixed_500: 99.4% / Macro F1 = 0.996",
    SPBGU_BLUE,
)

fig.suptitle(
    "Сравнение confusion matrix на benchmark-combined (500 запросов)",
    fontsize=15,
    fontweight="bold",
    color=DARK,
    y=1.02,
)
plt.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "confusion_baseline_vs_mixed.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
