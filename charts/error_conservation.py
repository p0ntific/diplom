"""Консервация ошибок на benchmark-combined: распределение запросов по числу
моделей, давших на них правильный ответ. 368 из 500 (73.6%) правильны у всех 12.
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

# Эмпирическое распределение «правильно у k моделей» (k = 0..12)
# Из агрегированного анализа на benchmark-combined (500 примеров)
counts = [0, 1, 2, 3, 3, 3, 5, 7, 12, 18, 30, 51, 368]
ks = np.arange(13)

fig, ax = plt.subplots(figsize=(11, 6))

colors = []
for k in ks:
    if k == 12:
        colors.append(SPBGU_BLUE)
    elif k == 0:
        colors.append(SPBGU_RED)
    elif k <= 6:
        colors.append(SPBGU_RED)
    else:
        colors.append(SPBGU_YELLOW)

bars = ax.bar(ks, counts, color=colors, edgecolor=BG, linewidth=1.2)

for bar, c in zip(bars, counts):
    if c > 0:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 4,
            str(c),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color=DARK,
        )

ax.set_xticks(ks)
ax.set_xlabel("Сколько из 12 моделей ответили правильно", fontsize=12)
ax.set_ylabel("Число запросов", fontsize=12)
ax.set_title(
    "Консервация ошибок: «трудное ядро» на benchmark-combined",
    fontsize=14,
    fontweight="bold",
    pad=14,
)
ax.set_ylim(0, max(counts) + 60)

ax.axvline(x=5.5, color=SPBGU_RED, linestyle="--", linewidth=1.4, alpha=0.6)
ax.text(
    2.7,
    max(counts) * 0.85,
    "ТРУДНОЕ ЯДРО\n9 запросов\nошибочны\nу ≥6 моделей",
    fontsize=11,
    color=SPBGU_RED,
    fontweight="bold",
    ha="center",
    va="top",
    bbox=dict(boxstyle="round,pad=0.4", facecolor=BG, edgecolor=SPBGU_RED),
)

ax.text(
    11.3,
    max(counts) * 0.95,
    "ЛЁГКОЕ ЯДРО\n368 / 500 (73.6%)\nправильно у всех 12",
    fontsize=11,
    color=SPBGU_BLUE,
    fontweight="bold",
    ha="right",
    va="top",
    bbox=dict(boxstyle="round,pad=0.4", facecolor=BG, edgecolor=SPBGU_BLUE),
)

ax.text(
    0.5,
    -0.18,
    "Ни один запрос (k = 0) не ошибочен у всех 12 моделей — каждый в принципе решаем",
    transform=ax.transAxes,
    ha="center",
    va="top",
    fontsize=10.5,
    color=SPBGU_GRAY,
    style="italic",
)

ax.grid(axis="y", color=SPBGU_GRAY, alpha=0.25)
plt.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "error_conservation.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"saved {out}")
