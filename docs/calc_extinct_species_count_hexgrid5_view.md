# extinct_species_count_hexgrid5
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_hexgrid5.geom_id, count(extinct_species_recordcount_hexgrid5.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_hexgrid5 GROUP BY extinct_species_recordcount_hexgrid5.geom_id;