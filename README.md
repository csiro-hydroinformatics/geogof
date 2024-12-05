# geogof

[![ci](https://github.com/csiro-hydroinformatics/geogof/workflows/ci/badge.svg)](https://github.com/csiro-hydroinformatics/geogof/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://csiro-hydroinformatics.github.io/geogof/)
[![pypi version](https://img.shields.io/pypi/v/geogof.svg)](https://pypi.org/project/geogof/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#geogof:gitter.im)

Geographic visualisations for models' goodness of fit

## Purpose

Geogof is a Python library for creating geographic visualizations to assess the goodness of fit between jydrologic models and observed data. The library stems from the observation that the author(s) had recurring needs for exploring model performance on maps (static or interactive) and kept repurposing or reinventing ad-hoc code for various projects. `geogof` will focus on visualisation, not data analysis or model calibration.

- **interactive dashboards**: ipyleaflet, perhaps folium.
- **static maps**: matplotlib.

A prior example, to give a visual of the intented use (from [monthly-lstm-runoff](https://csiro-hydroinformatics.github.io/monthly-lstm-runoff/)):

<img src="https://csiro-hydroinformatics.github.io/monthly-lstm-runoff/img/model_benchmarking_dashboard_output.png" alt="interactive dashboard" width="700"/>

## Installation

from source:

```sh
cd path/to/geogof
uv pip install -e .
```

or, in a requirement.txt file: 

```txt
geogof @ git+https://github.com/csiro-hydroinformatics/geogof@main
```

**Placeholder as of dec 2024** Down the track this package may be installable via `pip` and [`uv`](https://docs.astral.sh/uv/).

```bash
pip install geogof
```

```bash
uv tool install geogof
```
