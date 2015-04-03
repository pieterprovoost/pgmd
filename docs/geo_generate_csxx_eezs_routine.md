# generate_csxx_eezs
database: [obis](../)  
schema: [geo](geo)  

    
    
    /*Creating tables intersecting eezs and csquares from 10d down to 6m
    Should be ran each time a new version of the EEZ layer is available from VLIZ
    
    Input: string, can be anything - use to identify the run
    
    evberghe 2010-05-22
    */
    
    	declare
    		s varchar(255); -- return variable
    		eezrecord geo.eezs%rowtype;
    		eez_csrecord geo.eez_cs10d%rowtype;
    	begin
    		set search_path to geo, public;
    
    		truncate eez_cs10d;
    		for eezrecord in select * from geo.eezs loop
    			insert into eez_cs10d(cscode, eez_id, geom)
    				select cs10d.cscode, eezrecord.id, st_intersection(geom, eezrecord.geom)
    				from cs10d where geom && eezrecord.geom;
    			raise notice E'cs10d % \r\n', eezrecord.id;
    		end loop;
    		delete from eez_cs10d where st_isempty(geom) or geometrytype(geom) in ('POINT','LINESTRING');
    		update eez_cs10d set fullsquare=st_equals(eez_cs10d.geom, cs10d.geom) 
    			from cs10d where eez_cs10d.cscode=cs10d.cscode;
    
    		truncate eez_cs5d;
    		for eez_csrecord in select * from geo.eez_cs10d where not fullsquare loop
    			insert into eez_cs5d(cscode, eez_id, geom)
    				select cs5d.cscode, eez_csrecord.eez_id, st_intersection(geom, eez_csrecord.geom)
    				from cs5d where cscode~('^'||eez_csrecord.cscode);
    			raise notice E'cs5d % \r\n', eez_csrecord.id;
    		end loop;
    		delete from eez_cs5d where st_isempty(geom) or geometrytype(geom) in ('POINT','LINESTRING');
    		update eez_cs5d set fullsquare=st_equals(eez_cs5d.geom, cs5d.geom) 
    			from cs5d where eez_cs5d.cscode=cs5d.cscode;
    
    		truncate eez_cs1d;
    		for eez_csrecord in select * from geo.eez_cs5d where not fullsquare loop
    			insert into eez_cs1d(cscode, eez_id, geom)
    				select cs1d.cscode, eez_csrecord.eez_id, st_intersection(geom, eez_csrecord.geom)
    				from cs1d where cscode~('^'||eez_csrecord.cscode);
    			raise notice E'cs1d % \r\n', eez_csrecord.id;
    		end loop;
    		delete from eez_cs1d where st_isempty(geom) or geometrytype(geom) in ('POINT','LINESTRING');
    		update eez_cs1d set fullsquare=st_equals(eez_cs1d.geom, cs1d.geom) 
    			from cs1d where eez_cs1d.cscode=cs1d.cscode;
    
    		truncate eez_cs30m;
    		for eez_csrecord in select * from geo.eez_cs1d where not fullsquare loop
    			insert into eez_cs30m(cscode, eez_id, geom)
    				select cs30m.cscode, eez_csrecord.eez_id, st_intersection(geom, eez_csrecord.geom)
    				from cs30m where cscode~('^'||eez_csrecord.cscode);
    			raise notice E'cs30m % \r\n', eez_csrecord.id;
    		end loop;
    		delete from eez_cs30m where st_isempty(geom) or geometrytype(geom) in ('POINT','LINESTRING');
    		update eez_cs30m set fullsquare=st_equals(eez_cs30m.geom, cs30m.geom) 
    			from cs30m where eez_cs30m.cscode=cs30m.cscode;
    
    -- table cs6m does not exist, so we first create a table with the cs6m squares we need
    		drop table if exists cs6m;
    		create table cs6m(id serial, cscode character varying (16), geom geometry);
    		insert into cs6m(cscode, geom)
    			select cscode||csdiv5.c5 as cscode, 
    				st_geomfromtext(get_wkt_from_csquare(cscode||csdiv5.c5),4326) as geom
    			from eez_cs30m, csdiv5
    			where not fullsquare
    				and substring(cscode from 10 for 1)=csdiv5.c2;
    		truncate eez_cs6m;
    		for eez_csrecord in select * from geo.eez_cs30m where not fullsquare loop
    			insert into eez_cs6m(cscode, eez_id, geom)
    				select cscode, eez_csrecord.eez_id, st_intersection(cs6m.geom, eez_csrecord.geom)
    				from cs6m where cscode~('^'||eez_csrecord.cscode);
    			raise notice E'cs6m % \r\n', eez_csrecord.id;
    		end loop;
    		delete from eez_cs6m where st_isempty(geom) or geometrytype(geom) in ('POINT','LINESTRING');
    		update eez_cs6m set fullsquare=false where geometrytype(geom)='GEOMETRYCOLLECTION'; 
    		update eez_cs6m set fullsquare=
    			st_equals(geom, public.st_polyfromtext(get_wkt_from_csquare(cscode),4326)) 
    			where fullsquare is null;
    		
    		s:='Return string: '||i;
    	return s;
    	end;
