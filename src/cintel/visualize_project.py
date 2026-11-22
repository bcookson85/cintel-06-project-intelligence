"""Visualize integrated project performance monitoring results.

Author: Brian Cookson
Date: 2026-11

Create a chart of project response times and rolling monitoring signals.
"""

from pathlib import Path
from typing import Final

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import polars as pl

ROOT_DIR: Final[Path] = Path.cwd()
SIGNALS_FILE: Final[Path] = ROOT_DIR / "artifacts" / "project_signals.csv"
IMAGE_FILE: Final[Path] = (
    ROOT_DIR / "docs" / "images" / "project_response_monitoring.png"
)


def main() -> None:
    """Generate and save the project response monitoring visualization."""
    df = pl.read_csv(SIGNALS_FILE)

    observations = df["observation"].to_list()
    response_days = df["response_days"].to_list()
    rolling_avg = df["rolling_avg_response_days"].to_list()

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        observations,
        response_days,
        marker="o",
        linewidth=1.5,
        label="Individual response time",
    )

    ax.plot(
        observations,
        rolling_avg,
        linewidth=2.5,
        label="Five-request rolling average",
    )

    ax.axhline(
        y=7,
        linestyle="--",
        linewidth=1.5,
        label="Seven-day overdue threshold",
    )

    ax.set_title("Continuous Intelligence: Project Response Monitoring")
    ax.set_xlabel("Request observation number")
    ax.set_ylabel("Response time (days)")
    ax.set_xticks(range(1, 31, 2))
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    IMAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGE_FILE, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Visualization saved: {IMAGE_FILE}")


if __name__ == "__main__":
    main()
