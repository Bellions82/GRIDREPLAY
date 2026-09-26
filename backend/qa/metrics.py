from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricResult:
    name: str
    value: float | None
    threshold: float | None
    status: str
    source: str


def metric(
    name: str,
    value: float | None,
    threshold: float | None,
    source: str = "provider",
) -> MetricResult:
    if value is None or threshold is None:
        status = "UNKNOWN"
    else:
        status = "PASS" if value >= threshold else "FAIL"
    return MetricResult(name, value, threshold, status, source)


def normalize_metrics(raw: dict | None) -> dict:
    raw = raw or {}
    return {
        key: value
        for key, value in raw.items()
        if isinstance(value, (int, float, str, bool, type(None)))
    }


def evaluate_thresholds(metrics: dict, thresholds: dict) -> dict:
    results = {}
    failures = []
    unknowns = []

    for name, threshold in thresholds.items():
        value = metrics.get(name)
        result = metric(
            name,
            float(value) if isinstance(value, (int, float)) else None,
            float(threshold) if threshold is not None else None,
        )
        results[name] = {
            "value": result.value,
            "threshold": result.threshold,
            "status": result.status,
            "source": result.source,
        }
        if result.status == "FAIL":
            failures.append(name)
        elif result.status == "UNKNOWN":
            unknowns.append(name)

    return {
        "results": results,
        "failures": failures,
        "unknowns": unknowns,
        "complete": not unknowns,
    }
