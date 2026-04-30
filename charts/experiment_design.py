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

HERE = os.path.dirname(os.path.abspath(__file__))

# 1. Таблица обучающих выборок
fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.axis("off")
ax1.set_title("Обучающие выборки", fontsize=16, fontweight="bold", color=DARK, pad=16)

table_data = [
    ["train-synthetic-50", "50", "synthetic"],
    ["train-synthetic-250", "250", "synthetic"],
    ["train-synthetic-500", "500", "synthetic"],
    ["train-synthetic-1000", "908", "synthetic"],
    ["train-real-250", "250", "real"],
    ["train-mixed-500", "500", "mixed (250r + 250s)"],
]
col_labels = ["Выборка", "Примеров", "Тип данных"]

table = ax1.table(
    cellText=table_data,
    colLabels=col_labels,
    cellLoc="center",
    loc="center",
    colWidths=[0.36, 0.16, 0.42],
)
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.7)

for j in range(3):
    cell = table[0, j]
    cell.set_facecolor(SPBGU_BLUE)
    cell.set_text_props(color="white", fontweight="bold")
    cell.set_edgecolor(SPBGU_BLUE)

row_color_map = {
    "synthetic": "#E0E4EA",
    "real": "#CCE0F0",
    "mixed (250r + 250s)": "#CCE0F0",
}
for i, row in enumerate(table_data, start=1):
    bg = row_color_map.get(row[2], BG)
    for j in range(3):
        cell = table[i, j]
        cell.set_facecolor(bg)
        cell.set_edgecolor("#D8D8D8")
        cell.set_text_props(color=DARK)

fig1.savefig(os.path.join(HERE, "training_sets.png"), dpi=200, bbox_inches="tight")
print("saved training_sets.png")


# 2. Состав benchmark'ов (pie charts)
fig2, (ax_p1, ax_p2) = plt.subplots(1, 2, figsize=(10, 5))
fig2.suptitle("Состав benchmark'ов", fontsize=16, fontweight="bold", color=DARK, y=1.02)

pie_colors = [SPBGU_BLUE, SPBGU_YELLOW]

w1, t1, a1 = ax_p1.pie(
    [326, 174],
    labels=["GEO", "TAG"],
    colors=pie_colors,
    autopct=lambda p: f"{int(round(p * 500 / 100))}",
    startangle=90,
    textprops={"fontsize": 13, "color": DARK},
    wedgeprops={"edgecolor": BG, "linewidth": 2.5},
)
for t in a1:
    t.set_fontweight("bold")
    t.set_fontsize(15)
a1[0].set_color("white")
a1[1].set_color(DARK)
ax_p1.set_title("benchmark-combined\n(500)", fontsize=14, fontweight="bold", color=DARK, pad=12)

w2, t2, a2 = ax_p2.pie(
    [203, 47],
    labels=["GEO", "TAG"],
    colors=pie_colors,
    autopct=lambda p: f"{int(round(p * 250 / 100))}",
    startangle=90,
    textprops={"fontsize": 13, "color": DARK},
    wedgeprops={"edgecolor": BG, "linewidth": 2.5},
)
for t in a2:
    t.set_fontweight("bold")
    t.set_fontsize(15)
a2[0].set_color("white")
a2[1].set_color(DARK)
ax_p2.set_title("benchmark-real\n(250)", fontsize=14, fontweight="bold", color=DARK, pad=12)

fig2.savefig(os.path.join(HERE, "benchmark_composition.png"), dpi=200, bbox_inches="tight")
print("saved benchmark_composition.png")
