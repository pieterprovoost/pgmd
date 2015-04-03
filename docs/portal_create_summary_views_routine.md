# create_summary_views
database: [obis](../)  
schema: [portal](portal)  

    
    declare
    	table_name character varying;
    	msg character varying;
    	status boolean;
    	num_found integer;
    begin
    	raise notice 'Create summary views: start of the function'; 
    	
    	status := true;
    	
    	table_name := 'geo.csxd';
    	raise notice 'Checking geo.csxd'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('cs5d', 'cs1d', 'cs30m'));
        if num_found < 3 then
    		status := false;
    	    msg := table_name || ' not found (only ' || num_found || ' found)';
        end if;
        
    	table_name := 'calc.mapxd';
    	raise notice 'Checking calc.mapxd'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('map5d', 'map1d', 'map30m', 'map6m'));
        if num_found < 4 then
    		status := false;
    	    msg := table_name || ' not found (only ' || num_found || ' found)';
        end if;
    
    
    	if not status then
    		return msg;
    	end if;
    	
    	
    	set search_path to portal;
    	
    	raise notice 'Start creating mapxdeg_with_geom views...'; 
    	
    	-- copied from create_summaries_views.sql
    	CREATE OR REPLACE VIEW map5deg_with_geom AS 
    	 SELECT map5d.cscode, map5d.n, map5d.s, map5d.shannon::real, map5d.simpson::real, map5d.es::real, cs5d.geom
    	   FROM calc.map5d
    	   JOIN geo.cs5d ON map5d.cscode::text = cs5d.cscode::text;
    	
    	CREATE OR REPLACE VIEW map1deg_with_geom AS 
    	 SELECT map1d.cscode, map1d.n, map1d.s, map1d.shannon::real, map1d.simpson::real, map1d.es::real, cs1d.geom
    	   FROM calc.map1d
    	   JOIN geo.cs1d ON map1d.cscode::text = cs1d.cscode::text;
    	
    	CREATE OR REPLACE VIEW map05deg_with_geom AS 
    	 SELECT map30m.cscode, map30m.n, map30m.s, map30m.shannon::real, map30m.simpson::real, map30m.es::real, cs30m.geom
    	   FROM calc.map30m
    	   JOIN geo.cs30m ON map30m.cscode::text = cs30m.cscode::text;
    
    	CREATE OR REPLACE VIEW map01deg_with_geom AS 
    	 SELECT map6m.cscode, map6m.n, map6m.s, map6m.shannon::real, map6m.simpson::real, map6m.es::real, cs6m.geom
    	   FROM calc.map6m
    	   JOIN geo.cs6m ON map6m.cscode::text = cs6m.cscode::text;
    
    /*
    	
    	raise notice 'Start creating map01deg_with_geom table...'; 
    	
    	-- copied from create_create_map6m_with_geom.sql
    	DROP TABLE IF EXISTS map01deg_with_geom CASCADE;
    	
    	CREATE TABLE map01deg_with_geom AS
    	SELECT
    	*, 
    	public.st_geomfromtext(geo.get_wkt_from_csquare(cscode)) as geom
    	FROM
    	calc.map6m;
    	
    	CREATE INDEX idx_map01deg_with_geom_geom ON map01deg_with_geom
    	USING gist
    	(geom);
    	
    */	
    	msg := 'Success!';
    	
    	raise notice 'End of the function'; 
    	return msg;
    		
    end;
