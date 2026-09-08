from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class QualityRule:
    name: str
    expression: str
    description: str


SILVER_RULES = [
    QualityRule("event_id_not_null", "event_id IS NOT NULL", "Event identifier is required."),
    QualityRule(
        "patient_id_not_null", "patient_id IS NOT NULL", "Synthetic patient identifier is required."
    ),
    QualityRule(
        "facility_id_not_null", "facility_id IS NOT NULL", "Facility identifier is required."
    ),
    QualityRule(
        "confidence_range",
        "model_confidence BETWEEN 0.0 AND 1.0",
        "Confidence must be a probability.",
    ),
    QualityRule(
        "quality_range",
        "image_quality_score BETWEEN 0.0 AND 1.0",
        "Quality score must be a probability.",
    ),
]


def rule_names() -> list[str]:
    return [r.name for r in SILVER_RULES]
