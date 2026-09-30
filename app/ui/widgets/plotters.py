from typing import Sequence

import numpy as np
from matplotlib.axes import Axes

from app.models.algorithm_result import AlgorithmResult
from app.services.expression_parser import ParsedFunction
from app.utils.formatting import format_number

CURVE_COLOR = "#1d4ed8"
POINT_COLOR = "#dc2626"
GUIDE_COLOR = "#f59e0b"
AXIS_COLOR = "#6b7280"
FILL_COLOR = "#60a5fa"
MAX_DRAWN_STEPS = 8
CURVE_SAMPLES = 600


def _padded_range(values: Sequence[float]) -> tuple[float, float]:
    low, high = float(min(values)), float(max(values))
    span = high - low
    pad = span * 0.25 if span > 0 else 1.0
    return low - pad, high + pad


def _draw_curve(
    axes: Axes,
    function: ParsedFunction,
    low: float,
    high: float,
    include: Sequence[float] = (),
) -> None:
    xs = np.linspace(low, high, CURVE_SAMPLES)
    ys = function.evaluate_array(xs)
    axes.plot(xs, ys, color=CURVE_COLOR, linewidth=2, label="f(x)")
    axes.axhline(0, color=AXIS_COLOR, linewidth=1)
    finite = ys[np.isfinite(ys)]
    if finite.size:
        bottom, top = np.percentile(finite, [2, 98])
        bottom = min([bottom, 0.0, *include])
        top = max([top, 0.0, *include])
        margin = (top - bottom) * 0.15 or 1.0
        axes.set_ylim(bottom - margin, top + margin)
    axes.set_xlim(low, high)
    axes.set_xlabel("x")
    axes.set_ylabel("f(x)")


def plot_bisection(axes: Axes, result: AlgorithmResult) -> None:
    function: ParsedFunction = result.extra["function"]
    lower, upper = result.extra["interval"]
    rows = result.table_rows
    low, high = _padded_range([lower, upper])
    _draw_curve(axes, function, low, high, [function(lower), function(upper)])
    axes.axvspan(lower, upper, color=FILL_COLOR, alpha=0.12, label="Initial interval [a, b]")
    if rows:
        axes.scatter([row[3] for row in rows], [row[4] for row in rows], color=GUIDE_COLOR, s=30, zorder=3, label="c (midpoints)")
        for row in rows[:MAX_DRAWN_STEPS]:
            axes.annotate(str(row[0]), (row[3], row[4]), textcoords="offset points", xytext=(4, 6), fontsize=8)
        root = rows[-1][3]
        axes.axvline(root, color=POINT_COLOR, linestyle="--", label=f"Root ≈ {format_number(root)}")
    axes.set_title("Bisection Method")
    axes.legend(loc="best")


def plot_newton_raphson(axes: Axes, result: AlgorithmResult) -> None:
    function: ParsedFunction = result.extra["function"]
    path: list[float] = result.extra["path"][: MAX_DRAWN_STEPS + 1]
    low, high = _padded_range(path)
    values = [function(x) for x in path]
    _draw_curve(axes, function, low, high, values)
    for index in range(len(path) - 1):
        axes.plot([path[index], path[index + 1]], [values[index], 0], color=GUIDE_COLOR, linewidth=1.3,
                  label="Tangent lines" if index == 0 else None)
        axes.plot([path[index + 1]] * 2, [0, values[index + 1]], color=AXIS_COLOR, linestyle=":", linewidth=1)
    axes.scatter(path, values, color=GUIDE_COLOR, s=30, zorder=3, label="x_i on curve")
    if result.success and result.result is not None:
        axes.scatter([result.result], [0], color=POINT_COLOR, marker="*", s=140, zorder=4,
                     label=f"Root ≈ {format_number(result.result)}")
    axes.set_title("Newton-Raphson Method")
    axes.legend(loc="best")


def plot_secant(axes: Axes, result: AlgorithmResult) -> None:
    function: ParsedFunction = result.extra["function"]
    path: list[float] = result.extra["path"][: MAX_DRAWN_STEPS + 2]
    low, high = _padded_range(path)
    values = [function(x) for x in path]
    _draw_curve(axes, function, low, high, values)
    for index in range(len(path) - 2):
        axes.plot([path[index], path[index + 2]], [values[index], 0], color=GUIDE_COLOR, linewidth=1.3,
                  label="Secant lines" if index == 0 else None)
    axes.scatter(path, values, color=GUIDE_COLOR, s=30, zorder=3, label="x_i on curve")
    if result.success and result.result is not None:
        axes.scatter([result.result], [0], color=POINT_COLOR, marker="*", s=140, zorder=4,
                     label=f"Root ≈ {format_number(result.result)}")
    axes.set_title("Secant Method")
    axes.legend(loc="best")


def plot_trapezoidal(axes: Axes, result: AlgorithmResult) -> None:
    function: ParsedFunction = result.extra["function"]
    nodes: list[float] = result.extra["nodes"]
    values: list[float] = result.extra["values"]
    a, b = result.extra["a"], result.extra["b"]
    pad = (b - a) * 0.1
    _draw_curve(axes, function, a - pad, b + pad, values)
    axes.fill_between(nodes, values, color=FILL_COLOR, alpha=0.35, label="Trapezoids")
    axes.plot(nodes, values, color=POINT_COLOR, linewidth=1, marker="o", markersize=3)
    if len(nodes) <= 51:
        axes.vlines(nodes, 0, values, color=POINT_COLOR, linewidth=0.8)
    axes.set_title(f"Trapezoidal Rule (n = {result.extra['n']}) — Integral ≈ {format_number(result.result)}")
    axes.legend(loc="best")
