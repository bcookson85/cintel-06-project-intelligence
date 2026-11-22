# cintel-06-continuous-intelligence

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](pyproject.toml)
[![CI](https://github.com/bcookson85/cintel-06-project-intelligence/actions/workflows/ci-python-zensical.yml/badge.svg)](https://github.com/bcookson85/cintel-06-project-intelligence/actions/workflows/ci-python-zensical.yml)
[![Documentation](https://img.shields.io/badge/docs-site-blue?logo=github)](https://bcookson85.github.io/cintel-06-project-intelligence/)

[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> Combine monitoring signals and anomaly detection to assess system health.

## Project Overview

**Author:** Brian Cookson

**Date:** November 2026

This project explores integrated continuous intelligence monitoring
using Python and Polars as part of the Continuous Intelligence course
at Northwest Missouri State University.

The initial objective is to understand and execute Dr. Denise Case's
original continuous intelligence example, which transforms system
measurements into analytical signals, detects unusual observations,
and evaluates overall system health.

### Proposed Customization: Integrated Project Performance Monitoring

My proposed customization will combine the project performance
monitoring techniques developed throughout previous modules into
a single continuous intelligence application.

Using synthetic project request response data, the application
will explore:

- **Signal Design:** Calculate meaningful project performance
  indicators, including response times and overdue request rates.
- **Anomaly Detection:** Identify individual project requests
  with unusually long response times.
- **Rolling Monitoring:** Track changes in response performance
  across successive observations.
- **Drift Detection:** Compare recent response performance against
  historical baseline measurements.
- **Integrated Assessment:** Combine these indicators to evaluate
  overall project responsiveness and identify potential issues.

The goal is to demonstrate how multiple analytical techniques
can work together to provide a more complete understanding of
project performance and support informed operational decisions.

The project is configured in [pyproject.toml](pyproject.toml).

### Technical Experiment: Maximum Average Latency Threshold

**Objective:** Investigate how changing the maximum average latency
threshold affects anomaly detection and overall system assessment.

**Original Configuration:**
The original application used a maximum average latency threshold
of 40.0 milliseconds.

With this threshold, the pipeline processed 60 system observations,
detected 7 anomalies, and classified the overall system as STABLE.

The average latency was approximately 33.71 milliseconds.

**Modification:**
In `src/cintel/continuous_intelligence.py`, I changed:

`MAX_AVG_LATENCY: Final[float] = 40.0`

to:

`MAX_AVG_LATENCY: Final[float] = 30.0`

**Reason:**
I wanted to examine how reducing an operational threshold affects
the sensitivity of an integrated continuous intelligence application.

**Prediction:**
I predicted that lowering the latency threshold to 30.0 milliseconds
would change the overall classification from STABLE to DEGRADED
because the average latency of 33.71 milliseconds would exceed
the new threshold.

I also expected the number of detected anomalies to increase.

**Actual Results:**
After rerunning the pipeline, the system classification changed
from STABLE to DEGRADED.

The number of detected anomalies increased from 7 to 40.

| Measurement | Original | Modified |
|---|---:|---:|
| Maximum latency threshold | 40.0 ms | 30.0 ms |
| Average latency | 33.71 ms | 33.71 ms |
| Detected anomalies | 7 | 40 |
| Overall system state | STABLE | DEGRADED |

**Interpretation:**
The experiment demonstrated that the detection thresholds
significantly influence the results of continuous intelligence
monitoring.

Although the underlying observations and average latency remained
unchanged, reducing the threshold caused 33 additional observations
to be flagged and changed the overall system classification.

**Conclusion:**
Operational thresholds should be selected based on meaningful
performance requirements rather than arbitrary values.

Thresholds set too low may produce excessive alerts, while
thresholds set too high may overlook important performance changes.

## Data

The example uses system metrics from `data/`.

Each observation includes:

- `requests` - number of requests handled.
- `errors` - number of failed requests.
- `total_latency_ms` - total response time in milliseconds.

The example uses stored observations to demonstrate
an integrated monitoring assessment.

## Approach

The pipeline uses Polars to:

1. Read system measurements.
2. Calculate error rate and average latency.
3. Identify signals exceeding defined thresholds.
4. Summarize system behavior.
5. Assign a system assessment based on the monitored signals.

Explore these project components:

- [pyproject.toml](pyproject.toml) - project configuration and dependencies.
- [src/cintel/continuous_intelligence.py](src/cintel/continuous_intelligence.py) - integrated monitoring pipeline.
- [data/](data/) - system measurements.
- [artifacts/](artifacts/) - generated system assessment.
- [tests/](tests/) - automated tests.
- [.github/workflows/](.github/workflows/) - automated checks and documentation deployment.
- [docs/](docs/) - project documentation.

## Run the Project

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
to set up your machine and project environment.

From a VS Code terminal in the project root:

```shell
uv run python -m cintel.continuous_intelligence
```

## Run the Reactive App

From a VS Code terminal in the project root
(hit CTRL + c to quit):

```shell
uv run marimo run  src/cintel/app.py
```

## Results

The pipeline summarizes the monitored signals
and writes `artifacts/system_assessment.csv`.
Review the resulting system assessment and explain
which signals support the reported state.

The example classifies the system state as:

- **STABLE** - summary signals remain within the defined thresholds.
- **DEGRADED** - one or more summary signals exceed the defined thresholds.

Successful execution produces a terminal message:

```shell
========================
Pipeline executed successfully!
========================
```

A `project.log` file is created in the project root.

This confirms that the Python pipeline executes
and the logging system works.

## Verification

Run the automated tests:

```shell
uv run pytest
```

## Project Documentation

The [hosted documentation site][hosted documentation site](https://bcookson85.github.io/cintel-06-project-intelligence/)
is published using Zensical and GitHub Pages.

The documentation site is used to present the project report,
covering such sections as data, methods, results, visualizations,
interpretation, and conclusions.

## CI/CD and GitHub Actions

This project includes continuous integration and continuous deployment (CI/CD)
to check project files and publish the docs.
GitHub Actions include:

- [CI: Python and Documentation Checks](https://github.com/bcookson85/cintel-06-project-intelligence/actions/workflows/ci-python-zensical.yml)
- [CD: Documentation Deployment](https://github.com/bcookson85/cintel-06-project-intelligence/actions/workflows/deploy-zensical.yml)

## Developer Reference

Follow the
[Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
for **detailed instructions and troubleshooting**.

### Initialize and Update the Python Environment

With the project open in VS Code, open a VS Code terminal.
Paste each command and hit Enter or Return after to run it.

```shell
uvx pup-clean --delete
uv self update
uv python pin 3.14
uv python install
uv lock --upgrade
uv sync
uv audit
```

### Set Up and Run Git Hooks

Set up and run the git hooks to perform
basic checks automatically before
any changes get pushed to GitHub.

In the VS Code terminal,
paste each command and hit Enter or Return after to run it.

```shell
uvx prek install --force
uvx prek update --freeze --cooldown-days 7

git add -A
uvx prek run --all-files
# repeat if changes were made
uvx prek run --all-files
```

### Run Common Chores

Run linters, formatters, type checks, tests, and
build the documentation.

```shell
uv run ruff check . --fix
uv run ruff format .

uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

### Git add-commit-push to GitHub

After making useful changes, save your work to GitHub.

```shell
git add -A
git commit -m "describe your changes in quotes"
git push -u origin main
```

## Developer Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.

## Developer Tools

This project uses professional Python tools to support development,
testing, documentation, and code quality.

- [uv](https://docs.astral.sh/uv/) - Python environments and dependencies.
- [Ruff](https://docs.astral.sh/ruff/) - Python linting and formatting, configured in [.ruff.toml](.ruff.toml).
- [ty](https://docs.astral.sh/ty/) - Python type checking.
- [pytest](https://docs.pytest.org/) - automated Python testing, configured in [.pytest.toml](.pytest.toml).
- [prek](https://prek.j178.dev/) - Git hooks and automated checks, configured in [prek.toml](prek.toml).
- [Zensical](https://zensical.org/) - project documentation, configured in [zensical.toml](zensical.toml).

## Links

- [Hosted Documentation](https://bcookson85.github.io/cintel-06-project-intelligence/)
- [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
- [Citation](CITATION.cff)
- [License](LICENSE)
