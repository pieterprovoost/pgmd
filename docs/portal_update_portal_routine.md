# update_portal
database: [obis](../)  
schema: [portal](portal)  

    
    declare
    	table_name character varying;
    	msg character varying;
    	status boolean;
    	num_found integer;
    begin
    	raise notice 'Start update portal'; 
    
    	table_name := 'obis.snames';
    	-- raise notice 'Checking obis.snames'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('snames'));
    	if num_found < 1 then
    		status := false;
    		msg := table_name || ' not found';
    	end if;
        
    	table_name := 'obis.tnames';
    	-- raise notice 'Checking obis.tnames'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('tnames'));
    	if num_found < 1 then
    		status := false;
    		msg := table_name || ' not found';
    	end if;
    
    	table_name := 'obis.drs';
    	-- raise notice 'Checking obis.drs'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('drs'));
    	if num_found < 1 then
    		status := false;
    		msg := table_name || ' not found';
    	end if;
    
    	table_name := 'obis.positions';
    	-- raise notice 'Checking obis.positions'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('positions'));
    	if num_found < 1 then
    		status := false;
    		msg := table_name || ' not found';
    	end if;
    
    	table_name := 'obis.resources';
    	--raise notice 'Checking obis.resources'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('resources'));
    	if num_found < 1 then
    		status := false;
    		msg := table_name || ' not found';
    	end if;
    
    	if not status then
    		return msg;
    	end if;
    	
    	-- all functions have to be rewritten to do a truncate rather than a drop of the tables; this is the best way of assuring
    	-- that all the indexes and permits are consistent across versions.
    	raise notice 'create drs with woa returned %', portal.create_drs_with_woa();
    	
    	-- Ei's species_summaries are created starting from WoRMS; some irregularities in the taxonomic classification
    	-- make taxa (incl Decapoda) disappear. While the irregularities in tnames table have been weeded out, I think
    	-- it is safer to construct the summaries on the basis of the tnames table directly
    	-- Now Edward's version is incorporated into create_species_summaries.
    	raise notice 'create species summaries returned %', portal.create_species_summaries();
    
    	-- functions below have to be revisited; most of the functionality is a duplication of what happens while
    	-- indexing in the OBIS schema.
    
    	-- we no longer have to create the views, as they are not deleted as in Ei's version of the procedure
    	--raise notice 'create distribution views returned %', portal.create_distribution_views();
    
    	-- we no longer have to create the views, as they are not deleted as in Ei's version of the procedure
    	--raise notice 'create summary views returned %', portal.create_summary_views();
    
    	-- we no longer have to create these tables, as they are not deleted in the first place as in Ei's version
    	--raise notice 'create support tables returned %', portal.create_support_tables();
    
    	return 'finished';
    		
    end;
