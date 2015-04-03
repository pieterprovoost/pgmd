# extinct_species_count_hexgrid3
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_hexgrid3.geom_id, count(extinct_species_recordcount_hexgrid3.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_hexgrid3 GROUP BY extinct_species_recordcount_hexgrid3.geom_id;