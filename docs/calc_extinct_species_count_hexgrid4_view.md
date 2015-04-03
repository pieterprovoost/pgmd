# extinct_species_count_hexgrid4
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_hexgrid4.geom_id, count(extinct_species_recordcount_hexgrid4.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_hexgrid4 GROUP BY extinct_species_recordcount_hexgrid4.geom_id;