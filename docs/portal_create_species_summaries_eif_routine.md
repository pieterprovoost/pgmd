# create_species_summaries_eif
database: [obis](../)  
schema: [portal](portal)  

    
    declare
    	table_name character varying;
    	msg character varying;
    	status boolean;
    	num_found integer;
    begin
    	raise notice 'Species summaries: start of the function'; 
    	
    	status := true;
    	
    	table_name := 'worms.tu';
    --	raise notice 'Checking worms.tu'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('tu'));
        if num_found < 	1 then
    		status := false;
    	    msg := table_name || ' not found';
        end if;
    			
    	table_name := 'summaries.cs10d_res_valids';
    --	raise notice 'Checking summaries.cs10d_res_valids'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('cs10d_res_valids'));
        if num_found < 1 then
    		status := false;
    	    msg := table_name || ' not found';
        end if;
        
    	table_name := 'obis.tnames';
    --	raise notice 'Checking obis.tnames'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('tnames'));
        if num_found < 1 then
    		status := false;
    	    msg := table_name || ' not found';
        end if;
    
    	table_name := 'drs_with_woa';
    	raise notice 'Checking drs_with_woa'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('drs_with_woa'));
        if num_found < 1 then
    		status := false;
    	    msg := table_name || ' not found';
        end if;
    
    	table_name := 'obis.ranks';
    --	raise notice 'Checking obis.ranks'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('ranks'));
        if num_found < 1 then
    		status := false;
    	    msg := table_name || ' not found';
        end if;
    
    	table_name := 'obis.resources';
    --	raise notice 'Checking obis.resources'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('resources'));
        if num_found < 1 then
    		status := false;
    	    msg := table_name || ' not found';
        end if;
    
    	if not status then
    		return msg;
    	end if;
    	
    	
    	set search_path to portal;
    	
    	raise notice 'Start creating species_summary table...'; 
    	
    	-- copied from create_species-summary_v6.sql
    	-- This is Edward's version, more efficient and it does not need the second SQL to add non-worms species.
    	DROP TABLE IF EXISTS species_summary CASCADE;
    	
    	CREATE TABLE species_summary AS
    	
    	SELECT
    	tu.id as worms_id,
    	tnames.valid_id,
    	tname as scientific,
    	tauthor as authority,
    	tu_parent as parent_worms_id,
    	parent_id as parent_valid_id,
    	tnames.rank_id,
    	rank_name,
    	ranks.kingdom_id,
    	nexcl as num_records,
    	nincl as num_records_incl,
    	num_resources,
    	date_min,
    	date_max,
    	data_extent,
    	depth_min, depth_max, bottomdepth_min, bottomdepth_max, woa_depth_min, woa_depth_max,
    	temperature_min, temperature_max, salinity_min, salinity_max, 
    	nitrate_min, nitrate_max, oxygen_min, oxygen_max, phosphate_min, phosphate_max,
    	silicate_min, silicate_max, 
    	tu_sp as taxon_tree_worms,
    	storedpath as taxon_tree
    	
    	FROM
    	obis.tnames
    	
    	LEFT JOIN worms.tu ON tu.id = tnames.worms_id
    	LEFT JOIN 
    	(
    	SELECT
    	valid_id,
    	sum(nexcl) as nexcl,
    	sum(nincl) as nincl,
    	count(distinct resource_id) as num_resources
    	FROM
    	summaries.global_res_valids
    	GROUP BY valid_id
    	) foo ON tnames.id = foo.valid_id
    	
    	LEFT JOIN
    	(
    	SELECT
    	valid_id,
    	min((datecollected AT TIME ZONE 'GMT')::timestamp(0)) as date_min,
    	max((datecollected AT TIME ZONE 'GMT')::timestamp(0)) as date_max,
    	public.st_extent(geom) as data_extent,
    	min(depth) as depth_min,
    	max(depth) as depth_max,
    	min(bottomdepth) as bottomdepth_min,
    	max(bottomdepth) as bottomdepth_max,
    	min(woa_depth) as woa_depth_min,
    	max(woa_depth) as woa_depth_max,
    	min(temperature) as temperature_min,
    	max(temperature) as temperature_max,
    	min(salinity) as salinity_min,
    	max(salinity) as salinity_max,
    	min(nitrate) as nitrate_min,
    	max(nitrate) as nitrate_max,
    	min(oxygen) as oxygen_min,
    	max(oxygen) as oxygen_max,
    	min(phosphate) as phosphate_min,
    	max(phosphate) as phosphate_max,
    	min(silicate) as silicate_min,
    	max(silicate) as silicate_max
    	FROM
    	drs_with_woa
    	GROUP BY valid_id
    	) goo ON tnames.id = goo.valid_id
    	
    	--LEFT JOIN obis.ranks ON tnames.rank_id = ranks.rank_id and ranks.kingdom_id = substring(storedpath from '[0-9]*[^|]')::int
    	LEFT JOIN obis.ranks ON tnames.rank_id = ranks.rank_id and ranks.kingdom_id = CASE WHEN tnames.rank_id = 10 THEN 738303 ELSE (string_to_array(storedpath, '|')::text[])[3]::int END	
    	WHERE
    	tnames.id = tnames.valid_id;
    	
    	
    	raise notice 'Start creating indexes on species_summary...'; 
    	-- copied from create_indexes_on_species_summary.sql
    	CREATE INDEX idx_species_summary_parent_worms_id
    	  ON species_summary
    	  USING btree
    	  (parent_worms_id);
    	
    	CREATE INDEX idx_species_summary_scientific
    	  ON species_summary
    	  USING btree
    	  (lower(scientific::text));
    	
    	CREATE INDEX idx_species_summary_taxon_tree_worms
    	  ON species_summary
    	  USING btree
    	  (taxon_tree_worms);
    	
    	CREATE INDEX idx_species_summary_valid_id
    	  ON species_summary
    	  USING btree
    	  (valid_id);
    	
    	CREATE INDEX idx_species_summary_worms_id
    	  ON species_summary
    	  USING btree
    	  (worms_id);	
    	
    
    	raise notice 'Start creating speices_per_resource...'; 
    	-- copied from species_per_resource_v2.sql
    	DROP TABLE IF EXISTS species_per_resource CASCADE;
    	
    	CREATE TABLE species_per_resource AS
    	SELECT
    	global_res_valids.resource_id,
    	global_res_valids.valid_id,
    	tname as scientific,
    	worms_id,
    	rank_id,
    	nexcl as num_records,
    	nincl as num_records_incl,
    	date_min,
    	date_max,
    	bbox,
    	bbox_str
    	FROM
    	summaries.global_res_valids
    	JOIN obis.tnames on global_res_valids.valid_id = tnames.valid_id and tnames.id = tnames.valid_id
    	JOIN 
    	(SELECT 
    	valid_id,
    	resource_id,
    	min(datecollected) as date_min,
    	max(datecollected) as date_max,
    	public.st_extent(geom) as bbox,
    	public.st_xmin(public.st_extent(geom))::text || ',' || public.st_ymin(public.st_extent(geom))::text || ',' || public.st_xmax(public.st_extent(geom))::text || ',' || public.st_ymax(public.st_extent(geom))::text as bbox_str
    	FROM
    	obis.drs
    	join obis.positions ON drs.position_id = positions.id
    	GROUP BY resource_id, drs.valid_id
    	) foo ON global_res_valids.valid_id = foo.valid_id and global_res_valids.resource_id = foo.resource_id
    	;
    	
    	CREATE INDEX idx_species_per_resource_valid_id
    	  ON species_per_resource
    	  USING btree
    	  (valid_id);
    	  
    	CREATE INDEX idx_species_per_resource_resource_id
    	  ON species_per_resource
    	  USING btree
    	  (resource_id);
    
    	
    	msg := 'Success!';
    	
    	raise notice 'End of the function'; 
    	return msg;
    		
    end;
