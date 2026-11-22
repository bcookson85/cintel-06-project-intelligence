"""Integrated project performance monitoring application.

Author: Brian Cookson
Date: 2026-11

Combine signal design, anomaly detection, rolling monitoring,
and baseline comparison using synthetic project request data.
"""

import logging
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import get_logger, log_header, log_path
import polars as pl

from cintel.utils_project import (
    assess_project_performance,
    compute_rolling_monitoring,
    design_project_signals,
    load_project_data,
)

LOG: logging.Logger = get_logger("P6-PROJECT", level="DEBUG")

ROOT_DIR: Final[Path] = Path.cwd()
DATA_FILE: Final[Path] = ROOT_DIR / "data" / "project_requests.csv"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

SIGNALS_FILE: Final[Path] = ARTIFACTS_DIR / "project_signals.csv"
ASSESSMENT_FILE: Final[Path] = ARTIFACTS_DIR / "project_assessment.csv"

OVERDUE_THRESHOLD: Final[int] = 7
ROLLING_WINDOW: Final[int] = 5
BASELINE_SIZE: Final[int] = 10
RECENT_SIZE: Final[int] = 10
DRIFT_THRESHOLD: Final[float] = 2.0


def main() -> None:
    """Run the integrated project intelligence monitoring pipeline."""
    log_header(LOG, "PROJECT CONTINUOUS INTELLIGENCE")

    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "SIGNALS_FILE", SIGNALS_FILE)
    log_path(LOG, "ASSESSMENT_FILE", ASSESSMENT_FILE)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    df: pl.DataFrame = load_project_data(DATA_FILE)
    LOG.info(f"STEP 1. Loaded {df.height} project request records")

    signals_df: pl.DataFrame = design_project_signals(
        df,
        overdue_threshold=OVERDUE_THRESHOLD,
    )
    LOG.info("STEP 2. Designed project response-time signals")

    monitoring_df: pl.DataFrame = compute_rolling_monitoring(
        signals_df,
        window_size=ROLLING_WINDOW,
    )
    LOG.info("STEP 3. Calculated rolling monitoring metrics")

    assessment_df: pl.DataFrame = assess_project_performance(
        monitoring_df,
        baseline_size=BASELINE_SIZE,
        recent_size=RECENT_SIZE,
        drift_threshold_days=DRIFT_THRESHOLD,
    )
    LOG.info("STEP 4. Completed integrated project assessment")

    monitoring_df.write_csv(SIGNALS_FILE)
    assessment_df.write_csv(ASSESSMENT_FILE)

    LOG.info(f"Saved detailed signals: {SIGNALS_FILE}")
    LOG.info(f"Saved project assessment: {ASSESSMENT_FILE}")

    LOG.info("Integrated assessment results:")
    for field_name, field_value in assessment_df.to_dicts()[0].items():
        LOG.info(f"{field_name}: {field_value}")

    LOG.info("Pipeline executed successfully!")


if __name__ == "__main__":
    main()
