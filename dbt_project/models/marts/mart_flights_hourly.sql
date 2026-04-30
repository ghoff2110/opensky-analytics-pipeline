with base as (
    select * from {{ ref('stg_flights') }}
    where not on_ground
      and velocity_ms is not null
      and baro_altitude_m is not null
),

aggregated as (
    select
        origin_country,
        date(ingested_at)                        as flight_date,
        extract(hour from ingested_at)           as flight_hour,

        count(*)                                 as total_flights,
        count(distinct icao24)                   as unique_aircraft,

        round(avg(velocity_ms) * 3.6, 1)        as avg_speed_kmh,
        round(avg(baro_altitude_m), 0)           as avg_altitude_m,
        round(max(baro_altitude_m), 0)           as max_altitude_m,
        round(avg(vertical_rate_ms), 2)          as avg_vertical_rate,

        countif(vertical_rate_ms > 1)            as climbing_count,
        countif(vertical_rate_ms < -1)           as descending_count

    from base
    group by 1, 2, 3
)

select * from aggregated
order by total_flights desc