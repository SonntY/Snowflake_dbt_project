{{ config(materialized='table') }}


-- Join the transformed tables tests_transform and visit_info_transform on id and date
select
    t.id,
    t.date,
    t.sugar,
    t.fe,
    t.white_cells,       
    t.red_cells,
    v.sick,
    v.active,
    v.medication,
    v.regular
from tests_transform t
join visit_info_transform v
on t.id = v.id
and t.date = v.date