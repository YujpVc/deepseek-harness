# Agent Note: Editable data charts in the PPT assistant

Status: implemented

English | [中文](2026-10-08-native-data-charts.zh.md)

## Problem

The general PPT generator needs charts that express composition, trends and relationships as well as simple category comparisons. Limited chart selection, weak labeling and screenshot-based charts make data difficult to interpret and edit.

## Decision

The shared [chart module](../../../../ppt-assistant/charts.py) resolves inline JSON or explicit CSV data, validates it and produces twelve native PowerPoint chart types with embedded workbooks. The [generator](../../../../ppt-assistant/build_deck.py) exposes single-chart pages and two-to-four-chart dashboards in ordinary decks and reference-template expansion. Strict template filling retains its existing behavior. Chart data and rendering remain engine-owned, independent of workspace scripts.

Missing measurements remain gaps. Ranking moves labels and values together. Validation rejects non-finite numbers, malformed CSV, mixed input sources, invalid composition data and axes that hide observations or stacked totals. Bar and area charts retain zero. Percentage stacks preserve source counts, use a 0–1 value axis and omit count labels by default. Explicit count labels retain their original units.

The [preset](../../../../profiles/yujp-web/presets/ppt-assistant/agent.cordis.yml) chooses charts by the question being answered, prefers native charts for data-heavy decks and requires source, unit and rendered-label checks. Shared styling provides series colors, sparse category ticks, highlights, axis titles and coordinated panels; dense bar panels fail instead of squeezing unreadable labels.

## Alternatives considered

**Embed raster chart images.** This allows more specialized plots but loses editable series and duplicates data presentation outside the engine.

**Add a plotting service or another dependency.** The existing PowerPoint library supports the required chart types and embedded workbooks without another service or package.

## Verification

The [keyless example](../../../../ppt-assistant/examples/chart_report.json) exercises all chart types with explicitly labeled example data. Its [snapshot](../../../../ppt-assistant/examples/chart_report.expected.json) records visible text, native types, series values, XY coordinates and bubble areas. [Tests](../../../../ppt-assistant/test_charts.py) invoke the CLI, reread native data, verify embedded workbooks and check CSV, gaps, invalid inputs, zero baselines, template cover preservation, dashboard geometry and output preservation. Structure and geometry checks precede rendered review; chart-internal labels still require visual inspection.

## Consequences

Users can edit charts and their data in the resulting PPTX. Capacities depend on panel geometry, and category ticks can be sparse without discarding observations. Fixed palettes, a six-series limit and an eight-slice limit favor readable business charts; specialized scientific plots need a separate artifact. LibreOffice rendering provides visual evidence; WPS interactive editing requires application-specific verification.
