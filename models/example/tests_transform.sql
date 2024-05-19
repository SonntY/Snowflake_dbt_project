{{ config(materialized='table') }}


-- Create a new table with 1.standardized column names 2.dates in date format


with transformed_data as (
   select
       sugar as sugar,
       fe as fe,
       whitecells as white_cells,
       redcells as red_cells,
       to_date(date, 'DD/MM/YY') as date,
       id as id
   from tests
)


select * from transformed_data