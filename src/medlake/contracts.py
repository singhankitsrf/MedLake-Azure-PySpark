from __future__ import annotations
EVENT_REQUIRED_FIELDS={"event_id","event_ts","patient_id","facility_id","screening_mode","device_type","predicted_class","model_confidence","image_quality_score","referred","referral_reason","ingestion_source","schema_version"}
ALLOWED_CLASSES={"normal","acute_otitis_media","chronic_otitis_media","cerumen_impaction","myringosclerosis"}
ALLOWED_SCREENING_MODES={"camp","clinic","tele_screening"}
def validate_event_dict(event:dict)->list[str]:
    errors=[]; missing=EVENT_REQUIRED_FIELDS-set(event)
    if missing: return [f"missing_fields={sorted(missing)}"]
    if not event.get("event_id"): errors.append("event_id_empty")
    if not event.get("patient_id"): errors.append("patient_id_empty")
    if not event.get("facility_id"): errors.append("facility_id_empty")
    c=event.get("model_confidence"); q=event.get("image_quality_score")
    if not isinstance(c,(int,float)) or not 0<=c<=1: errors.append("model_confidence_out_of_range")
    if not isinstance(q,(int,float)) or not 0<=q<=1: errors.append("image_quality_score_out_of_range")
    if event.get("predicted_class") not in ALLOWED_CLASSES: errors.append("unknown_predicted_class")
    if event.get("screening_mode") not in ALLOWED_SCREENING_MODES: errors.append("unknown_screening_mode")
    return errors
