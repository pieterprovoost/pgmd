# extinct_species_count_hexgrid6
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_hexgrid6.geom_id, count(extinct_species_recordcount_hexgrid6.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_hexgrid6 GROUP BY extinct_species_recordcount_hexgrid6.geom_id;