{{ config(materialized='table') }}

-- Create a new table with corrected city names and transformed dates, see Git
with corrected_city_dates as (
   select
       name,
       family,
       id,
       case
           when substring(birthdate, 7, 2)::int <= 24 then to_date('20' || substring(birthdate, 7, 2) || '-' || substring(birthdate, 4, 2) || '-' || substring(birthdate, 1, 2), 'YYYY-MM-DD')
           else to_date('19' || substring(birthdate, 7, 2) || '-' || substring(birthdate, 4, 2) || '-' || substring(birthdate, 1, 2), 'YYYY-MM-DD')
       end as birthdate,
       lower(case
                 when city = 'Ramay Gan' then 'Ramat Gan'
                 when city = 'Raaana' then 'Raanana'
                 else city
            end) as city,
       lower(region) as region
   from patients
)

select * from corrected_city_dates