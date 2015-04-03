# extinct_species_count_hexgrid2
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_hexgrid2.geom_id, count(extinct_species_recordcount_hexgrid2.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_hexgrid2 GROUP BY extinct_species_recordcount_hexgrid2.geom_id;