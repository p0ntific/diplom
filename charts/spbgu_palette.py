"""Единый модуль цветовой палитры СПбГУ для всех графиков защитной презентации.

Использование:
    from spbgu_palette import (
        SPBGU_RED, SPBGU_BLUE, SPBGU_YELLOW, SPBGU_WHITE, SPBGU_GRAY,
        BG, DARK, apply_spbgu_style,
    )
    apply_spbgu_style()
"""

import matplotlib.pyplot as plt

SPBGU_RED = "#9E1B32"
SPBGU_BLUE = "#003F7D"
SPBGU_GRAY = "#5A5A5A"          # тёмно-серый — прочие конфигурации
SPBGU_SLATE = "#8C99A6"         # сине-серый — синтетика (вместо жёлтого/коричневого)
SPBGU_GRAY_LIGHT = "#C8C8C8"
SPBGU_WHITE = "#FFFFFF"

# Совместимость: старые импорты SPBGU_YELLOW и SPBGU_BROWN -> SPBGU_SLATE.
SPBGU_YELLOW = SPBGU_SLATE
SPBGU_BROWN = SPBGU_SLATE

BG = "#FFFFFF"
DARK = "#0F1115"
LIGHT_GRID = "#D8D8D8"


def apply_spbgu_style():
    """Глобальная настройка matplotlib под палитру СПбГУ."""
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
            "font.size": 12,
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "text.color": DARK,
            "axes.edgecolor": SPBGU_GRAY,
            "axes.labelcolor": DARK,
            "axes.titlecolor": DARK,
            "xtick.color": DARK,
            "ytick.color": DARK,
            "axes.grid": True,
            "grid.color": LIGHT_GRID,
            "grid.alpha": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
