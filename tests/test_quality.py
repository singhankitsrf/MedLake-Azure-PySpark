from medlake.quality import rule_names
def test_quality_rule_names_are_unique():
    names=rule_names(); assert len(names)==len(set(names)); assert "confidence_range" in names
