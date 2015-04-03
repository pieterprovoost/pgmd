# create_drs_with_woa_eif
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
    --	raise notice 'Checking woa tables'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('temperature', 'nitrate', 'oxygen', 'phosphate', 'salinity', 'silicate'));
    	if num_found < 6 then
    		status := false;
    		msg := table_name || ' not found (only ' || num_found || ' found)';
    	end if;
    			
    	table_name := 'obis.snames';
    --	raise notice 'Checking obis.snames'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('snames'));
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
    
    	table_name := 'obis.drs';
    --	raise notice 'Checking obis.drs'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('drs'));
        if num_found < 1 then
    		status := false;
    	    msg := table_name || ' not found';
        end if;
    
    	table_name := 'obis.positions';
    --	raise notice 'Checking obis.positions'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('positions'));
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
    	
    	raise notice 'Start creating woa_depths table...'; 
    	
    	-- copied from create_woa_depth.sql
    	DROP TABLE IF EXISTS woa_depths CASCADE;
    	
    	CREATE TABLE woa_depths AS
    	SELECT depth FROM woa.temperature GROUP BY depth ORDER BY depth;
    
    	
    	raise notice 'Start creating drs_with_woa_pre_clustered table...'; 
    	
    	-- copied from create_drs_with_woa.sql
    	DROP TABLE IF EXISTS drs_with_woa_pre_clustered CASCADE;
    	
    	CREATE TABLE drs_with_woa_pre_clustered AS
    	SELECT 
    	drs.id, drs.resource_id, resname, drs.lifestage, drs.basisofrecord, drs.latitude, drs.longitude, drs.coordinateprecision,
    	drs.datelastcached, drs.datecollected, drs.dateprecision::varchar, drs.datelastmodified,
    	date_part('year', datecollected)::int as yearcollected,
    	date_part('month', datecollected)::int as monthcollected,
    	date_part('day', datecollected)::int as daycollected,
    	drs.valid_id, 
    	 (SELECT sname FROM obis.snames WHERE drs.sname_id = snames.id) as sname,
    	 (SELECT sauthor FROM obis.snames WHERE drs.sname_id = snames.id) as sauthor,
    	 (SELECT tname FROM obis.snames WHERE drs.sname_id = snames.id) as tname,
    	 (SELECT storedpath FROM obis.tnames WHERE drs.valid_id = tnames.valid_id and tnames.id = tnames.valid_id) as storedpath,
    	 geom, cs6m, eez_id, lme_id, meow_id, iho_id,
    	 drs.depth, drs.depthprecision, bottomdepth, drs.display,
    	 -- if drs.depth (sample depth is null), do not sample oceanographic variables
    	CASE
    	    WHEN drs.depth IS NULL THEN NULL
    	    ELSE ( SELECT woa_depths.depth
    	       FROM woa_depths
    	      ORDER BY abs(woa_depths.depth::double precision - drs.depth)
    	     LIMIT 1)
    	END AS woa_depth, 
    	--(SELECT temperature.pval
    	--	FROM woa.temperature
    	--	WHERE "substring"(positions.cs6m::text, 1, 8) = temperature.cscode::text AND 
    	--	CASE
    	--	    WHEN drs.depth IS NULL THEN 0
    	--	    ELSE ( SELECT woa_depths.depth
    	--	       FROM woa_depths
    	--	      ORDER BY abs(woa_depths.depth::double precision - drs.depth)
    	--	     LIMIT 1)
    	--	END = temperature.depth) AS temperature, 
    	CASE WHEN drs.depth IS NULL THEN NULL
    	ELSE
    		(SELECT temperature.pval
    			FROM woa.temperature
    			WHERE "substring"(positions.cs6m::text, 1, 8) = temperature.cscode::text AND 
    			    ( SELECT woa_depths.depth
    			       FROM woa_depths
    			      ORDER BY abs(woa_depths.depth::double precision - drs.depth)
    			     LIMIT 1) = temperature.depth) 
    	END AS temperature, 
    	CASE WHEN drs.depth IS NULL THEN NULL 
    	ELSE
    		(SELECT salinity.pval
    			FROM woa.salinity
    			WHERE "substring"(positions.cs6m::text, 1, 8) = salinity.cscode::text AND 
    			    ( SELECT woa_depths.depth
    			       FROM woa_depths
    			      ORDER BY abs(woa_depths.depth::double precision - drs.depth)
    			     LIMIT 1) = salinity.depth) 
    	END AS salinity, 
    	CASE WHEN drs.depth IS NULL THEN NULL
    	ELSE
    		(SELECT nitrate.pval
    			FROM woa.nitrate
    			WHERE "substring"(positions.cs6m::text, 1, 8) = nitrate.cscode::text AND 
    			    ( SELECT woa_depths.depth
    			       FROM woa_depths
    			      ORDER BY abs(woa_depths.depth::double precision - drs.depth)
    			     LIMIT 1) = nitrate.depth)
    	END AS nitrate, 
    	CASE WHEN drs.depth IS NULL THEN NULL
    	ELSE
    		(SELECT oxygen.pval
    			FROM woa.oxygen
    			WHERE "substring"(positions.cs6m::text, 1, 8) = oxygen.cscode::text AND 
    			    ( SELECT woa_depths.depth
    			       FROM woa_depths
    			      ORDER BY abs(woa_depths.depth::double precision - drs.depth)
    			     LIMIT 1) = oxygen.depth) 
    	END AS oxygen, 
    	CASE WHEN drs.depth IS NULL THEN NULL
    	ELSE
    		(SELECT phosphate.pval
    			FROM woa.phosphate
    			WHERE "substring"(positions.cs6m::text, 1, 8) = phosphate.cscode::text AND 
    			    ( SELECT woa_depths.depth
    			       FROM woa_depths
    			      ORDER BY abs(woa_depths.depth::double precision - drs.depth)
    			     LIMIT 1) = phosphate.depth) 
    	END AS phosphate, 
    	CASE WHEN drs.depth IS NULL THEN NULL
    	ELSE
    		(SELECT silicate.pval
    			FROM woa.silicate
    			WHERE "substring"(positions.cs6m::text, 1, 8) = silicate.cscode::text AND 
    			    ( SELECT woa_depths.depth
    			       FROM woa_depths
    			      ORDER BY abs(woa_depths.depth::double precision - drs.depth)
    			     LIMIT 1) = silicate.depth) 
    	END AS silicate
    	FROM obis.drs
    	JOIN obis.positions ON drs.position_id = positions.id
    	JOIN obis.resources ON drs.resource_id = resources.id;
    	
    	raise notice 'Start creating indexes on drs_with_woa_pre_clustered...';	
    	CREATE INDEX idx_drs_with_woa_pre_clustered_valid_id ON drs_with_woa_pre_clustered USING btree (valid_id);
    	CREATE INDEX idx_drs_with_woa_pre_clustered_resource_id ON drs_with_woa_pre_clustered USING btree (resource_id);
    	CREATE INDEX idx_drs_with_woa_pre_clustered_datecollected ON drs_with_woa_pre_clustered USING btree (datecollected);	
    
    	raise notice 'Start creating drs_with_woa_clustered...';	
    	-- copied from create_drs_with_woa.sql
    	DROP TABLE IF EXISTS drs_with_woa_clustered CASCADE;
    	CREATE TABLE drs_with_woa_clustered AS
    		SELECT * FROM drs_with_woa_pre_clustered ORDER BY valid_id, resource_id, datecollected, latitude, longitude;
    
    	  
    	raise notice 'Start creating indexes on drs_with_woa_clustered...';	
    	CREATE INDEX idx_drs_with_woa_clustered_resource_id ON drs_with_woa_clustered USING btree (resource_id);
    	CREATE INDEX idx_drs_with_woa_clustered_datecollected ON drs_with_woa_clustered USING btree (datecollected);
    	CREATE INDEX idx_drs_with_woa_clustered_yearcollected ON drs_with_woa_clustered USING btree (yearcollected);
    	CREATE INDEX idx_drs_with_woa_clustered_monthcollected ON drs_with_woa_clustered USING btree (monthcollected);
    	CREATE INDEX idx_drs_with_woa_clustered_daycollected ON drs_with_woa_clustered USING btree (daycollected);
    	CREATE INDEX idx_drs_with_woa_clustered_id ON drs_with_woa_clustered USING btree (id);
    	CREATE INDEX idx_drs_with_woa_clustered_valid_id ON drs_with_woa_clustered USING btree (valid_id);
    	CREATE INDEX idx_drs_with_woa_clustered_geom ON drs_with_woa_clustered USING gist (geom);
    	CREATE INDEX idx_drs_with_woa_clustered_temperature ON drs_with_woa_clustered USING btree (temperature);
    	CREATE INDEX idx_drs_with_woa_clustered_salinity ON drs_with_woa_clustered USING btree (salinity);
    	CREATE INDEX idx_drs_with_woa_clustered_nitrate ON drs_with_woa_clustered USING btree (nitrate);
    	CREATE INDEX idx_drs_with_woa_clustered_oxygen ON drs_with_woa_clustered USING btree (oxygen);
    	CREATE INDEX idx_drs_with_woa_clustered_phosphate ON drs_with_woa_clustered USING btree (phosphate);
    	CREATE INDEX idx_drs_with_woa_clustered_silicate ON drs_with_woa_clustered USING btree (silicate);
    	CREATE INDEX idx_drs_with_woa_clustered_eez_id ON drs_with_woa_clustered USING btree (eez_id);
    	CREATE INDEX idx_drs_with_woa_clustered_lme_id ON drs_with_woa_clustered USING btree (lme_id);
    	CREATE INDEX idx_drs_with_woa_clustered_meow_id ON drs_with_woa_clustered USING btree (meow_id);      
    	CREATE INDEX idx_drs_with_woa_clustered_iho_id ON drs_with_woa_clustered USING btree (iho_id);
    	CREATE INDEX idx_drs_with_woa_clustered_storedpath ON drs_with_woa_clustered USING btree (upper(storedpath));
    	  
    	raise notice 'Start creating drs_with_woa...';	
    	DROP TABLE IF EXISTS drs_with_woa CASCADE;
    	ALTER TABLE drs_with_woa_clustered RENAME TO drs_with_woa;
    	
    	ALTER INDEX idx_drs_with_woa_clustered_resource_id RENAME TO idx_drs_with_woa_resource_id;
    	ALTER INDEX idx_drs_with_woa_clustered_datecollected RENAME TO idx_drs_with_woa_datecollected;
    	ALTER INDEX idx_drs_with_woa_clustered_yearcollected RENAME TO idx_drs_with_woa_yearcollected;
    	ALTER INDEX idx_drs_with_woa_clustered_monthcollected RENAME TO idx_drs_with_woa_monthcollected;
    	ALTER INDEX idx_drs_with_woa_clustered_daycollected RENAME TO idx_drs_with_woa_daycollected;
    	ALTER INDEX idx_drs_with_woa_clustered_id RENAME TO idx_drs_with_woa_id;
    	ALTER INDEX idx_drs_with_woa_clustered_valid_id RENAME TO idx_drs_with_woa_valid_id;
    	ALTER INDEX idx_drs_with_woa_clustered_geom RENAME TO idx_drs_with_woa_geom;
    	ALTER INDEX idx_drs_with_woa_clustered_temperature RENAME TO idx_drs_with_woa_temperature;
    	ALTER INDEX idx_drs_with_woa_clustered_salinity RENAME TO idx_drs_with_woa_salinity;
    	ALTER INDEX idx_drs_with_woa_clustered_nitrate RENAME TO idx_drs_with_woa_nitrate;
    	ALTER INDEX idx_drs_with_woa_clustered_oxygen RENAME TO idx_drs_with_woa_oxygen;
    	ALTER INDEX idx_drs_with_woa_clustered_phosphate RENAME TO idx_drs_with_woa_phosphate;
    	ALTER INDEX idx_drs_with_woa_clustered_silicate RENAME TO idx_drs_with_woa_silicate;
    	ALTER INDEX idx_drs_with_woa_clustered_eez_id RENAME TO idx_drs_with_woa_eez_id;
    	ALTER INDEX idx_drs_with_woa_clustered_lme_id RENAME TO idx_drs_with_woa_lme_id;
    	ALTER INDEX idx_drs_with_woa_clustered_meow_id RENAME TO idx_drs_with_woa_meow_id;
    	ALTER INDEX idx_drs_with_woa_clustered_iho_id RENAME TO idx_drs_with_woa_iho_id;
    	ALTER INDEX idx_drs_with_woa_clustered_storedpath RENAME TO idx_drs_with_woa_storedpath;
    	
    	DROP TABLE drs_with_woa_pre_clustered CASCADE;
    	  
    	raise notice 'Start creating points_ex...';	
    	CREATE OR REPLACE VIEW points_ex AS
    	SELECT
    	drs_with_woa.*,
    	--resources.resname,
    	--dxs.datelastmodified, 
    	dxs.recordlastcached, 
    	dxs.sourceofrecord, 
    	dxs.citation, 
    	dxs.recordurl, 
    	--dxs.basisofrecord, 
    	dxs.institutioncode, 
    	dxs.collectioncode, 
    	dxs.catalognumber, 
    	dxs.collector, 
    	--dxs.yearcollected, 
    	dxs.startyearcollected, 
    	dxs.endyearcollected, 
    	--dxs.monthcollected, 
    	dxs.startmonthcollected, 
    	dxs.endmonthcollected, 
    	--dxs.daycollected, 
    	dxs.startdaycollected, 
    	dxs.enddaycollected, 
    	dxs.starttimecollected, 
    	dxs.endtimecollected, 
    	dxs.julianday, 
    	dxs.startjulianday, 
    	dxs.endjulianday, 
    	dxs.timeofday, 
    	dxs.starttimeofday, 
    	dxs.endtimeofday, 
    	dxs.timezone, 
    	dxs.locality, 
    	dxs.ocean, 
    	dxs.country, 
    	dxs.state, 
    	dxs.county, 
    	--dxs.latitude, 
    	--dxs.longitude, 
    	--dxs.coordinateprecision, 
    	dxs.cscode, 
    	dxs.slatitude, 
    	dxs.elatitude, 
    	dxs.slongitude, 
    	dxs.elongitude, 
    	dxs.seprecision, 
    	--dxs.depth, 
    	--dxs.depthprecision, 
    	dxs.minimumdepth, 
    	dxs.maximumdepth, 
    	dxs.depthrange, 
    	--dxs.datecollected, 
    	--dxs.lifestage, 
    	dxs.identifiedby, 
    	dxs.yearidentified, 
    	dxs.monthidentified, 
    	dxs.dayidentified, 
    	dxs.typestatus, 
    	dxs.collectornumber, 
    	dxs.fieldnumber, 
    	--dxs.temperature, 
    	dxs.sex, 
    	dxs.preparationtype, 
    	dxs.individualcount, 
    	dxs.observedindividualcount, 
    	dxs.observedweight, 
    	dxs.samplesize, 
    	dxs.previouscatalognumber, 
    	dxs.relationshiptype, 
    	dxs.relatedcatalogitem, 
    	dxs.notes, 
    	dxs.concatenated
    	FROM
    	drs_with_woa
    	JOIN obis.dxs ON drs_with_woa.id = dxs.dr_id;
    	
    	msg := 'Success!';
    	
    	raise notice 'Create_drs_with_woa: end of the function'; 
    	return msg;
    		
    end;
