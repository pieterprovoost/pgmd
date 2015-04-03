# create_drs_with_woa
database: [obis](../)  
schema: [portal](portal)  

    
    	declare
    		table_name character varying;
    		msg character varying;
    		status boolean;
    		num_found integer;
    	begin
    		raise notice 'Create_drs_with_woa: start of the function'; 
    		
    		status := true;
    		
    		table_name := 'woa tables';
    		raise notice 'Checking woa tables'; 
    		num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('temperature', 'nitrate', 'oxygen', 'phosphate', 'salinity', 'silicate'));
    		if num_found < 6 then
    			status := false;
    			msg := table_name || ' not found (only ' || num_found || ' found)';
    		end if;
    				
    		if not status then
    			return msg;
    		end if;
    		
    		set search_path to portal;
    		truncate drs_with_woa;
    
    		raise notice 'Start populating drs_with_woa table...'; 
    		
    		insert into drs_with_woa
    		SELECT 
    		drs.id, drs.resource_id, resname, drs.lifestage, drs.basisofrecord, drs.latitude, drs.longitude, drs.coordinateprecision,
    		drs.datelastcached, drs.datecollected, drs.dateprecision::varchar, drs.datelastmodified,
    		date_part('year', datecollected)::int as yearcollected,
    		date_part('month', datecollected)::int as monthcollected,
    		date_part('day', datecollected)::int as daycollected,
    		drs.valid_id, sname, sauthor, tnames.tname, tnames.tauthor, storedpath,
    		geom, cs6m, eez_id, lme_id, meow_id, iho_id, fao_id, mwhs_id,
    		drs.depth, drs.depthprecision, bottomdepth, drs.display,
    		woadepth as woa_depth, woavals.temperature, salinity, nitrate, oxygen, phosphate, silicate
    		FROM obis.drs
    		inner JOIN obis.positions ON drs.position_id = positions.id
    		inner JOIN obis.resources ON drs.resource_id = resources.id
    		inner join obis.snames on drs.sname_id=snames.id
    		inner join obis.tnames on drs.valid_id=tnames.id
    		left join obis.woavals on drs.id=dr_id
    		WHERE tnames.display != '0'
    		order by valid_id, resource_id, datecollected;
    				
    		msg := 'Success!';
    		
    		raise notice 'Create_drs_with_woa: end of the function'; 
    		return msg;
    			
    	end;
