# create_species_summaries
database: [obis](../)  
schema: [portal](portal)  

    
    declare
    	table_name character varying;
    	msg character varying;
    	status boolean;
    	num_found integer;
    begin
    	raise notice 'Start of function create_species_summaries'; 
    	
    	set search_path to portal, public;
    	
    	raise notice 'Start creating species summary table...'; 
    	
    	truncate species_summary;
    	insert into species_summary (
    		tname_id, valid_id, scientific, authority, parent_valid_id, rank_id, rank_name, kingdom_id,
    		worms_id, 
    		num_records, num_records_incl, num_resources, date_min, date_max, data_extent, 
    		depth_min, depth_max,
    		bottomdepth_min, bottomdepth_max, woa_depth_min, woa_depth_max, temperature_min, temperature_max,
    		salinity_min, salinity_max, nitrate_min, nitrate_max, oxygen_min, oxygen_max, phosphate_min, phosphate_max,
    		silicate_min, silicate_max, storedpath)
    	with extents as (
    		select valid_id, st_extent(geom) as b2d
    		from summaries.cs6m_valids
    		group by valid_id
    	)
    	select tnames.id, tnames.valid_id, tname, tauthor, tnames.parent_id, tnames.rank_id, 
    		rank_name,
    		case when storedpath='x' then null else regexp_replace(storedpath, '^x([1-9][0-9]*).*', E'\\1')::integer end,
    		worms_id, 
    		nexcl, nincl, (select count(*) from summaries.global_res_valids where global_res_valids.valid_id=tnames.id),
    		mindate, maxdate, 
    		extents.b2d::box2d,
    		mindepth, maxdepth, 
    		minbotdepth, maxbotdepth, 
    		minwoadepth, maxwoadepth, 
    		mintemperature, maxtemperature, minsalinity, maxsalinity, minnitrate, maxnitrate,
    		minoxygen, maxoxygen, minphosphate, maxphosphate, minsilicate, maxsilicate,
    		-- not used: min, maxo2sat, min, maxaou; should be included here and in web site
    		tnames.storedpath
    	from obis.tnames -- left join worms.tu on tnames.worms_id=tu.id no longer needed now that worms fields are restricted to worms_id
    		left join summaries.global_valids on tnames.id=global_valids.valid_id
    		left join obis.taxintenvelopes on tnames.id=taxintenvelopes.tname_id
    		left join extents on tnames.id=extents.valid_id
    		left join obis.ranks on tnames.rank_id=ranks.rank_id and kingdom_id=738303
    	WHERE coalesce(tnames.display, '1') = '1';
    	update species_summary set parent_valid_id=0 where scientific='Biota';
    	
    	raise notice 'Start creating species per resource...'; 
    	truncate species_per_resource;
    	insert into species_per_resource (
    		resource_id, valid_id, scientific, author, worms_id, rank_id, num_records, num_records_incl,
    		date_min, date_max, bbox
    	)
    	with minmaxdates as (
    		select valid_id, resource_id, min(datecollected) as mindate, max(datecollected) as maxdate
    		from obis.drs
    		where datecollected is not null
    		group by valid_id, resource_id
    	)
    	select drs.resource_id, drs.valid_id, tnames.tname as scientific, tnames.tauthor as author, 
    		worms_id, rank_id, count(*) as num_records, global_res_valids.nincl, 
    		mindate, maxdate, public.st_extent(geom)::box2d as bbox
    	from obis.drs inner join obis.tnames on drs.valid_id=tnames.id
    		left join obis.positions on drs.position_id=positions.id
    		left join summaries.global_res_valids on drs.valid_id=global_res_valids.valid_id and summaries.global_res_valids.resource_id=drs.resource_id
    		left join minmaxdates on drs.valid_id=minmaxdates.valid_id and drs.resource_id=minmaxdates.resource_id
    	WHERE coalesce(tnames.display, '1') = '1'
    	group by drs.resource_id, drs.valid_id, tnames.tname, tnames.tauthor, worms_id, rank_id, mindate, maxdate, global_res_valids.nincl;
    		
    	msg := 'Success!';
    	
    	raise notice 'End of the function'; 
    	return msg;
    		
    end;
