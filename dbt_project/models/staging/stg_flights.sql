with source as (
    select * from {{ source('opensky_raw', 'opensky_data') }}
),

cleaned as (
    select
        icao24,
        nullif(trim(callsign), '') as callsign,
        origin_country,

        -- timestamps
        timestamp_seconds(cast(time_position as int64))  as time_position_utc,
        timestamp_seconds(cast(last_contact as int64))   as last_contact_utc,
        ingested_at,

        -- position
        round(latitude, 6)      as latitude,
        round(longitude, 6)     as longitude,
        round(baro_altitude, 2) as baro_altitude_m,
        round(geo_altitude, 2)  as geo_altitude_m,

        -- movement
        round(velocity, 2)      as velocity_ms,
        round(true_track, 2)    as true_track_deg,
        round(vertical_rate, 2) as vertical_rate_ms,

        -- flags
        on_ground,
        cast(spi as bool)       as spi,
        cast(position_source as string) as position_source,
        squawk

    from source
    where icao24 is not null
)

select * from cleaned