from medlake.contracts import validate_event_dict
def valid(): return {"event_id":"EVT-1","event_ts":"2026-01-01T00:00:00Z","patient_id":"P-1","facility_id":"FAC-1","screening_mode":"clinic","device_type":"scope_a","predicted_class":"normal","model_confidence":0.9,"image_quality_score":0.8,"referred":False,"referral_reason":"none","ingestion_source":"test","schema_version":1}
def test_valid_event(): assert validate_event_dict(valid())==[]
def test_bad_confidence():
    row=valid(); row["model_confidence"]=1.2; assert "model_confidence_out_of_range" in validate_event_dict(row)
def test_missing_patient():
    row=valid(); row["patient_id"]=None; assert "patient_id_empty" in validate_event_dict(row)
