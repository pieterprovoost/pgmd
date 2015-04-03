# create_distribution_views
database: [obis](../)  
schema: [portal](portal)  

    
    declare
    	table character varying;
    	msg character varying;
    	status boolean;
    	num_found integer;
    begin
    	raise notice 'Start of the function'; 
    	
    	status := true;
    	
    	table := 'resources';
    	raise notice 'Checking resources'; 
        if not exists(SELECT relname FROM pg_class WHERE relname = table) then
    		status := false;
    	    msg := table || ' not found';
        end if;
        
    	table := 'species_summary';
    	raise notice 'Checking species_summary'; 
        if not exists(SELECT relname FROM pg_class WHERE relname = table) then
    		status := false;
    	    msg := table || ' not found';
        end if;
    
    	table := 'csxd_valids';
    	raise notice 'Checking csxd_valids'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('cs5d_valids', 'cs1d_valids', 'cs30m_valids', 'cs6m_valids'));
        if num_found < 4 then
    		status := false;
    	    msg := table || ' not found (only ' || num_found || ' found)';
        end if;
        
    	table := 'csxd_res_valids';
    	raise notice 'Checking csxd_res_valids'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('cs5d_res_valids', 'cs1d_res_valids', 'cs30m_res_valids', 'cs6m_res_valids'));
        if num_found < 4 then
    		status := false;
    	    msg := table || ' not found (only ' || num_found || ' found)';
        end if;
    
    
    	if not status then
    		return msg;
    	end if;
    	
    	
    	set search_path to portal;
    	
    	raise notice 'Start creating dist_sp_xdeg views...'; 
    	
    	-- copied from create_dist_sp_views.sql
    	-- 5 degree
    	CREATE OR REPLACE VIEW dist_sp_5deg AS
    	SELECT cs5d_valids.*,
    	species_summary.scientific, authority, rank_name
    	FROM summaries.cs5d_valids
    	JOIN species_summary ON cs5d_valids.valid_id = species_summary.valid_id;
    	
    	-- 1 degree
    	CREATE OR REPLACE VIEW dist_sp_1deg AS
    	SELECT cs1d_valids.*,
    	species_summary.scientific, authority, rank_name
    	FROM summaries.cs1d_valids
    	JOIN species_summary ON cs1d_valids.valid_id = species_summary.valid_id;
    	
    	-- 30m
    	CREATE OR REPLACE VIEW dist_sp_05deg AS
    	SELECT cs30m_valids.*,
    	species_summary.scientific, authority, rank_name
    	FROM summaries.cs30m_valids
    	JOIN species_summary ON cs30m_valids.valid_id = species_summary.valid_id;
    	
    	-- 6m
    	CREATE OR REPLACE VIEW dist_sp_01deg AS
    	SELECT cs6m_valids.*,
    	species_summary.scientific, authority, rank_name
    	FROM summaries.cs6m_valids
    	JOIN species_summary ON cs6m_valids.valid_id = species_summary.valid_id;
    	
    	
    	raise notice 'Start creating dist_sp_res_xdeg views...'; 
    	
    	-- copied from create_dist_sp_res_views.sql
    	-- 5 degree
    	CREATE OR REPLACE VIEW dist_sp_res_5deg AS
    	SELECT cs5d_res_valids.*,
    	species_summary.scientific, authority, rank_name,
    	resname
    	FROM summaries.cs5d_res_valids
    	JOIN species_summary ON cs5d_res_valids.valid_id = species_summary.valid_id
    	JOIN obis.resources ON cs5d_res_valids.resource_id = resources.id;
    	
    	
    	-- 1 degree
    	CREATE OR REPLACE VIEW dist_sp_res_1deg AS
    	SELECT cs1d_res_valids.*,
    	species_summary.scientific, authority, rank_name,
    	resname
    	FROM summaries.cs1d_res_valids
    	JOIN species_summary ON cs1d_res_valids.valid_id = species_summary.valid_id
    	JOIN obis.resources ON cs1d_res_valids.resource_id = resources.id;
    	
    	
    	-- 30m
    	CREATE OR REPLACE VIEW dist_sp_res_05deg AS
    	SELECT cs30m_res_valids.*,
    	species_summary.scientific, authority, rank_name,
    	resname
    	FROM summaries.cs30m_res_valids
    	JOIN species_summary ON cs30m_res_valids.valid_id = species_summary.valid_id
    	JOIN obis.resources ON cs30m_res_valids.resource_id = resources.id;
    	
    	-- 6m
    	CREATE OR REPLACE VIEW dist_sp_res_01deg AS
    	SELECT cs6m_res_valids.*,
    	species_summary.scientific, authority, rank_name,
    	resname
    	FROM summaries.cs6m_res_valids
    	JOIN species_summary ON cs6m_res_valids.valid_id = species_summary.valid_id
    	JOIN obis.resources ON cs6m_res_valids.resource_id = resources.id;
    	
    	
    	msg := 'Success!';
    	
    	raise notice 'End of the function'; 
    	return msg;
    		
    end;
