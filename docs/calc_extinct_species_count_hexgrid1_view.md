# extinct_species_count_hexgrid1
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_hexgrid1.geom_id, count(extinct_species_recordcount_hexgrid1.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_hexgrid1 GROUP BY extinct_species_recordcount_hexgrid1.geom_id;