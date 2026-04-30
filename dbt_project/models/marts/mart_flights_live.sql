select
    icao24,
    callsign,
    origin_country,
    latitude,
    longitude,
    baro_altitude_m,
    velocity_ms,
    round(velocity_ms * 3.6, 1)  as velocity_kmh,
    true_track_deg,
    vertical_rate_ms,
    on_ground,
    ingested_at

from {{ ref('stg_flights') }}
where latitude is not null
  and longitude is not null