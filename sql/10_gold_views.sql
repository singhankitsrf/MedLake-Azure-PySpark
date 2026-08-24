CREATE OR REPLACE VIEW medlake.gold.vw_daily_network_summary AS
SELECT _event_date, SUM(screenings) AS screenings, SUM(referrals) AS referrals,
SUM(referrals) / NULLIF(SUM(screenings),0) AS referral_rate,
AVG(avg_model_confidence) AS avg_model_confidence, AVG(avg_image_quality) AS avg_image_quality
FROM medlake.gold.facility_daily_kpis GROUP BY _event_date;
