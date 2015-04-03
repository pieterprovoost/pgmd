# calc_hexgrid5
database: [obis](../)  
schema: [hexgrid](hexgrid)  

|Column|Type|Constraint|
|:---|:---|:---|
|hex_id|integer|pk_calc_hexgrid5 |
|a|numeric||
|n|integer||
|d|numeric||
|s|integer||
|shannon|numeric||
|simpson|numeric||
|es|numeric||
|hill_1|numeric||
|hill_2|numeric||
|hill_inf|numeric||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
