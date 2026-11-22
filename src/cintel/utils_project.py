"""Utility functions for integrated project performance monitoring.

Author: Brian Cookson
Date: 2026-11

Combine signal design, anomaly detection, rolling monitoring,
and baseline comparison using synthetic project request data.
"""

from pathlib import Path

import polars as pl


def load_project_data(data_file: Path) -> pl.DataFrame:
    """Load and validate synthetic project request observations."""
    df = pl.read_csv(data_file)

    required = {"request_id", "project_phase", "response_days"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.height < 20:
        raise ValueError("At least 20 observations are required.")

    if df.select(
        pl.any_horizontal(
            pl.col("request_id").is_null(),
            pl.col("project_phase").is_null(),
            pl.col("response_days").is_null(),
        ).any()
    ).item():
        raise ValueError("Required fields cannot contain missing values.")

    if (df["response_days"] < 0).any():
        raise ValueError("Response days cannot be negative.")

    if df["request_id"].n_unique() != df.height:
        raise ValueError("Request IDs must be unique.")

    return df


def design_project_signals(
    df: pl.DataFrame,
    overdue_threshold: int = 7,
) -> pl.DataFrame:
    """Add overdue and anomaly signals to individual observations."""
    return df.with_row_index("observation", offset=1).with_columns(
        [
            (pl.col("response_days") > overdue_threshold).alias("is_overdue"),
            (pl.col("response_days") > overdue_threshold).alias("is_anomaly"),
        ]
    )


def compute_rolling_monitoring(
    df: pl.DataFrame,
    window_size: int = 5,
) -> pl.DataFrame:
    """Calculate rolling average response time and overdue percentage."""
    if window_size < 1:
        raise ValueError("Window size must be positive.")

    return df.with_columns(
        [
            pl.col("response_days")
            .rolling_mean(window_size=window_size)
            .round(2)
            .alias("rolling_avg_response_days"),
            (
                pl.col("is_overdue")
                .cast(pl.Float64)
                .rolling_mean(window_size=window_size)
                * 100
            )
            .round(2)
            .alias("rolling_overdue_pct"),
        ]
    )


def assess_project_performance(
    df: pl.DataFrame,
    baseline_size: int = 10,
    recent_size: int = 10,
    drift_threshold_days: float = 2.0,
) -> pl.DataFrame:
    """Assess recent performance against an earlier observation baseline."""
    if baseline_size < 1 or recent_size < 1:
        raise ValueError("Comparison periods must contain observations.")

    if baseline_size + recent_size > df.height:
        raise ValueError("Baseline and recent periods must not overlap.")

    if drift_threshold_days < 0:
        raise ValueError("Drift threshold cannot be negative.")

    baseline = df.head(baseline_size)
    recent = df.tail(recent_size)

    baseline_avg = float(baseline["response_days"].mean())
    recent_avg = float(recent["response_days"].mean())

    difference = recent_avg - baseline_avg
    drift_detected = abs(difference) > drift_threshold_days

    total_anomalies = int(df["is_anomaly"].sum())
    recent_overdue_pct = float(recent["is_overdue"].mean()) * 100

    system_state = "DEGRADED" if drift_detected else "STABLE"

    return pl.DataFrame(
        {
            "total_observations": [df.height],
            "total_anomalies": [total_anomalies],
            "baseline_avg_days": [round(baseline_avg, 2)],
            "recent_avg_days": [round(recent_avg, 2)],
            "response_difference_days": [round(difference, 2)],
            "drift_threshold_days": [drift_threshold_days],
            "drift_detected": [drift_detected],
            "recent_overdue_pct": [round(recent_overdue_pct, 2)],
            "system_state": [system_state],
        }
    )
