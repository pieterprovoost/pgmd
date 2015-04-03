# positions
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_positions |
|latitude|double precision||
|longitude|double precision||
|cs6m|character varying||
|margin|character varying||
|bottomdepth|integer||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
|eez_id|integer||
|lme_id|integer||
|meow_id|integer||
|iho_id|integer||
|fao_id|integer||
|mwhs_id|integer||
|hexgrid1_id|integer|[positions_hexgrid1_id_fkey](hexgrid_hexgrid1_table) |
|hexgrid2_id|integer|[positions_hexgrid2_id_fkey](hexgrid_hexgrid2_table) |
|hexgrid3_id|integer|[positions_hexgrid3_id_fkey](hexgrid_hexgrid3_table) |
|hexgrid4_id|integer|[positions_hexgrid4_id_fkey](hexgrid_hexgrid4_table) |
|hexgrid5_id|integer|[positions_hexgrid5_id_fkey](hexgrid_hexgrid5_table) |
|hexgrid6_id|integer|[positions_hexgrid6_id_fkey](hexgrid_hexgrid6_table) |
|lme66_id|integer||
|mpa_id|integer||
|dist2coast|double precision||
