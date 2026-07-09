"""Generate a CVRP example figure: empty instance + same instance with a feasible solution.

Run with: uv run slide/figures/cvrp_example.py
Output:   slide/figures/cvrp_example.pdf
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)

N = 15
DEPOT = np.array([0.5, 0.5])
customers = rng.uniform(0.05, 0.95, size=(N, 2))
demands = rng.integers(3, 10, size=N)
Q = 30

# Build feasible routes by sweeping customers in angular order around the depot
angles = np.arctan2(customers[:, 1] - DEPOT[1], customers[:, 0] - DEPOT[0])
order = np.argsort(angles)

routes: list[list[int]] = []
current: list[int] = []
load = 0
for idx in order:
    if load + int(demands[idx]) > Q:
        routes.append(current)
        current = []
        load = 0
    current.append(int(idx))
    load += int(demands[idx])
if current:
    routes.append(current)

# Slide-palette colors (matches darkblue / myorange / mygreen / mypurple)
ROUTE_COLORS = ["#1E4678", "#F77F00", "#4CAF50", "#7832A0"]
CUSTOMER_COLOR = "#2E86AB"
DEPOT_COLOR = "#D62828"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))


def plot_instance(ax, draw_routes: bool) -> None:
    sizes = 60 + 25 * demands
    ax.scatter(
        customers[:, 0], customers[:, 1], s=sizes,
        c=CUSTOMER_COLOR, edgecolor="black", linewidth=0.5, alpha=0.9, zorder=3,
    )
    for i, (x, y) in enumerate(customers):
        ax.annotate(
            str(int(demands[i])), (x, y),
            fontsize=6, ha="center", va="center",
            color="white", fontweight="bold", zorder=4,
        )
    ax.scatter(
        [DEPOT[0]], [DEPOT[1]], marker="*", s=380,
        c=DEPOT_COLOR, edgecolor="black", linewidth=0.8, zorder=5,
    )
    if draw_routes:
        for r, route in enumerate(routes):
            color = ROUTE_COLORS[r % len(ROUTE_COLORS)]
            pts = np.vstack([DEPOT, customers[route], DEPOT])
            ax.plot(pts[:, 0], pts[:, 1], "-", color=color,
                    linewidth=2.2, zorder=2)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    for spine in ax.spines.values():
        spine.set_linewidth(0.6)


plot_instance(ax1, draw_routes=False)
ax1.set_title("Instance: depot + customers (demands)", fontsize=11)

plot_instance(ax2, draw_routes=True)
ax2.set_title(f"Feasible solution: {len(routes)} routes (Q={Q})", fontsize=11)

plt.tight_layout()

out_path = Path(__file__).resolve().parent / "cvrp_example.pdf"
plt.savefig(out_path, bbox_inches="tight", dpi=300)
print(f"Wrote {out_path}")
