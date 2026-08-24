WITH latest AS (SELECT MAX(_event_date) AS max_date FROM medlake.gold.facility_daily_kpis)
SELECT facility_id,screenings,referrals,referral_rate,avg_model_confidence,avg_image_quality
FROM medlake.gold.facility_daily_kpis WHERE _event_date=(SELECT max_date FROM latest)
ORDER BY referral_rate DESC,screenings DESC LIMIT 20;
