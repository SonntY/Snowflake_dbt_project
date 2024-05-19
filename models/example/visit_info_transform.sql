{{ config(materialized='table') }}


-- Create a new table with booleans and transformed dates


with transformed_data as (
   select
       case when sick = 1 then true else false end as sick,
       case when active = 1 then true else false end as active,
       case when medication = 1 then true else false end as medication,
       case when regular = 1 then true else false end as regular,
       to_date(date, 'DD/MM/YY') as date,
       id
   from visit_info
)


select * from transformed_data