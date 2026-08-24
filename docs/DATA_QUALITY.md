# Data Quality Strategy

Silver validation treats quality as a first-class data product concern. Rules cover required event/patient/facility identifiers, model-confidence and image-quality ranges, and duplicate event IDs. Invalid rows are quarantined rather than silently dropped. Synthetic generators provide realistic failure modes for testing.
