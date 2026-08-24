from __future__ import annotations
import argparse,random
from pathlib import Path
import pandas as pd
CLASSES=["normal","acute_otitis_media","chronic_otitis_media","cerumen_impaction","myringosclerosis"]; MODES=["camp","clinic","tele_screening"]; DEVICES=["scope_a","scope_b","scope_c"]
def generate(rows:int,seed:int):
    rng=random.Random(seed); base=pd.Timestamp("2026-01-01T00:00:00Z"); out=[]
    for i in range(rows):
        cls=rng.choice(CLASSES); conf=round(rng.uniform(0.45,0.99),4); quality=round(rng.uniform(0.40,1.0),4); referred=cls!="normal" or conf<0.70 or quality<0.55; out.append({"event_id":f"EVT-{i:08d}","event_ts":(base+pd.Timedelta(minutes=i)).isoformat(),"patient_id":f"P-{rng.randint(1,2500):06d}","facility_id":f"FAC-{rng.randint(1,30):03d}","screening_mode":rng.choice(MODES),"device_type":rng.choice(DEVICES),"predicted_class":cls,"model_confidence":conf,"image_quality_score":quality,"referred":referred,"referral_reason":"abnormal_finding" if cls!="normal" else "none","ingestion_source":"synthetic_generator","schema_version":1})
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--rows",type=int,default=20000); ap.add_argument("--seed",type=int,default=42); ap.add_argument("--output",default="data/generated_screening_events.jsonl"); a=ap.parse_args(); p=Path(a.output); p.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(generate(a.rows,a.seed)).to_json(p,orient="records",lines=True); print(f"Wrote {a.rows} rows to {p}")
if __name__=="__main__": main()
